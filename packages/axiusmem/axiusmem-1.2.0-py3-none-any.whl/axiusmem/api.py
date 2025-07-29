import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List, Optional
import rdflib
from .user_management import UserManager, AXM
from axiusmem.adapters.base import get_triplestore_adapter_from_env
import logging
from rdflib import Literal
import time
from threading import Lock
import tenacity

def create_app(graph=None):
    SECRET_KEY = os.getenv("AXIUSMEM_SECRET_KEY", "change_this_secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    app = FastAPI(title="AxiusMEM User/Role Management API")
    if graph is None:
        graph = rdflib.Graph()
    user_manager = UserManager(graph)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    class Token(BaseModel):
        access_token: str
        token_type: str

    class UserOut(BaseModel):
        username: str
        roles: List[str]

    def create_access_token(data: dict):
        from datetime import datetime, timedelta
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        if username not in user_manager.list_users():
            raise credentials_exception
        return username

    def require_admin(username: str = Depends(get_current_user)):
        if not user_manager.is_admin(username):
            raise HTTPException(status_code=403, detail="Admin privileges required")
        return username

    def ensure_initial_admin():
        disable_bootstrap = os.getenv("AXIUSMEM_DISABLE_ADMIN_BOOTSTRAP", "0").lower() in ("1", "true", "yes")
        if disable_bootstrap:
            logging.info("Admin bootstrap is disabled by AXIUSMEM_DISABLE_ADMIN_BOOTSTRAP.")
            return
        admin_user = os.getenv("AXIUSMEM_ADMIN_USER", "admin")
        admin_password = os.getenv("AXIUSMEM_ADMIN_PASSWORD", "admin")
        if admin_user in user_manager.list_users():
            # Update password and roles for existing admin user
            # Remove old password hash triple
            user_uri = user_manager._user_uri(admin_user)
            for p, o in list(user_manager.graph.predicate_objects(user_uri)):
                if str(p) == str(AXM.hasPasswordHash):
                    user_manager.graph.remove((user_uri, p, o))
            # Add new password hash
            import bcrypt
            pw_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
            user_manager.graph.add((user_uri, AXM.hasPasswordHash, Literal(pw_hash)))
            # Ensure admin role is present
            if "admin" not in user_manager.get_user_roles(admin_user):
                user_manager.assign_role(admin_user, "admin")
            logging.info(f"Updated existing admin user '{admin_user}' with new credentials and roles.")
        else:
            try:
                user_manager.create_user(admin_user, admin_password, roles=["admin"])
                if admin_password == "admin":
                    logging.warning(f"Default admin password is in use for user '{admin_user}'. Set AXIUSMEM_ADMIN_PASSWORD to secure your instance.")
                else:
                    logging.info(f"Initial admin user '{admin_user}' created.")
                logging.info(f"Admin bootstrap: username='{admin_user}'")
            except Exception as e:
                logging.error(f"Failed to create initial admin user: {e}")

    # Track error count in ServerStats
    class ServerStats:
        def __init__(self, user_manager):
            self.start_time = time.time()
            self.total_requests = 0
            self.endpoint_counts = {}
            self.auth_success = 0
            self.auth_failure = 0
            self.error_count = 0
            self.user_manager = user_manager
            self.lock = Lock()
        def log_request(self, endpoint):
            with self.lock:
                self.total_requests += 1
                self.endpoint_counts[endpoint] = self.endpoint_counts.get(endpoint, 0) + 1
        def log_auth(self, success):
            with self.lock:
                if success:
                    self.auth_success += 1
                else:
                    self.auth_failure += 1
        def log_error(self):
            with self.lock:
                self.error_count += 1
        def get_stats(self):
            with self.lock:
                return {
                    "uptime_seconds": int(time.time() - self.start_time),
                    "total_requests": self.total_requests,
                    "endpoint_counts": dict(self.endpoint_counts),
                    "auth_success": self.auth_success,
                    "auth_failure": self.auth_failure,
                    "error_count": self.error_count,
                    "user_count": len(self.user_manager.list_users()),
                }

    stats = ServerStats(user_manager)

    # In-memory transaction tracking (tx_id -> info)
    open_transactions = {}

    @app.middleware("http")
    async def log_and_count_requests(request, call_next):
        endpoint = request.url.path
        stats.log_request(endpoint)
        logging.info(f"Request: {request.method} {endpoint}")
        response = await call_next(request)
        logging.info(f"Response: {response.status_code} {endpoint}")
        return response

    @app.on_event("startup")
    def startup_event():
        ensure_initial_admin()

    # Patch login to log auth stats
    @app.post("/token", response_model=Token)
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        success = user_manager.authenticate_user(form_data.username, form_data.password)
        stats.log_auth(success)
        if not success:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @app.post("/users/", dependencies=[Depends(require_admin)])
    def create_user(username: str, password: str, roles: Optional[List[str]] = None):
        try:
            user_manager.create_user(username, password, roles)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"msg": "User created"}

    @app.delete("/users/{username}", dependencies=[Depends(require_admin)])
    def delete_user(username: str):
        user_manager.delete_user(username)
        return {"msg": "User deleted"}

    @app.post("/users/{username}/roles", dependencies=[Depends(require_admin)])
    def assign_role(username: str, role: str):
        user_manager.assign_role(username, role)
        return {"msg": f"Role '{role}' assigned to {username}"}

    @app.get("/users/", response_model=List[str], dependencies=[Depends(require_admin)])
    def list_users():
        return user_manager.list_users()

    @app.get("/me", response_model=UserOut)
    def get_me(username: str = Depends(get_current_user)):
        return UserOut(username=username, roles=user_manager.get_user_roles(username))

    # Health check endpoint (public)
    @app.get("/health")
    def health_check():
        """Public health check endpoint. Returns status and triplestore connectivity."""
        try:
            adapter = get_triplestore_adapter_from_env()
            triplestore_ok = False
            try:
                triplestore_ok = adapter.test_connection()
            except Exception:
                triplestore_ok = False
            return {"status": "ok", "triplestore": "ok" if triplestore_ok else "unreachable"}
        except Exception:
            return {"status": "ok", "triplestore": "unconfigured"}

    # Metrics endpoint (admin-only)
    @app.get("/metrics", dependencies=[Depends(require_admin)])
    def metrics():
        """Admin-only metrics endpoint. Returns server stats as JSON."""
        return stats.get_stats()

    # Tasks endpoint (admin-only, stub)
    @app.get("/tasks", dependencies=[Depends(require_admin)])
    def tasks():
        """Admin-only tasks endpoint. Returns a list of background/async tasks (stub for now)."""
        # In the future, return real background/async tasks
        return {"tasks": []}

    def handle_adapter_error(e, operation: str = "operation"):
        stats.log_error()
        import tenacity
        # Check exception chain for RetryError
        exc = e
        while exc:
            if isinstance(exc, tenacity.RetryError):
                last_exc = getattr(exc, 'last_attempt', None)
                last_exc_msg = ''
                if last_exc and hasattr(last_exc, 'exception'):
                    last_exc_msg = last_exc.exception()
                return HTTPException(
                    status_code=503,
                    detail=f"{operation} failed after multiple retries due to a transient error: {last_exc_msg}. Please try again later."
                )
            exc = getattr(exc, '__cause__', None) or getattr(exc, '__context__', None)
        return HTTPException(status_code=500, detail=f"{operation} failed: {e}")

    # Patch all endpoints that interact with the adapter to use handle_adapter_error
    @app.get("/sparql")
    def sparql_get(query: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            if query.strip().lower().startswith("ask"):
                result = adapter.sparql_select(query)
            else:
                result = adapter.sparql_select(query)
            return {"results": result}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="SPARQL endpoint not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "SPARQL query")

    @app.get("/graphs/", dependencies=[Depends(require_admin)])
    def list_named_graphs():
        try:
            adapter = get_triplestore_adapter_from_env()
            return {"graphs": adapter.list_named_graphs()}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "List named graphs")

    @app.post("/graphs/", dependencies=[Depends(require_admin)])
    def create_named_graph(graph_uri: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.create_named_graph(graph_uri)
            return {"msg": f"Named graph {graph_uri} created."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Create named graph")

    @app.delete("/graphs/{graph_uri}", dependencies=[Depends(require_admin)])
    def delete_named_graph(graph_uri: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.delete_named_graph(graph_uri)
            return {"msg": f"Named graph {graph_uri} deleted."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Delete named graph")

    @app.post("/graphs/{graph_uri}/clear", dependencies=[Depends(require_admin)])
    def clear_named_graph(graph_uri: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.clear_named_graph(graph_uri)
            return {"msg": f"Named graph {graph_uri} cleared."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Clear named graph")

    @app.post("/graphs/{graph_uri}/add", dependencies=[Depends(require_admin)])
    def add_triples_to_named_graph(graph_uri: str, triples: list):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.add_triples_to_named_graph(graph_uri, triples)
            return {"msg": f"Triples added to named graph {graph_uri}."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Add triples to named graph")

    @app.post("/graphs/{graph_uri}/query", dependencies=[Depends(require_admin)])
    def query_named_graph(graph_uri: str, query: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            results = adapter.get_triples_from_named_graph(graph_uri, query)
            return {"results": results}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Named graph management not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Query named graph")

    @app.post("/transactions/begin", dependencies=[Depends(require_admin)])
    def begin_transaction():
        try:
            adapter = get_triplestore_adapter_from_env()
            tx_id = adapter.begin_transaction()
            open_transactions[tx_id] = {"status": "open"}
            return {"tx_id": tx_id}
        except NotImplementedError as nie:
            raise HTTPException(status_code=501, detail="Transactions not supported by this adapter.") from nie
        except Exception as e:
            # Check exception chain for NotImplementedError
            exc = e
            while exc:
                if isinstance(exc, NotImplementedError):
                    raise HTTPException(status_code=501, detail="Transactions not supported by this adapter.") from e
                exc = getattr(exc, '__cause__', None) or getattr(exc, '__context__', None)
            raise handle_adapter_error(e, "Begin transaction")

    @app.post("/transactions/{tx_id}/commit", dependencies=[Depends(require_admin)])
    def commit_transaction(tx_id: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.commit_transaction(tx_id)
            open_transactions.pop(tx_id, None)
            return {"msg": f"Transaction {tx_id} committed."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Transactions not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Commit transaction")

    @app.post("/transactions/{tx_id}/rollback", dependencies=[Depends(require_admin)])
    def rollback_transaction(tx_id: str):
        try:
            adapter = get_triplestore_adapter_from_env()
            adapter.rollback_transaction(tx_id)
            open_transactions.pop(tx_id, None)
            return {"msg": f"Transaction {tx_id} rolled back."}
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Transactions not supported by this adapter.")
        except Exception as e:
            raise handle_adapter_error(e, "Rollback transaction")

    @app.get("/server/stats", dependencies=[Depends(require_admin)])
    def get_server_stats():
        try:
            return stats.get_stats()
        except Exception as e:
            raise handle_adapter_error(e, "Get server stats")

    return app

# For CLI/server use
app = create_app() 
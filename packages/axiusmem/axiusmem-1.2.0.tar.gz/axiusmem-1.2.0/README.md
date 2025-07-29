# AxiusMEM

A W3C-compliant temporal knowledge graph library for AI agents.

[![PyPI version](https://badge.fury.io/py/axiusmem.svg)](https://badge.fury.io/py/axiusmem)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://readthedocs.org/projects/axiusmem/badge/?version=latest)](https://axiusmem.readthedocs.io/en/latest/)

## Features
- **Bi-temporal data model** (valid & transaction time)
- **Incremental and batch data ingestion**
- **Advanced querying** (SPARQL, temporal, semantic, full-text)
- **GraphDB integration** (connection pooling, repository management)
- **AI agent utilities** (context retrieval, memory management)
- **ORM/Mapper** (Python objects <-> RDF)
- **Extensive tests and Sphinx documentation**

## Installation

Install via pip:
```bash
pip install axiusmem
```

## Quick Start
```python
from axiusmem import AxiusMEM

mem = AxiusMEM()
mem.load_ontology('src/axiusmem/axiusmem_ontology.ttl')
mem.connect_graphdb()
# Add triples, query, manage agent memory, etc.
```

## Documentation
- [Sphinx Docs (HTML)](https://axiusmem.readthedocs.io/en/latest/)
- [Ontology (Turtle)](src/axiusmem/axiusmem_ontology.ttl)

> **Note:** For previous versions, see the version selector on the documentation site if available.

## Contributing
See [CONTRIBUTORS.md](CONTRIBUTORS.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).

## License
See [LICENSE](LICENSE).

## Community & Support
- Feedback, issues, and feature requests: [GitHub Issues](https://github.com/<your-org>/axiusmem/issues)
- Roadmap and discussions: [GitHub Discussions](https://github.com/<your-org>/axiusmem/discussions)

## Triplestore Configuration

AxiusMEM now supports generic configuration for multiple triplestores. Set the following environment variables:

- `TRIPLESTORE_TYPE`: The type of triplestore to use (`graphdb`, `jena`, etc.)
- `TRIPLESTORE_URL`: The base URL or host for the triplestore
- `TRIPLESTORE_USER`: Username for authentication (optional)
- `TRIPLESTORE_PASSWORD`: Password for authentication (optional)
- `TRIPLESTORE_REPOSITORY`: Repository or dataset name (if required by the backend)

Example for GraphDB:
```
TRIPLESTORE_TYPE=graphdb
TRIPLESTORE_URL=http://localhost:7200
TRIPLESTORE_USER=admin
TRIPLESTORE_PASSWORD=secret
TRIPLESTORE_REPOSITORY=myrepo
```

Example for Jena Fuseki:
```
TRIPLESTORE_TYPE=jena
TRIPLESTORE_URL=http://localhost:3030
TRIPLESTORE_USER=admin
TRIPLESTORE_PASSWORD=secret
TRIPLESTORE_REPOSITORY=Default
```

## Adapter Factory Usage

To obtain the correct adapter for your environment, use:

```python
from axiusmem.adapters.base import get_triplestore_adapter_from_env
adapter = get_triplestore_adapter_from_env()
```

This will automatically select and configure the appropriate adapter based on your environment variables.

# Jena Fuseki Adapter Usage

AxiusMEM now provides first-class support for Apache Jena Fuseki as a triplestore backend. Below are detailed setup and usage instructions.

## Environment Variable Setup

Set the following environment variables to configure AxiusMEM to use Jena Fuseki:

- `TRIPLESTORE_TYPE=jena`
- `TRIPLESTORE_URL=http://localhost:3030`  # Change host/port as needed
- `TRIPLESTORE_USER=admin`                 # Your Fuseki username (if required)
- `TRIPLESTORE_PASSWORD=yourpassword`      # Your Fuseki password (if required)
- `TRIPLESTORE_REPOSITORY=Default`         # The dataset name in your Fuseki server

You can set these in your shell, a `.env` file, or your environment manager.

## Example: .env File
```
TRIPLESTORE_TYPE=jena
TRIPLESTORE_URL=http://localhost:3030
TRIPLESTORE_USER=admin
TRIPLESTORE_PASSWORD=yourpassword
TRIPLESTORE_REPOSITORY=Default
```

## Using the Adapter in Code

```python
from axiusmem.adapters.base import get_triplestore_adapter_from_env
adapter = get_triplestore_adapter_from_env()

# Example: Run a SPARQL SELECT query
query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
results = adapter.sparql_select(query)
print(results)

# Example: Run a SPARQL UPDATE
update = "INSERT DATA { <http://example.org/s> <http://example.org/p> <http://example.org/o> }"
adapter.sparql_update(update)

# Example: Bulk load RDF data
adapter.bulk_load("mydata.ttl", rdf_format="text/turtle")

# Test the connection
if adapter.test_connection():
    print("Jena Fuseki connection successful!")
else:
    print("Failed to connect to Jena Fuseki.")
```

## Troubleshooting & Common Issues

- **Connection Refused:** Ensure your Jena Fuseki server is running and accessible at the URL you provided.
- **Authentication Errors:** Double-check your username and password. If authentication is not required, leave these variables blank.
- **Dataset Not Found:** Make sure the dataset name in `TRIPLESTORE_REPOSITORY` matches one configured in your Fuseki server.
- **SPARQL Errors:** Check your query syntax and ensure your dataset contains data.

## Verifying Jena Fuseki is Running
- Visit `http://localhost:3030` in your browser. You should see the Fuseki web interface.
- Use the Fuseki UI to create datasets, upload data, and test queries.

## Extending to Other Triplestores
While this documentation focuses on Jena Fuseki, AxiusMEM is designed to support other triplestores via the adapter factory. To use another backend, set `TRIPLESTORE_TYPE` and the relevant environment variables, and ensure the adapter is implemented.

## User and Role Management REST API

AxiusMEM now provides a REST API for user and role management, supporting admin and agent roles.

> **Note:** On first run, you may need to create an initial admin user. This can be done via a special CLI command or by using the `/users/` endpoint if no users exist. See the documentation for details.

### Features
- Admin endpoints: create/delete users, assign roles, list users
- Agent endpoints: authenticate, get own info/roles
- JWT-based authentication
- Only admins can manage users/roles

### Quick Start

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn bcrypt python-jose
   ```
2. Run the API server:
   ```bash
   uvicorn src.axiusmem.api:app --reload
   ```
3. Use the interactive docs at `http://localhost:8000/docs`

### Example Usage

- **Authenticate (get JWT):**
  ```bash
  curl -X POST "http://localhost:8000/token" -d 'username=admin&password=yourpassword' -H 'Content-Type: application/x-www-form-urlencoded'
  ```
- **Create user (admin only):**
  ```bash
  curl -X POST "http://localhost:8000/users/?username=alice&password=secret&roles=agent" -H "Authorization: Bearer <JWT>"
  ```
- **Get current user info:**
  ```bash
  curl -H "Authorization: Bearer <JWT>" http://localhost:8000/me
  ```

See the OpenAPI docs for all endpoints and details.

## Server Logs and Statistics

AxiusMEM now tracks server statistics and logs all API requests and responses. Admins can access live server stats via a dedicated endpoint.

### Features
- Logs every API request and response (method, path, status)
- Tracks uptime, total requests, per-endpoint counts, auth success/failure, and user count
- In-memory stats (reset on server restart)
- Admin-only `/server/stats` endpoint returns all stats as JSON

### Example: Get Server Stats

1. Authenticate as admin to get a JWT token:
   ```bash
   curl -X POST "http://localhost:8000/token" -d 'username=admin&password=yourpassword' -H 'Content-Type: application/x-www-form-urlencoded'
   # Response: { "access_token": "...", "token_type": "bearer" }
   ```
2. Query server stats:
   ```bash
   curl -H "Authorization: Bearer <JWT>" http://localhost:8000/server/stats
   # Example response:
   # {
   #   "uptime_seconds": 123,
   #   "total_requests": 42,
   #   "endpoint_counts": {"/token": 5, "/users/": 10, ...},
   #   "auth_success": 4,
   #   "auth_failure": 1,
   #   "user_count": 3
   # }
   ```

See logs in your console or log file for detailed request/response info.

## Transactions API

AxiusMEM now provides admin-only endpoints for triplestore transactions (begin, commit, rollback) if supported by the backend adapter.

### Endpoints
- `POST /transactions/begin` → returns a transaction ID (tx_id)
- `POST /transactions/{tx_id}/commit` → commits the transaction
- `POST /transactions/{tx_id}/rollback` → rolls back the transaction

**Note:** Not all adapters support transactions. If not supported, a 501 error is returned.

### Example Usage

1. Begin a transaction:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" http://localhost:8000/transactions/begin
   # Response: { "tx_id": "..." }
   ```
2. Commit the transaction:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" http://localhost:8000/transactions/<tx_id>/commit
   # Response: { "msg": "Transaction <tx_id> committed." }
   ```
3. Rollback the transaction:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" http://localhost:8000/transactions/<tx_id>/rollback
   # Response: { "msg": "Transaction <tx_id> rolled back." }
   ```

See the OpenAPI docs for details and adapter support.

## Named Graph Management API

AxiusMEM now provides admin-only endpoints for managing named graphs (if supported by the backend adapter).

### Endpoints
- `GET /graphs/` — list all named graphs
- `POST /graphs/` — create a named graph (body: `{"graph_uri": "..."}`)
- `DELETE /graphs/{graph_uri}` — delete a named graph
- `POST /graphs/{graph_uri}/clear` — clear all triples from a named graph
- `POST /graphs/{graph_uri}/add` — add triples to a named graph (body: `{"triples": [[s, p, o], ...]}`)
- `POST /graphs/{graph_uri}/query` — run a SPARQL query against a named graph (body: `{"query": "..."}`)

**Note:** Not all adapters support named graphs. If not supported, a 501 error is returned.

### Example Usage

1. List named graphs:
   ```bash
   curl -H "Authorization: Bearer <JWT>" http://localhost:8000/graphs/
   # Response: { "graphs": ["http://example.org/graph1", ...] }
   ```
2. Create a named graph:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
     -d '{"graph_uri": "http://example.org/graph1"}' http://localhost:8000/graphs/
   # Response: { "msg": "Named graph http://example.org/graph1 created." }
   ```
3. Add triples to a named graph:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
     -d '{"triples": [["http://example.org/s", "http://example.org/p", "o"]]}' \
     http://localhost:8000/graphs/http://example.org/graph1/add
   # Response: { "msg": "Triples added to named graph http://example.org/graph1." }
   ```
4. Query a named graph:
   ```bash
   curl -X POST -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
     -d '{"query": "?s ?p ?o"}' http://localhost:8000/graphs/http://example.org/graph1/query
   # Response: { "results": [...] }
   ```

See the OpenAPI docs for details and adapter support.

## Public SPARQL Endpoint

AxiusMEM provides a public `GET /sparql` endpoint for running SPARQL SELECT and ASK queries via HTTP GET.

### Endpoint
- `GET /sparql?query=...` — run a SPARQL SELECT or ASK query (no authentication required)

> **Security Note:** The public SPARQL endpoint is read-only (SELECT, ASK). For production deployments, consider rate limiting, authentication, or restricting access as appropriate.

### Example Usage

1. Run a SELECT query:
   ```bash
   curl "http://localhost:8000/sparql?query=SELECT%20*%20WHERE%20%7B%20?s%20?p%20?o%20%7D%20LIMIT%2010"
   # Response: { "results": [...] }
   ```
2. Run an ASK query:
   ```bash
   curl "http://localhost:8000/sparql?query=ASK%20%7B%20?s%20?p%20?o%20%7D"
   # Response: { "results": [...] }
   ```

**Note:** Only read-only queries (SELECT, ASK) are supported. For updates, use the admin API.

See the OpenAPI docs for details and adapter support.

## Automatic Retry Policy

AxiusMEM automatically retries triplestore and network operations to improve reliability in the face of transient errors.

- **What is retried:**
  - All network/triplestore operations (SPARQL queries, updates, transactions, named graph ops) in supported adapters (GraphDB, Jena, etc.)
  - Retries are triggered on network errors and HTTP 5xx errors
- **Retry strategy:**
  - Up to 3 attempts
  - Exponential backoff (starts at 0.5s, up to 8s)
  - All retries and errors are logged
- **User impact:**
  - Most transient network issues are handled automatically
  - If all retries fail, a clear error is returned to the API/user

**Note:** For persistent errors (e.g., authentication failure, invalid query), no retry is performed.

See the OpenAPI docs and logs for details.

## Error Handling and Retry Responses

AxiusMEM provides clear, user-facing error messages for all API endpoints. If an operation is retried and still fails, the API returns a 503 with a message indicating the retry attempts. For other errors, a 500 is returned with context.

### Example Error Responses

- **Transient error with retries (503):**
  ```json
  {
    "detail": "SPARQL query failed after multiple retries due to a transient error: HTTPConnectionPool(host='localhost', port=3030): Max retries exceeded. Please try again later."
  }
  ```
- **Generic server error (500):**
  ```json
  {
    "detail": "Add triples to named graph failed: Invalid triple format."
  }
  ```

**Note:** For persistent errors (e.g., invalid query, authentication failure), a 400 or 401/403 is returned as appropriate.

See the OpenAPI docs for details and troubleshooting.

## Health Check, Metrics, and Tasks Endpoints

AxiusMEM provides endpoints for health checks, server metrics, and background tasks.

### Endpoints
- `GET /health` (public): Returns API status and triplestore connectivity
- `GET /metrics` (admin-only): Returns server stats (uptime, request count, error count, etc.)
- `GET /tasks` (admin-only): Returns a list of background/async tasks (stub for now)

### Example Usage

1. Health check:
   ```bash
   curl http://localhost:8000/health
   # Response: { "status": "ok", "triplestore": "ok" }
   ```
2. Metrics (admin):
   ```bash
   curl -H "Authorization: Bearer <JWT>" http://localhost:8000/metrics
   # Response: { "uptime_seconds": 123, "total_requests": 42, ... }
   ```
3. Tasks (admin):
   ```bash
   curl -H "Authorization: Bearer <JWT>" http://localhost:8000/tasks
   # Response: { "tasks": [] }
   ```

See the OpenAPI docs for details and future task support. 

import rdflib
from rdflib import URIRef, Literal, Namespace, RDF
import bcrypt
import uuid
from typing import List, Optional

AXM = Namespace("https://axius.info/axiusmem/")

class UserManager:
    def __init__(self, graph: rdflib.Graph):
        self.graph = graph

    def _user_uri(self, username: str) -> URIRef:
        return AXM[f"user/{username}"]

    def _role_uri(self, role: str) -> URIRef:
        return AXM[f"role/{role}"]

    def create_user(self, username: str, password: str, roles: Optional[List[str]] = None) -> URIRef:
        user_uri = self._user_uri(username)
        if (user_uri, RDF.type, AXM.User) in self.graph:
            raise ValueError("User already exists")
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.graph.add((user_uri, RDF.type, AXM.User))
        self.graph.add((user_uri, AXM.hasPasswordHash, Literal(pw_hash)))
        if roles:
            for role in roles:
                role_uri = self._role_uri(role)
                self.graph.add((role_uri, RDF.type, AXM.Role))
                self.graph.add((user_uri, AXM.hasRole, role_uri))
        return user_uri

    def authenticate_user(self, username: str, password: str) -> bool:
        user_uri = self._user_uri(username)
        pw_hash = self.graph.value(user_uri, AXM.hasPasswordHash)
        if not pw_hash:
            return False
        return bcrypt.checkpw(password.encode(), str(pw_hash).encode())

    def assign_role(self, username: str, role: str):
        user_uri = self._user_uri(username)
        role_uri = self._role_uri(role)
        self.graph.add((role_uri, RDF.type, AXM.Role))
        self.graph.add((user_uri, AXM.hasRole, role_uri))

    def get_user_roles(self, username: str) -> List[str]:
        user_uri = self._user_uri(username)
        return [str(role).split("/")[-1] for role in self.graph.objects(user_uri, AXM.hasRole)]

    def list_users(self) -> List[str]:
        return [str(u).split("/")[-1] for u in self.graph.subjects(RDF.type, AXM.User)]

    def delete_user(self, username: str):
        user_uri = self._user_uri(username)
        for p, o in self.graph.predicate_objects(user_uri):
            self.graph.remove((user_uri, p, o))
        for s, p in self.graph.subject_predicates(user_uri):
            self.graph.remove((s, p, user_uri))
        self.graph.remove((user_uri, None, None))

    def is_admin(self, username: str) -> bool:
        return "admin" in self.get_user_roles(username)

    def is_agent(self, username: str) -> bool:
        return "agent" in self.get_user_roles(username) 
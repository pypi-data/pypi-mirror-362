import uuid

from sinkove.connector import connector
from sinkove.datasets.client import DatasetClient


class OrganizationClient:
    def __init__(self, conn: connector.Connector):
        self.conn = conn

    def list(self):
        response = self.conn.make_request(f"/v1/organizations", "GET")

        return [Organization(self.conn, org["id"], org["name"]) for org in response]

    def get(self, organization_id: uuid.UUID):
        response = self.conn.make_request(f"/v1/organizations/{organization_id}", "GET")

        return Organization(self.conn, response["id"], response["name"])


class Organization:
    def __init__(
        self,
        conn: connector.Connector,
        organization_id: uuid.UUID,
        organization_name: str,
    ):
        self._conn = conn
        self.id = organization_id
        self.organization_name = organization_name

    @property
    def datasets(self):
        return DatasetClient(self._conn, self.id)

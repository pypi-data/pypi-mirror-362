import uuid

from sinkove.connector import connector
from sinkove.organizations.client import Organization, OrganizationClient


class Client(Organization):
    def __init__(self, organization_id: uuid.UUID, api_key: str | None = None):
        conn = connector.Connector(api_key)
        organization_client = OrganizationClient(conn)
        organization = organization_client.get(organization_id)

        super().__init__(conn, organization.id, organization.organization_name)

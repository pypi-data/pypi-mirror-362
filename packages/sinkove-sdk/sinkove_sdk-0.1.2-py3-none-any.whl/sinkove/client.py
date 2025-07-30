import uuid

from sinkove.connector import connector
from sinkove.organizations.client import Organization, OrganizationClient


class Client(Organization):
    """
    A client class that extends the Organization class to manage organization-specific operations.

    Attributes:
        organization_id (uuid.UUID): The unique identifier for the organization.
        api_key (str | None): The API key for authentication, optional. Can be set through SINKOVE_API_KEY environment variable.
    """

    def __init__(self, organization_id: uuid.UUID, api_key: str | None = None):
        """
        Initializes a new Client instance.

        Args:
            organization_id (uuid.UUID): The unique identifier for the organization.
            api_key (str | None): The API key for authentication, optional.
        """
        conn = connector.Connector(api_key)
        organization_client = OrganizationClient(conn)
        organization = organization_client.get(organization_id)

        super().__init__(conn, organization.id, organization.organization_name)

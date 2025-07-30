import uuid

from sinkove.connector import connector
from sinkove.datasets.client import DatasetClient


class OrganizationClient:
    """
    A client for interacting with organizations via a connector.

    Attributes:
    - conn: A connector object for making requests.
    """

    def __init__(self, conn: connector.Connector):
        """
        Initialize an OrganizationClient instance.

        Parameters:
        - conn: A connector object for making requests.
        """
        self.conn = conn

    def list(self):
        """
        List all organizations.

        Returns:
        - A list of Organization objects representing each organization.
        """
        response = self.conn.make_request(f"/v1/organizations", "GET")
        return [Organization(self.conn, org["id"], org["name"]) for org in response]

    def get(self, organization_id: uuid.UUID):
        """
        Get details of a specific organization.

        Parameters:
        - organization_id: The unique identifier of the organization.

        Returns:
        - An Organization object representing the specified organization.
        """
        response = self.conn.make_request(f"/v1/organizations/{organization_id}", "GET")
        return Organization(self.conn, response["id"], response["name"])


class Organization:
    """
    A class representing an organization with associated datasets.

    Attributes:
    - _conn: A connector object for making requests.
    - id: The unique identifier of the organization.
    - organization_name: The name of the organization.
    """

    def __init__(
        self,
        conn: connector.Connector,
        organization_id: uuid.UUID,
        organization_name: str,
    ):
        """
        Initialize an Organization instance.

        Parameters:
        - conn: A connector object for making requests.
        - organization_id: The unique identifier of the organization.
        - organization_name: The name of the organization.
        """
        self._conn = conn
        self.id = organization_id
        self.organization_name = organization_name

    @property
    def datasets(self):
        """
        Access the datasets associated with the organization.

        Returns:
        - A DatasetClient object for interacting with the organization's datasets.
        """
        return DatasetClient(self._conn, self.id)

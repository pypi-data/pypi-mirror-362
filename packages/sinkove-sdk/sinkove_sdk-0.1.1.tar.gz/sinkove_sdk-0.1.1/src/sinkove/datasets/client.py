import os
import typing
import requests
import uuid
import time

from sinkove.connector import connector
from sinkove.datasets import metadata


class Dataset:
    def __init__(
        self,
        conn: connector.Connector,
        id: uuid.UUID,
        model_id: uuid.UUID,
        organization_id: uuid.UUID,
        owner_id: str,
        num_samples: int,
        args: typing.Any,
        created_at: str,
        updated_at: str,
        metadata: typing.Optional[metadata.Metadata],
    ):
        self._conn = conn
        self.id = id
        self.model_id = model_id
        self.organization_id = organization_id
        self.owner_id = owner_id
        self.num_samples = num_samples
        self.args = args
        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata

    @property
    def finished(self):
        return self.state not in ["PENDING", "STARTED"]

    @property
    def ready(self):
        self._reload_metadata()
        return self.state == "READY"

    @property
    def state(self) -> metadata.State:
        if self.metadata is None:
            return "UNKNOWN"

        return self.metadata.state

    def _reload_metadata(self):
        response = self._conn.make_request(
            f"/v1/organizations/{self.organization_id}/datasets/{self.id}",
            "GET",
        )

        self.metadata = _parse_metadata(response.get("metadata"))

    def download(
        self,
        output_file: str,
        strategy: typing.Literal["fail", "skip", "replace"] = "fail",
        wait: bool = False,
        timeout: typing.Optional[int] = None,
    ):
        # Check if the file already exists
        if os.path.exists(output_file):
            if strategy == "fail":
                raise Exception(
                    f"The file '{output_file}' already exists and the strategy is set to 'fail'."
                )
            elif strategy == "skip":
                # The file 'output_file' already exists and the strategy is set to 'skip'.
                return
            elif strategy == "replace":
                # User wants to override the existing file if it already exists
                pass

        if wait:
            self.wait(timeout)

        response = self._conn.make_request(
            f"/v1/organizations/{self.organization_id}/datasets/{self.id}/urls/download",
            "GET",
        )

        if "URL" not in response:
            raise Exception("Failed to retrieve download URL")

        download_url = response["URL"]

        # Make a request to the presigned URL
        download_response = requests.request("GET", download_url)
        if download_response.status_code != 200:
            raise Exception(
                f"Failed to download dataset, status code: {download_response.status_code}"
            )

        with open(output_file, "wb") as f:
            f.write(download_response.content)

    def wait(self, timeout: typing.Optional[int] = None):
        start_time = time.time()
        while not self.finished:
            if timeout is not None and (time.time() - start_time) > timeout:
                raise TimeoutError("Waiting for dataset processing timed out.")

            time.sleep(1)

        if not self.ready:
            raise Exception(
                f"Failed to process dataset. The dataset state is '{self.state}'."
            )


class DatasetClient:
    def __init__(self, conn: connector.Connector, organization_id: uuid.UUID):
        self.conn = conn
        self.organization_id = organization_id

    def list(self):
        response = self.conn.make_request(
            f"/v1/organizations/{self.organization_id}/datasets", "GET"
        )

        return [self._parse_dataset(dataset) for dataset in response]

    def create(
        self, model_id: uuid.UUID, num_samples: int, args: typing.Dict[str, typing.Any]
    ):
        """
        Create a new dataset generation request.

        Parameters:
        - model_id: The ID of the model to use.
        - num_samples: The number of samples to generate.
        - args: A list of arguments required by the model.

        Returns:
        - The response from the dataset creation request.
        """
        payload = {"modelId": str(model_id), "numSamples": num_samples, "args": args}
        response = self.conn.make_request(
            f"/v1/organizations/{self.organization_id}/datasets", "POST", data=payload
        )

        return self._parse_dataset(response)

    def _parse_dataset(self, response: dict) -> Dataset:
        return Dataset(
            conn=self.conn,
            id=uuid.UUID(response["id"]),
            model_id=uuid.UUID(response["modelId"]),
            organization_id=uuid.UUID(response["organizationId"]),
            owner_id=response["ownerId"],
            num_samples=response["numSamples"],
            args=response["args"],
            created_at=response["createdAt"],
            updated_at=response["updatedAt"],
            metadata=_parse_metadata(response.get("metadata")),
        )

    def get(self, dataset_id: uuid.UUID) -> Dataset:
        response = self.conn.make_request(
            f"/v1/organizations/{self.organization_id}/datasets/{dataset_id}", "GET"
        )
        return self._parse_dataset(response)


def _parse_metadata(
    raw_metadata: typing.Optional[typing.Dict[str, typing.Any]],
) -> typing.Optional[metadata.Metadata]:
    if raw_metadata is None:
        return None

    return metadata.Metadata(
        id=uuid.UUID(raw_metadata["id"]),
        state=raw_metadata["state"],
        progress=raw_metadata["progress"],
        size=raw_metadata["size"],
        started_at=(
            raw_metadata["startedAt"] if raw_metadata.get("startedAt") else None
        ),
        finished_at=(
            raw_metadata["finishedAt"] if raw_metadata.get("finishedAt") else None
        ),
    )

import json
from dataclasses import asdict

from pyakri_de_utils.rest.rest_client import RestClient
from pyakri_de_utils.rest.utils import default_rest_client
from sink_writer_filters.models import PipelinePartitionCreateRequest


class DSPRestClient:
    def __init__(
        self,
        base_url: str,
        headers: dict,
    ):
        self._base_url = base_url.rstrip("/")
        self._headers = headers
        self._headers["Content-type"] = "application/json"
        self._rest_client: RestClient = default_rest_client()

    def update_dataset_partition(
        self,
        partition_id: str,
        session_id: str,
        pipeline_id: str,
        dataset_id: str,
        pipeline_partition_create_request: PipelinePartitionCreateRequest,
    ):
        path = (
            f"/ds/datasets/{dataset_id}/pipelines/{pipeline_id}/sessions/{session_id}/partitions/"
            f"{partition_id}"
        )
        endpoint = f"{self._base_url}{path}"
        payload = json.dumps(asdict(pipeline_partition_create_request))
        self._rest_client.exec_request(
            url=endpoint,
            body=payload,
            headers=self._headers,
            method="put",
        )

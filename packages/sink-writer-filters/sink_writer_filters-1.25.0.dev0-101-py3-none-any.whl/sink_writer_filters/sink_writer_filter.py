# flake8: noqa  E501
from abc import abstractmethod
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import akridata_akrimanager_v2 as am
from pyakri_de_utils.common_utils import get_values_in_batches
from pyakri_de_utils.file_utils import get_input_files_dir
from pyakri_de_utils.store_utils import upload_file_to_data_store

from .constants import Constants
from .dsp_rest_client import DSPRestClient
from .models import ApiManager, RegionIngestOutputPath
from .models import DataIngestOutputPath
from .models import PartitionOutputPath
from .models import PartitionOutputs
from .models import PipelinePartitionCreateRequest
from .models import RegionOutputPath
from .models import SinkWriterFilterInput


class SinkWriterFilter:
    def __init__(
        self,
        filter_input: SinkWriterFilterInput,
        api_manager: ApiManager,
        ccs_api_batch_size: int = Constants.CCS_API_BATCH_SIZE,
        import_features: bool = False,
    ):
        self._api_manager = api_manager
        self._filter_input = filter_input
        self._ccs_batch_size = ccs_api_batch_size
        self._import_features = import_features
        # TODO: to be removed after amv2 migrated to the pydantic-v2
        self._dsp_rest_client = DSPRestClient(
            base_url=api_manager.dsp_dataset_api.api_client.configuration.host,
            headers=api_manager.dsp_dataset_api.api_client.default_headers,
        )

    def run_from_input_dir(
        self,
        blobs_dir: str,
        thumbnail_dir: Optional[str] = None,
        full: Optional[DataIngestOutputPath] = None,
        patch: Optional[DataIngestOutputPath] = None,
        region: Optional[RegionIngestOutputPath] = None,
    ):
        data_dir_to_file_type_list = [
            (blobs_dir, am.DatastoreFileType.BLOBS),
            (thumbnail_dir, am.DatastoreFileType.THUMBNAIL),
        ]

        # Check whether all output path are empty or not
        if all(not output for output in [full, patch, region]):
            raise ValueError("File paths are missing for some file type!")

        if full:
            data_dir_to_file_type_list += [
                (full.coreset_dir, am.DatastoreFileType.FULL_CORESET),
                (full.sketch_dir, am.DatastoreFileType.FULL_SKETCH),
                (full.projections_dir, am.DatastoreFileType.FULL_PROJECTIONS),
            ]

        if patch:
            data_dir_to_file_type_list += [
                (patch.coreset_dir, am.DatastoreFileType.PATCH_CORESET),
                (patch.sketch_dir, am.DatastoreFileType.PATCH_SKETCH),
                (patch.projections_dir, am.DatastoreFileType.PATCH_PROJECTIONS),
            ]

        if region:
            data_dir_to_file_type_list += [
                (region.coreset_dir, am.DatastoreFileType.REGION_CORESET),
                (region.sketch_dir, am.DatastoreFileType.REGION_SKETCH),
                (region.projections_dir, am.DatastoreFileType.REGION_PROJECTIONS),
                (region.region_meta, am.DatastoreFileType.REGION_META),
            ]

        files_path_map = {}
        for data_dir, file_type in data_dir_to_file_type_list:
            # In import features, the thumbnail directory will be null,
            if not data_dir:
                files_path_map[file_type] = None
            else:
                arrow_files = get_input_files_dir(directory=data_dir)
                files_path_map[file_type] = str(arrow_files[0])

        self._run_from_files_map(files_map=files_path_map)

    def _get_partition_details(self) -> Tuple[int, int, str]:
        partition_start = self._filter_input.partition_start
        partition_end = self._filter_input.partition_end
        partition_id = f"{partition_start}_{partition_end}"
        return partition_start, partition_end, partition_id

    def _run_from_files_map(self, files_map: Dict[am.DatastoreFileType, Optional[str]]):
        (
            partition_start,
            partition_end,
            partition_id,
        ) = self._get_partition_details()

        store_path_map = self._store_files_to_data_store(
            partition_id=partition_id, files_map=files_map
        )

        self._update_dataset_partition(
            partition_id=partition_id,
            partition_start=partition_start,
            partition_end=partition_end,
            store_path_map=store_path_map,
        )

        self._insert_entries_to_pipeline_tables(
            store_path_map=store_path_map,
            partition_start=partition_start,
            partition_end=partition_end,
        )

    def _store_files_to_data_store(
        self,
        partition_id: str,
        files_map: Dict[am.DatastoreFileType, Optional[str]],
    ):
        # Filter file types for pre-signed url
        files_types_for_presigned_url = [
            stype for stype, spath in files_map.items() if spath
        ]

        list_pre_signed_response: am.ListPreSignedUrlResponseWithOperation = (
            self._api_manager.workflow_api.generate_presigned_url_for_workflow_files(
                dataset_id=self._filter_input.dataset_id,
                file_types=files_types_for_presigned_url,
                partition_id=partition_id,
                session_id=self._filter_input.session_id,
            )
        )  # type: ignore

        store_path_map = {}
        # Store file metadata to sink store using pre-signed url
        assert list_pre_signed_response.presignedurls is not None
        for pre_signed_url_resp in list_pre_signed_response.presignedurls:
            pre_signed_url_resp: am.GetPreSignedUrlResponseWithOperation = (
                pre_signed_url_resp
            )
            fields = pre_signed_url_resp.fields
            assert fields is not None
            store_path_with_dataset_id = fields.get("key")
            if not store_path_with_dataset_id:
                raise ValueError("Key is not present in the presigned url resp")

            store_path_without_dataset_id = "/".join(
                store_path_with_dataset_id.split("/")[1:]
            )

            upload_file_to_data_store(
                file_path=files_map[pre_signed_url_resp.file_type],
                presigned_url=pre_signed_url_resp.url,
                fields=fields,
            )

            store_path_map[
                pre_signed_url_resp.file_type
            ] = store_path_without_dataset_id

        return store_path_map

    def _update_dataset_partition(
        self,
        partition_id: str,
        partition_start: int,
        partition_end: int,
        store_path_map: Dict[am.DatastoreFileType, Optional[str]],
    ):
        # Dummy thumnail directory for import features
        thumbnail_blobs = [self._filter_input.pipeline_id]
        if store_path_map.get(am.DatastoreFileType.THUMBNAIL):
            thumbnail_blobs = [store_path_map[am.DatastoreFileType.THUMBNAIL]]

        full_output_path: Optional[PartitionOutputPath] = None
        if am.DatastoreFileType.FULL_PROJECTIONS in store_path_map:
            full_output_path = PartitionOutputPath(
                coreset=store_path_map[am.DatastoreFileType.FULL_CORESET],
                projection=store_path_map[am.DatastoreFileType.FULL_PROJECTIONS],
                sketch=store_path_map[am.DatastoreFileType.FULL_SKETCH],
            )

        patch_output_path: Optional[PartitionOutputPath] = None
        if am.DatastoreFileType.PATCH_PROJECTIONS in store_path_map:
            patch_output_path = PartitionOutputPath(
                coreset=store_path_map[am.DatastoreFileType.PATCH_CORESET],
                projection=store_path_map[am.DatastoreFileType.PATCH_PROJECTIONS],
                sketch=store_path_map[am.DatastoreFileType.PATCH_SKETCH],
            )

        region_output_path: Optional[RegionOutputPath] = None
        if am.DatastoreFileType.REGION_PROJECTIONS in store_path_map:
            region_output_path = RegionOutputPath(
                coreset=store_path_map[am.DatastoreFileType.REGION_CORESET],
                projection=store_path_map[am.DatastoreFileType.REGION_PROJECTIONS],
                sketch=store_path_map[am.DatastoreFileType.REGION_SKETCH],
                region_meta=store_path_map[am.DatastoreFileType.REGION_META],
            )

        partition_outputs = PartitionOutputs(
            region=region_output_path,
            patch=patch_output_path,
            full=full_output_path,
        )

        partition_create_request = PipelinePartitionCreateRequest(
            partition_end=partition_end,
            partition_start=partition_start,
            blobs=[store_path_map[am.DatastoreFileType.BLOBS]],
            thumbnails=thumbnail_blobs,
            start_frame_indices=[self._get_start_frame_indices()],
            img_end_indices=[self._get_end_frame_indices()],
            outputs=partition_outputs,
        )
        self._dsp_rest_client.update_dataset_partition(
            partition_id=partition_id,
            session_id=self._filter_input.session_id,
            pipeline_id=self._filter_input.pipeline_id,
            dataset_id=self._filter_input.dataset_id,
            pipeline_partition_create_request=partition_create_request,
        )

    def _insert_entries_to_pipeline_tables(
        self,
        store_path_map: Dict[Union[am.DatastoreFileType, str], str],
        partition_start: int,
        partition_end: int,
    ):
        blobs_table_insert_values: List[List[Union[int, str]]] = [
            [
                partition_start,
                partition_end,
                self._filter_input.workflow_id,
                self._filter_input.session_id,
                store_path_map[am.DatastoreFileType.BLOBS],
            ]
        ]

        summary_table_insert_values: List[List[Union[str, int]]] = [
            [
                partition_start,
                partition_end,
                self._filter_input.workflow_id,
                self._filter_input.session_id,
                store_path_map.get(am.DatastoreFileType.THUMBNAIL),
                store_path_map.get(am.DatastoreFileType.FULL_CORESET),
                store_path_map.get(am.DatastoreFileType.FULL_PROJECTIONS),
                store_path_map.get(am.DatastoreFileType.FULL_SKETCH),
                store_path_map.get(am.DatastoreFileType.PATCH_CORESET),
                store_path_map.get(am.DatastoreFileType.PATCH_PROJECTIONS),
                store_path_map.get(am.DatastoreFileType.PATCH_SKETCH),
                store_path_map.get(am.DatastoreFileType.REGION_CORESET),
                store_path_map.get(am.DatastoreFileType.REGION_PROJECTIONS),
                store_path_map.get(am.DatastoreFileType.REGION_SKETCH),
                store_path_map.get(am.DatastoreFileType.REGION_META),
            ]
        ]

        # populate insert values for primary table
        primary_table_insert_values: List[
            List[Union[int, str, datetime]]
        ] = self._get_primary_table_values(
            partition_start=partition_start,
            partition_end=partition_end,
            filter_input=self._filter_input,
        )

        tables_info = self._filter_input.tables_info
        # Insert entries to db
        for abs_table_name, columns, values in [
            (
                tables_info.blob_abs_table,
                Constants.BLOB_TABLE_COLUMNS,
                blobs_table_insert_values,
            ),
            (
                tables_info.summary_abs_table,
                Constants.SUMMARY_TABLE_COLUMNS,
                summary_table_insert_values,
            ),
            (
                tables_info.primary_abs_table,
                self._get_primary_table_columns(),
                primary_table_insert_values,
            ),
        ]:
            if values and len(columns) != len(values[0]):
                raise ValueError("Value length differs from column length!")

            for values_batch in get_values_in_batches(
                values=values, batch_size=self._ccs_batch_size
            ):
                self._api_manager.ccs_api.insert_data_in_catalog_table(
                    am.InsertCatalogData(
                        dataset_id=self._filter_input.dataset_id,
                        columns=columns,
                        values=values_batch,
                        abs_table_name=abs_table_name,
                    )
                )

    @staticmethod
    def _validate_primary_table_values(field: Optional[Any], field_name: str):
        if not field:
            raise ValueError(
                f"Field {field_name} should not be empty for video datasets"
            )

    @staticmethod
    @abstractmethod
    def _get_primary_table_columns():
        pass

    @abstractmethod
    def _get_primary_table_values(
        self,
        partition_start: int,
        partition_end: int,
        filter_input: SinkWriterFilterInput,
    ):
        pass

    @abstractmethod
    def _get_start_frame_indices(self) -> int:
        pass

    @abstractmethod
    def _get_end_frame_indices(self) -> int:
        pass

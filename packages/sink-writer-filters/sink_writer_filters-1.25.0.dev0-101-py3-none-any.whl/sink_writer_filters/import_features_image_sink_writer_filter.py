from datetime import datetime
from typing import List
from typing import Union

from .constants import Constants
from .models import SinkWriterFilterInput
from .sink_writer_filter import SinkWriterFilter


class ImportFeaturesImageSinkWriterFilter(SinkWriterFilter):
    @staticmethod
    def _get_primary_table_columns():
        return Constants.IMPORT_FEATURES_PRIMARY_TABLE_IMAGE_COLUMNS

    def _get_primary_table_values(
        self,
        partition_start: int,
        partition_end: int,
        filter_input: SinkWriterFilterInput,
    ):
        import_identifier = self._filter_input.import_identifier

        primary_table_insert_values: List[List[Union[int, str]]] = []
        for file_info in self._filter_input.file_metadata_list:
            primary_table_value = [
                partition_start,
                partition_end,
                self._filter_input.session_id,
                file_info.file_path,
                file_info.frame_idx_in_file,
                file_info.frame_idx_in_blob,
                file_info.blob_idx_in_partition,
                import_identifier,
                datetime.now(),
            ]
            primary_table_insert_values.append(primary_table_value)

        return primary_table_insert_values

    def _get_start_frame_indices(self) -> int:
        return 0

    def _get_end_frame_indices(self) -> int:
        return len(self._filter_input.file_metadata_list) - 1

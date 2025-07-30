from datetime import datetime
from typing import List, Union

from .constants import Constants
from .models import SinkWriterFilterInput
from .sink_writer_filter import SinkWriterFilter


class ImageSinkWriterFilter(SinkWriterFilter):
    @staticmethod
    def _get_primary_table_columns():
        return Constants.PRIMARY_TABLE_IMAGE_COLUMNS

    def _get_primary_table_values(
        self,
        partition_start: int,
        partition_end: int,
        filter_input: SinkWriterFilterInput,
    ):
        primary_table_insert_values: List[List[Union[int, str, datetime]]] = []
        for file_info in filter_input.file_metadata_list:
            primary_table_value = [
                partition_start,
                partition_end,
                self._filter_input.workflow_id,
                self._filter_input.session_id,
                file_info.frame_idx_in_blob,
                file_info.blob_idx_in_partition,
                file_info.file_path,
                datetime.now(),
                file_info.file_id,
                file_info.frame_idx_in_file,
                file_info.file_name,
                file_info.total_frames_in_file,
                file_info.frame_height,
                file_info.frame_width,
            ]

            primary_table_insert_values.append(primary_table_value)

        return primary_table_insert_values

    def _get_start_frame_indices(self) -> int:
        return 0

    def _get_end_frame_indices(self) -> int:
        return len(self._filter_input.file_metadata_list) - 1

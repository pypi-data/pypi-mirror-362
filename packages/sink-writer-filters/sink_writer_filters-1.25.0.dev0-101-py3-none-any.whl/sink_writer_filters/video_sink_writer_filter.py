from datetime import datetime
from typing import List, Union

from .constants import Constants
from .models import SinkWriterFilterInput
from .sink_writer_filter import SinkWriterFilter


class VideoSinkWriterFilter(SinkWriterFilter):
    @staticmethod
    def _get_primary_table_columns():
        return Constants.PRIMARY_TABLE_VIDEO_COLUMNS

    def _get_primary_table_values(
        self,
        partition_start: int,
        partition_end: int,
        filter_input: SinkWriterFilterInput,
    ):
        primary_table_insert_values: List[List[Union[int, str, datetime]]] = []
        for file_info in filter_input.file_metadata_list:
            self._validate_primary_table_values(file_info.native_fps, "native_fps")

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
                file_info.native_fps,
            ]

            primary_table_insert_values.append(primary_table_value)

        return primary_table_insert_values

    def _get_start_frame_indices(self) -> int:
        file_metadata_list = self._filter_input.file_metadata_list
        first_frame = file_metadata_list[0]
        return first_frame.frame_idx_in_file

    def _get_end_frame_indices(self) -> int:
        file_metadata_list = self._filter_input.file_metadata_list
        last_frame = file_metadata_list[-1]
        return last_frame.frame_idx_in_file

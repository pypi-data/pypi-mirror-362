from .enums import DataType
from .image_sink_writer_filter import (
    ImageSinkWriterFilter,
)
from .import_features_image_sink_writer_filter import (
    ImportFeaturesImageSinkWriterFilter,
)
from .import_features_video_sink_writer_filter import (
    ImportFeaturesVideoSinkWriterFilter,
)
from .models import ApiManager, SinkWriterFilterInput
from .video_sink_writer_filter import VideoSinkWriterFilter


class SinkWriterFilterFactory:
    @staticmethod
    def get_sink_writer(
        filter_input: SinkWriterFilterInput,
        api_manager: ApiManager,
        data_type: DataType.IMAGE,
    ):
        params = {
            "filter_input": filter_input,
            "api_manager": api_manager,
        }

        if data_type == DataType.IMAGE:
            return ImageSinkWriterFilter(**params)
        elif data_type == DataType.VIDEO:
            return VideoSinkWriterFilter(**params)

        raise ValueError(f"Sink writer for data type {data_type} " f"is not defined!")

    @staticmethod
    def get_import_features_sink_writer(
        filter_input: SinkWriterFilterInput,
        api_manager: ApiManager,
        data_type: DataType.IMAGE,
    ):
        params = {
            "filter_input": filter_input,
            "api_manager": api_manager,
            "import_features": True,
        }
        if data_type == DataType.IMAGE:
            return ImportFeaturesImageSinkWriterFilter(**params)
        elif data_type == DataType.VIDEO:
            return ImportFeaturesVideoSinkWriterFilter(**params)

        raise ValueError(
            f"Import Features Sink writer for data type {data_type} " f"is not defined!"
        )

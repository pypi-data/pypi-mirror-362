from dataclasses import dataclass
from typing import List
from typing import Optional

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp


@dataclass
class ApiManager:
    workflow_api: am.WorkflowsApi
    dsp_dataset_api: dsp.DatasetApi
    ccs_api: am.CcsApi


@dataclass
class BlobBlobFileInfo:
    frame_idx_in_blob: int
    blob_idx_in_partition: int


@dataclass
class BaseFileInfo(BlobBlobFileInfo):
    file_path: str
    frame_idx_in_file: int


@dataclass
class FileInfo(BaseFileInfo):
    file_id: int
    file_name: str
    frame_height: int
    frame_width: int
    total_frames_in_file: int

    native_fps: Optional[float]


@dataclass
class SinkTablesInfo:
    """Class for table info for sink writer filter."""

    primary_abs_table: str
    summary_abs_table: str
    blob_abs_table: str


@dataclass
class SinkWriterFilterInput:
    """Class for input params for sink writer filter."""

    file_metadata_list: List[BaseFileInfo]
    dataset_id: str
    workflow_id: str
    session_id: str
    pipeline_id: str
    partition_start: int
    partition_end: int
    tables_info: SinkTablesInfo
    import_identifier: Optional[str] = None


@dataclass
class DataIngestOutputPath:
    coreset_dir: str
    sketch_dir: str
    projections_dir: str


@dataclass
class RegionIngestOutputPath(DataIngestOutputPath):
    region_meta: str


# DSP related models
@dataclass
class PartitionOutputPath:
    projection: str
    sketch: str
    coreset: str


@dataclass
class RegionOutputPath(PartitionOutputPath):
    region_meta: str


@dataclass
class PartitionOutputs:
    full: Optional[PartitionOutputPath] = None
    patch: Optional[PartitionOutputPath] = None
    region: Optional[RegionOutputPath] = None


@dataclass
class PipelinePartitionCreateRequest:
    partition_start: int
    partition_end: int
    blobs: List[str]
    outputs: PartitionOutputs
    img_end_indices: List[int]
    start_frame_indices: Optional[List[int]] = None
    thumbnails: Optional[List[str]] = None

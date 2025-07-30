import akridata_akrimanager_v2 as am


class Constants:
    CCS_API_BATCH_SIZE = 1000

    BLOB_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "blob_id",
    ]
    SUMMARY_TABLE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "thumbnail",
        "full_coreset",
        "full_projections",
        "full_sketch",
        "patch_coreset",
        "patch_projections",
        "patch_sketch",
        "region_coreset",
        "region_projections",
        "region_sketch",
        "region_meta",
    ]
    PRIMARY_TABLE_IMAGE_COLUMNS = [
        "partition_start",
        "partition_end",
        "workflow_id",
        "session_id",
        "frame_idx_in_blob",
        "blob_idx_in_partition",
        "file_path",
        "timestamp",
        "file_id",
        "frame_idx_in_file",
        "file_name",
        "total_frames_in_file",
        "frame_height",
        "frame_width",
    ]

    PRIMARY_TABLE_VIDEO_COLUMNS = PRIMARY_TABLE_IMAGE_COLUMNS + [
        "native_fps",
    ]

    IMPORT_FEATURES_PRIMARY_TABLE_IMAGE_COLUMNS = [
        "partition_start",
        "partition_end",
        "session_id",
        "file_path",
        "frame_idx_in_file",
        "frame_idx_in_blob",
        "blob_idx_in_partition",
        "import_identifier",
        "akd_import_ts",
    ]

    IMPORT_FEATURES_PRIMARY_TABLE_VIDEO_COLUMNS = (
        IMPORT_FEATURES_PRIMARY_TABLE_IMAGE_COLUMNS
    )

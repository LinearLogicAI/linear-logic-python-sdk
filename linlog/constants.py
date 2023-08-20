import os


BASE_URL = 'https://linearlogic.ai/api/v1'

MODULE_ROOT = os.path.expanduser("~") + os.sep + ".linear-logic"


class ProjectType:
    Image = "image"
    Categorisation = "categorisation"
    Geospatial = "geospatial"

    @classmethod
    def get_all(self):
        return [self.Image, self.Geospatial, self.Categorisation]


class TaskType:
    Image = "image"
    Categorisation = "categorisation"
    Geospatial = "geospatial"

    @classmethod
    def get_all(self):
        return [self.Image, self.Geospatial, self.Categorisation]


class AnnotationType:
    BoundingBox = 'bounding-box'
    Polygon = 'polygon'
    Point = 'point'
    Line = 'line'

    @classmethod
    def get_all(self):
        return [self.BoundingBox, self.Polygon, self.Point, self.Line]


IN_MEMORY_PREFIX = 'inmem_'

ORGANISATION_ID_KEY = 'id'
ORGANISATION_NAME_KEY = 'name'
ORGANISATION_SUBSCRIPTION_KEY = 'subscription'
ORGANISATION_MEMBERS_KEY = 'members'

PROJECT_ID_KEY = 'id'
PROJECT_CREATED_DATE_KEY = 'created_date'
PROJECT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
PROJECT_TITLE_KEY = 'title'
PROJECT_TYPE_KEY = 'type'
PROJECT_OBJECTS_TO_ANNOTATE_KEY = 'objects_to_annotate'
PROJECT_ITEM_COUNT_KEY = 'item_count'
PROJECT_COMPLETED_TASKS_KEY = 'completed_tasks'
PROJECT_ANNOTATION_ATTRIBUTES_KEY = 'annotation_attributes'
PROJECT_PARAM_HISTORY_KEY = 'param_history'

PROJECT_ATTRIBUTE_ID_KEY = 'id'
PROJECT_ATTRIBUTE_KEY_KEY = 'key'
PROJECT_ATTRIBUTE_TYPE_KEY = 'attribute_type'
PROJECT_ATTRIBUTE_IS_GLOBAL_KEY = 'is_global'
PROJECT_ATTRIBUTE_ALLOW_MULTIPLE_KEY = 'allow_multiple'
PROJECT_ATTRIBUTE_OPTIONS_KEY = 'options'

OBJECT_TO_ANNOTATE_ID_KEY = 'id'
OBJECT_TO_ANNOTATE_NAME_KEY = 'name'
OBJECT_TO_ANNOTATE_DISPLAY_NAME_KEY = 'display_name'
OBJECT_TO_ANNOTATE_TASK_TYPE_KEY = 'task_type'
OBJECT_TO_ANNOTATE_COLOUR_R_KEY = 'colour_r'
OBJECT_TO_ANNOTATE_COLOUR_G_KEY = 'colour_g'
OBJECT_TO_ANNOTATE_COLOUR_B_KEY = 'colour_b'
OBJECT_TO_ANNOTATE_RAW_COLOUR_CODE_KEY = 'colour_code'

DATASET_ID_KEY = 'id'
DATASET_CREATED_DATE_KEY = 'created_date'
DATASET_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATASET_NAME_KEY = 'name'
DATASET_TYPE_KEY = 'type'
DATASET_LABELS_KEY = 'labels'
DATASET_ITEM_COUNT_KEY = 'item_count'
DATASET_OBJECT_COUNT_KEY = 'object_count'

DATASET_LABEL_NAME_KEY = 'label'
DATASET_LABEL_TYPE_KEY = 'type'

TASK_ID_KEY = 'id'
TASK_GLOBAL_KEY_KEY = 'global_key'
TASK_FILENAME_KEY = 'filename'
TASK_COMPLETE_KEY = 'complete'
TASK_REJECTED_KEY = 'rejected'
TASK_WORKFLOW_STAGE_KEY = 'workflow_stage'
TASK_ERRORS_KEY = 'errors'
TASK_IS_ERROR_KEY = 'error'
TASK_PROCESSING_KEY = 'processing'
TASK_WARNINGS_KEY = 'warnings'
TASK_PROJECT_ID_KEY = 'project_id'
TASK_DATASET_ID_KEY = 'dataset_id'
TASK_BATCH_KEY = 'batch'
TASK_TYPE_KEY = 'task_type'
TASK_ANNOTATIONS_KEY = 'annotations'
TASK_PARAMS_KEY = 'params'
TASK_ATTACHMENT_KEY = 'attachment'
TASK_ATTACHMENT_TYPE_KEY = 'attachment_type'
TASK_TAGS_KEY = 'tags'
TASK_METADATA_KEY = 'metadata'
TASK_EXTERNAL_DATA_KEY = 'external_data'
TASK_UNIQUE_ID_KEY = 'unique_id'

IMAGE_TASK_MEDIA_SPECS = 'media_specs'
IMAGE_TASK_WIDTH = 'width'
IMAGE_TASK_HEIGHT = 'height'

GEOTASK_BOUNDS_KEY = 'bounds'
GEOTASK_BOUNDS_NW_KEY = 'nw'
GEOTASK_BOUNDS_NE_KEY = 'ne'
GEOTASK_BOUNDS_SE_KEY = 'se'
GEOTASK_BOUNDS_SW_KEY = 'sw'

GEOTASK_ZOOM_KEY = 'zoom'
GEOTASK_ZOOM_MIN_KEY = 'min'
GEOTASK_ZOOM_MAX_KEY = 'max'

ANNOTATION_ID_KEY = 'id'
ANNOTATION_TYPE_KEY = 'annotation_type'
ANNOTATION_LABEL_KEY = 'label'
ANNOTATION_SOURCE_KEY = 'source'
ANNOTATION_IS_MODEL_RUN_KEY = 'is_model_run'
ANNOTATION_IOU_KEY = 'iou'
ANNOTATION_ATTRIBUTES_KEY = 'attributes'

BOUNDING_BOX_TOP_KEY = 'top'
BOUNDING_BOX_LEFT_KEY = 'left'
BOUNDING_BOX_WIDTH_KEY = 'width'
BOUNDING_BOX_HEIGHT_KEY = 'height'
BOUNDING_BOX_ROTATION_KEY = 'rotation'

POLYGON_SEGMENTS_KEY = 'segments'
POLYGON_SEGMENTS_PATH_KEY = 'path'
POLYGON_SEGMENTS_SUBTRACTION_KEY = 'subtraction'
POLYGON_VERTEX_X_KEY = 'x'
POLYGON_VERTEX_Y_KEY = 'y'

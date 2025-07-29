COMPONENT_KEY = "digitizer"
ES_INDEX_DEFAULT = "digitizer_output"


class ModelTypes:
    IMAGE_PROCESSOR = "image_processor"


class StatusKeys:
    DOWNLOAD_MODELS = "digitizer_download_models"
    CLEAN_UP = "digitizer_clean_up"
    ELASTICSEARCH_UPLOAD = "digitizer_elasticsearch_upload"
    UPLOAD = "s3_upload"
    DOWNLOAD = "digitizer_s3_download"
    OCR = "digitizer_ocr"


class Queue:
    IO = "io"
    DOWNLOAD = "download"
    FINISH = "finish"
    OCR = "ocr"


class Tasks:
    START_DIGITIZER_PIPELINE = "start_digitizer_pipeline"

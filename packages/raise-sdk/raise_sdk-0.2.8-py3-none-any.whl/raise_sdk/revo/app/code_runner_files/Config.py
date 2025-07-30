from pathlib import Path
import platform
import os


class LogConfig:
    LOGS_FOLDER_NAME = os.environ.get("LOG_FOLDER_NAME", "logs")
    LOGS_FILE_NAME = os.environ.get("LOG_FILE_NAME", "rai-psm.log")
    LOG_MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB
    DEBUG = os.environ.get("DEBUG", "True")
    LOG_PATH = Path("./", LOGS_FOLDER_NAME) if platform.uname().system == "Linux" else Path(".", LOGS_FOLDER_NAME)
    if not LOG_PATH.exists():
        LOG_PATH.mkdir(exist_ok=True)
    LOG_DIR = str(LOG_PATH)

    LEVEL = "DEBUG" if DEBUG else "WARN"  # Valid values: DEBUG | INFO | WARN | ERROR | CRITICAL
    CONSOLE_HANDLER = DEBUG
    CONSOLE_HANDLER_LEVEL = "DEBUG"
    FILE_HANDLER = True


class CeleryConfigProcessingScripts:
    MODULE_NAME = "RAI Processing Scripts Manager"
    BROKER_IP = os.environ.get("BROKER_IP", "192.168.65.169")
    BROKER_PORT = os.environ.get("BROKER_PORT", "5672")
    BROKER_CLIENT_USER = os.environ.get("BROKER_CLIENT_USER", "raise")
    BROKER_CLIENT_PWD = os.environ.get("BROKER_CLIENT_PWD", "raise_pwd")
    TOPIC = os.environ.get("PROCESSING_SCRIPTS_TOPIC", "processing-scripts")
    BROKER_URL = f"amqp://{BROKER_CLIENT_USER}:{BROKER_CLIENT_PWD}@{BROKER_IP}:{BROKER_PORT}/{TOPIC}"

    # json serializer is more secure than the default pickle
    CELERY_TASK_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_RESULT_SERIALIZER = "json"

    # Use UTC instead of localtime
    CELERY_ENABLE_UTC = True

    # Maximum retries per task
    CELERY_TASK_ANNOTATIONS = {"*": {"max_retries": 3}}

    # A custom property used in tasks.py:run()
    CUSTOM_RETRY_DELAY = 10

    # Kill all long-running tasks with late acknowledgment enabled on connection loss
    CELERYD_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = True


class MinioConfig:
    # Connection configuration
    MINIO_IP = os.environ.get("MINIO_IP")
    MINIO_USER = os.environ.get("MINIO_USER")
    MINIO_PWD = os.environ.get("MINIO_PWD")
    # Buckets
    DATASETS_BUCKET = os.environ.get("MINIO_BUCKET_DATASETS", "datasets")
    PROCESSING_SCRIPTS_BUCKET = os.environ.get("MINIO_BUCKET_PROCESSING_SCRIPTS", "processing-scripts")
    PROCESSING_SCRIPTS_RESULTS_BUCKET = os.environ.get(
        "MINIO_BUCKET_PROCESSING_SCRIPTS_RESULTS", "processing-scripts-results"
    )

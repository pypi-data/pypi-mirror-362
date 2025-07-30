# -*- coding: utf-8 -*-
"""
    RAISE - RAI Certified Node API

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os
import shutil
import docker
from time import sleep
import socket
from typing import List
import json

# Third-party app imports

# Imports from your apps
from app.code_runner_files.MinioClient import MinioClient
from app.code_runner_files.Config import MinioConfig
from app.code_runner_files.custom_exceptions import DockerConnectionError


TIMEOUT_CONTAINER = os.environ.get("TIMEOUT_CONTAINER", 300)
RESULTS_FILENAME = os.environ.get("RESULTS_FILENAME", "results")


class CodeRunner:
    def __init__(self, experiment_id: str, dataset_id_list: List[str], logger):

        self.experiment_id = experiment_id
        self.dataset_id_list = dataset_id_list
        self.status_code = 0

        self.root_path = os.getcwd()
        self.data_path = f"{self.root_path}/experiments/{experiment_id}/data"
        self.experiment_path = f"{self.root_path}/experiments/{experiment_id}"
        self.logs_path = f"{self.experiment_path}/logs"
        self.results_path = f"{self.root_path}/experiments/{experiment_id}/results"

        os.makedirs(self.experiment_path)
        os.makedirs(self.logs_path)
        os.makedirs(self.results_path)

        self.logfile = f"{self.logs_path}/rai-psm.log"
        open(self.logfile, "w").close()
        os.chmod(self.logfile, mode=666)

        self.minio_client = MinioClient()

        self.logger = logger
        self.docker_client = connect_with_docker(self.logger)
        if self.docker_client is None:
            raise DockerConnectionError
        
    def prepare_data_from_minio(self):
        """
        From the datasets bucket takes various files and paced them in the data path
        where according to the dockerfile they will be copied to working directory
        """
        for dataset_id in self.dataset_id_list:
            objects = self.minio_client.list_folder_files(bucket_name=os.environ.get("DATASETS_BUCKET"),
                                                      prefix=f"{dataset_id}/")
            for obj in objects:
                file = obj.split('/')[1]
                if file != "descriptive_statistics.json":
                    self.minio_client.get_object(bucket_name=os.environ.get("DATASETS_BUCKET"),
                                                org_file=obj,
                                                dest_file=f"{self.data_path}/{dataset_id}/{file}") 
            self.files_downloaded = True

    def erase_downloaded_data():
        if self.files_downloaded:
            shutil.rmtree(self.data_path) 

    def prepare_experiment_path(self):
        """
        From the processing scripts bucket takes the files defined in config 
        to the working directory
        """
        file_paths = self.minio_client.list_folder_files(
            bucket_name=MinioConfig.PROCESSING_SCRIPTS_BUCKET,
            prefix=f"{self.experiment_id}/"
        )
        for file_path in file_paths:
            self.minio_client.get_object(
                bucket_name=MinioConfig.PROCESSING_SCRIPTS_BUCKET,
                org_file=f"{file_path}",
                dest_file=f"{self.root_path}/experiments/{file_path}",
            )
            # NO NEED TO COPY THE CODE RUNNER RELATED FILES
        # shutil.copytree(f"{self.root_path}/code_runner_files", f"{self.experiment_path}/code_runner_files")
        os.chmod(f"{self.results_path}", mode=0o777) # Required, if not the child docker does not have permissions to write in the folder
        os.chmod(f"{self.logs_path}", mode=0o777) # Required, if not the child docker does not have permissions to write in the folder

    def build_docker_image(self):
        log_buffer_size = 7 # Should this be a paramter?
        log_buffer = []
        build_logs = self.docker_client.api.build(
                    path=self.experiment_path,
                    dockerfile=f"{self.experiment_path}/Dockerfile",
                    tag=f"img_raise_{self.experiment_id}",
                    nocache=True,
                    forcerm=True,
                    rm=True,
                    decode=True,  
                )
                
        for chunk in build_logs:
            if "stream" in chunk: # Usual logs -> required as error details are stored as this logs
                log_line = chunk["stream"].strip()
                log_buffer.append(f"{log_line}\n")
                if len(log_buffer) > log_buffer_size:
                    log_buffer.pop(0)
            elif "errorDetail" in chunk: # Detect the error in logs -> write the logs to minio and the last usual logs
                error_message = chunk["errorDetail"].get("message", "").strip()
                log_buffer.append(f"Docker build error: {error_message}\n")
                docker_logs = " ".join(log_buffer)
                self.minio_client.save_object(bucket_name=MinioConfig.PROCESSING_SCRIPTS_RESULTS_BUCKET,object_name=f"{self.experiment_id}/logfile.log",data=docker_logs,content_type="text/plain")
                raise docker.errors.BuildError(f"Error building Docker image. Check logs of the experiment",build_log=[])

    def run_docker_container(self):
        try:
            self.docker_client.containers.run(
                image=f"img_raise_{self.experiment_id}",
                environment=self.environment_variables(),
                auto_remove=True,
                remove=True,
                name=f"container_raise_{self.experiment_id}",
                detach=True,
                volumes={
                        "/app/experiments/" + str(self.experiment_id) + "/results": {
                            "bind": "/tmp/results", 
                            "mode": "rw"
                            },
                            "/app/experiments/" + str(self.experiment_id) + "/logs": {
                            "bind": "/tmp/logs", 
                            "mode": "rw"
                            }
                        }, 
                runtime="runsc"
            ).wait(timeout=TIMEOUT_CONTAINER)
            self.status_code = 0
        except Exception as exc:
            self.logger.exception(f"Exception occurred while running the docker container: {str(exc)}")
            self.status_code = 2

    def upload_results_to_minio_and_execution_logs(self):
        files = os.listdir(self.results_path)
        self.logger.info("files stored in results ->" + str(files))
        self.minio_client.save_object_from_file(bucket_name=os.environ.get(
                    "PROCESSING_SCRIPTS_RESULTS_BUCKET", "processing-scripts-results"
                    ),object_name=f"{self.experiment_id}/logfile.log",filepath=f"{self.logs_path}/execution.log")
        if files:
            for file in files:
                self.minio_client.save_object_from_file(bucket_name=os.environ.get(
                    "PROCESSING_SCRIPTS_RESULTS_BUCKET", "processing-scripts-results"
                    ),object_name=f"{self.experiment_id}/{file}",filepath=f"{self.results_path}/{file}")
        else:
            self.logger.info("There are no files in results folder!")
            return 

    def check_results(self):
        try:
            processing_scripts_results_bucket = os.environ.get(
                "PROCESSING_SCRIPTS_RESULTS_BUCKET", "processing-scripts-results"
            )
            results_files = self.minio_client.list_folder_files(
                bucket_name=processing_scripts_results_bucket, prefix=f"{self.experiment_id}/"
            )
            if len(results_files) == 0:
                self.status_code = 1
            else:
                self.status_code = 0
        except Exception as exc:
            self.logger.exception(f"Exception occurred while checking the results: {str(exc)}")
            self.status_code = 2

    def save_logfile(self):
        try:
            processing_scripts_results_bucket = os.environ.get(
                "PROCESSING_SCRIPTS_RESULTS_BUCKET", "processing-scripts-results"
            )
            self.minio_client.save_object_from_file(
                bucket_name=processing_scripts_results_bucket,
                object_name=f"{self.experiment_id}/logfile.log",
                filepath=self.logfile,
            )
        except Exception as exc:
            self.logger.exception(f"Exception occurred while saving the log file: {str(exc)}")

    def remove_image(self):
        try:
            shutil.rmtree(self.experiment_path)
            image = f"img_raise_{self.experiment_id}"
            self.docker_client.images.remove(image)
            return True
        except Exception as exc:
            self.logger.exception(f"Exception occurred while removing the docker image: {str(exc)}")
            return False

    def environment_variables(self):
        # minio_service_name = os.environ.get("MINIO_SERVICE_NAME", "minio.")
        # data = socket.gethostbyname(minio_service_name)
        # minio_service_ip = str(data)
        # minio_port = os.environ.get("MINIO_PORT", "9000")
        # minio_host_port_resolved = f"{minio_service_ip}:{minio_port}"

        return {
            "EXPERIMENT_ID": self.experiment_id,
            "RAISE_DATASET_ID_LIST": json.dumps(self.dataset_id_list) # Load dataset id list as a string id1,id2,id3
            # "MINIO_IP": minio_host_port_resolved,
            # "MINIO_USER": os.environ.get("MINIO_USER"),
            # "MINIO_PWD": os.environ.get("MINIO_PWD"),
            # "DATASETS_BUCKET": os.environ.get("DATASETS_BUCKET"),
            # "PROCESSING_SCRIPTS_BUCKET": os.environ.get("PROCESSING_SCRIPTS_BUCKET"),
            # "PROCESSING_SCRIPTS_RESULTS_BUCKET": os.environ.get("PROCESSING_SCRIPTS_RESULTS_BUCKET"),
            # "RESULTS_FILENAME": RESULTS_FILENAME,
        }


def connect_with_docker(logger):
    for _ in range(6):
        try:
            client = docker.from_env()
        except Exception:
            logger.info("HTTPConnectionPool(host='docker', port=2375) Connection refused, retrying...")
            sleep(10)
        else:
            logger.info("New connection to docker established.")
            return client
    else:
        logger.exception("Connection to docker refused.")
        return None

# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os

# from pathlib import Path

# Third-party app imports

# Imports from your apps
from code_runner_files.MinioClient import MinioClient

# from code_runner_files.custom_exceptions import MinioConnectionError
from code_runner_files.LogClass import LogClass
from code_runner_files.custom_exceptions import ResultsFormatNotAvailable

VALID_RESULTS_FORMATS = ["txt", "csv", "fig"]


class ResultsObject(LogClass):
    """
    Class for the researcher to store the results of his algorithm, through the AbstractExperimentRunner class
    """

    def __init__(self, experiment_id: str, results_data, filename: str, format: str):
        super().__init__()

        self.experiment_id = experiment_id
        self.results_data = results_data
        self.results_filename = filename

        if format in VALID_RESULTS_FORMATS:
            self.results_format = format
        else:
            raise ResultsFormatNotAvailable

        self._minio_client = MinioClient()
        self.results_bucket = os.environ.get("PROCESSING_SCRIPTS_RESULTS_BUCKET")

    def store_results_object(self):
        self.log_info(f"Saving {self.results_filename} for experiment_id = {self.experiment_id}")
        try:
            if self.results_format == "csv":
                self._minio_client.save_object(
                    bucket_name=self.results_bucket,
                    object_name=f"{self.experiment_id}/{self.results_filename}.csv",
                    data=self.results_data.to_csv(),
                    content_type="application/csv",
                )
            elif self.results_format == "txt":
                self._minio_client.save_object(
                    bucket_name=self.results_bucket,
                    object_name=f"{self.experiment_id}/{self.results_filename}.txt",
                    data=str(self.results_data),
                    content_type="text/plain",
                )
            elif self.results_format == "fig":
                self.results_data.savefig(f"{self.results_filename}.png")
                self._minio_client.save_object_from_file(
                    bucket_name=self.results_bucket,
                    object_name=f"{self.experiment_id}/{self.results_filename}.png",
                    filepath=f"{self.results_filename}.png",
                )
            else:
                raise ResultsFormatNotAvailable
        except Exception:
            self.log_exception(f"Could not retrieve results for experiment_id = {self.experiment_id}")

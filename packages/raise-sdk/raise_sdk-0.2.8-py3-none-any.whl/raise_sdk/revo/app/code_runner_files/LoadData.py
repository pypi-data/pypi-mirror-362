# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os

# import json
import pandas as pd

# Third-party app imports


# Imports from your apps
from code_runner_files.Dataset import Dataset
from code_runner_files.MinioClient import MinioClient
from code_runner_files.custom_exceptions import MinioConnectionError
from code_runner_files.LogClass import LogClass
from code_runner_files.Config import MinioConfig


class LoadData(LogClass):
    """
    Class to store the data corresponding to the requested dataset_id for code running
    """

    def __init__(self, dataset_id: str, data_format: str):
        super().__init__()
        self.dataset_id = dataset_id
        self.data_format = data_format

        self.__data = self.load_data()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    def load_data(self):
        try:
            self.log_info(
                f"Loading dataset from minio, dataset_id = {self.dataset_id}, data_format = {self.data_format}"
            )
            if self.data_format == "csv":
                minio_client = MinioClient()
                minio_client.get_object(
                    bucket_name=MinioConfig.DATASETS_BUCKET,
                    org_file=f"{self.dataset_id}/datafile.csv",
                    dest_file="datafile.csv",
                )
                data = pd.read_csv("datafile.csv")
                os.remove("datafile.csv")

            dataset = Dataset(name=self.dataset_id, data=data)
            return dataset

        except MinioConnectionError:
            self.log_exception("There has been a problem when loading data from Minio")
        except Exception as exc:
            self.log_exception(f"Exception occurred when loading data: {str(exc)}")

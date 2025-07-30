# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import io

# Third-party app imports
from minio import Minio
from minio.error import S3Error

# Imports from your apps
from code_runner_files.custom_exceptions import MinioConnectionError
from code_runner_files.Config import MinioConfig


class MinioClient:
    def __init__(self):

        self.client = Minio(MinioConfig.MINIO_IP, MinioConfig.MINIO_USER, MinioConfig.MINIO_PWD, secure=False)

    def save_object(self, bucket_name, object_name, data, content_type):
        try:
            data_stream, bytes_len = self.transform_data(data)
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data_stream,
                length=bytes_len,
                content_type=content_type,
            )
        except S3Error:
            raise MinioConnectionError("Error while saving " + object_name + " object in Minio")

    def save_object_from_file(self, bucket_name, object_name, filepath):
        try:
            self.client.fput_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=filepath,
            )
        except S3Error:
            raise MinioConnectionError("Error while saving " + object_name + " object in Minio")

    def get_object(self, bucket_name, org_file, dest_file):
        try:
            self.client.fget_object(bucket_name=bucket_name, object_name=org_file, file_path=dest_file)
        except S3Error:
            raise MinioConnectionError("Error while reading " + org_file + " object from Minio")

    def transform_data(self, data):
        values_as_bytes = data.encode("utf-8")
        values_as_a_stream = io.BytesIO(values_as_bytes)
        return values_as_a_stream, len(values_as_bytes)

    def object_exists(self, bucket_name, object_name):
        objects = self.client.list_objects(bucket_name)
        for ob in objects:
            if object_name in ob.object_name:
                return True
        return False

    def list_folder_files(self, bucket_name, prefix):
        files = []
        objects = self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True)
        for obj in objects:
            files.append(obj.object_name)
        return files

# -*- coding: utf-8 -*-
"""
    RAISE - RAI Certified Node API

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports

# Imports from your apps


class MinioConnectionError(Exception):
    """Raised if there has been a problem when saving a file in Minio"""

    def __init__(self, message="There has been a problem when saving a file in Minio Server"):
        self.message = message
        super().__init__(self.message)


class DockerConnectionError(Exception):
    """Raised if there has been a problem when connecting with docker"""

    def __init__(self, message="There has been a problem with docker connection"):
        self.message = message
        super().__init__(self.message)


class DockerImageBuildingError(Exception):
    """Raised if there has been a problem when building the docker image for the experiment"""

    def __init__(self, message="There has been a problem when building the docker image for the experiment"):
        self.message = message
        super().__init__(self.message)


class ResultsFormatNotAvailable(Exception):
    """Raised if a results format is not available"""

    def __init__(
        self,
        message="The chose results format type is not compatible with the actual version of the RAI Certified Node.",
    ):
        self.message = message
        super().__init__(self.message)

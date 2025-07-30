# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import abc


# Third-party app imports


# Imports from your apps
from code_runner_files.Dataset import Dataset


class AbstractCodeRunner(metaclass=abc.ABCMeta):
    """
    An abstract class to be inherited by the code to be executed in the RAI node

    :param dataset: Dataset obtained after querying the RAI node. When running this script locally for development, \
        it uses synthetic data. But, run in the RAI node, dataset contains a pointer to real query data in the RAI \
        node.

    """

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def run_code(self):
        """

        Abstract method to be implemented by this API users. This code will be executed on the DataSet.

        :returns: It does not return anything
        :rtype: None
        """
        raise NotImplementedError

# -*- coding: utf-8 -*-
"""
    RAISE - RAI Processing Scripts Manager

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports


# Third-party app imports


# Imports from your apps


class Dataset:
    """
    Abstract class to define type specific Data classes for DataSet

    :param name: Name of the dataset
    """

    def __init__(self, name: str, data):
        super().__init__()
        self._name = name
        self._data = data

    def __getdata__(self):
        return self._data

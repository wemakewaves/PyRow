"""
PyRow.Concept2.Exception.RetryLimitException
"""

# coding=utf-8
__author__ = 'UVD'


class RetryLimitException(Exception):
    """
    RetryLimitException
    """

    def __init__(self, waiting_for):
        """
        :param string waiting_for:
        :return:
        """
        self.__waiting_for = waiting_for

    def __str__(self):
        """
        :return string:
        """
        return "Retry limit reached, waiting for {0}".format(self.__waiting_for)

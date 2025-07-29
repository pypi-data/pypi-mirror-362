import argparse

from wai.logging import LOGGING_WARNING
from wai.ma.algorithm.pls import SIMPLS as WaiSIMPLS

from ._abstractpls import AbstractSingleResponsePLS, PREPROCESSING_ENUM


class SIMPLS(AbstractSingleResponsePLS):
    """
    Applies SIMPLS to the batches.
    """

    def __init__(self, preprocessing: str = None, num_components: int = None,
                 response: str = None, num_coefficients: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param preprocessing: the type of preprocessing to apply
        :type preprocessing: str
        :param num_components: the number of PLS components
        :type num_components: int
        :param response: the name of the sample_data field to use as response
        :type response: str
        :param num_coefficients: the number of coefficients of W to keep, 0 for all
        :type num_coefficients: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(preprocessing=preprocessing, num_components=num_components, response=response,
                         logger_name=logger_name, logging_level=logging_level)
        self.num_coefficients = num_coefficients

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "simpls"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies SIMPLS to the batches of spectra. More information: https://www.sciencedirect.com/science/article/abs/pii/016974399385002X"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-c", "--num_coefficients", type=int, help="The number of coefficients of W to keep, 0 for all.", default=0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.num_coefficients = ns.num_coefficients

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.num_coefficients is None:
            self.num_coefficients = 0

    def _initialize_algorithm(self):
        """
        Initializes the PLS algorithm, setting all the parameters.

        :return: the instance of the PLS algorithm
        """
        result = WaiSIMPLS()
        result.preprocessing_type = PREPROCESSING_ENUM[self.preprocessing]
        result.num_components = self.num_components
        result.num_coefficients = self.num_coefficients
        return result

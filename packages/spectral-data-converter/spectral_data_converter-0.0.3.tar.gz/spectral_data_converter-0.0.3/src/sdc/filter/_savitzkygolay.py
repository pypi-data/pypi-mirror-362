import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.ma.transformation import SavitzkyGolay as WaiSavitzkyGolay

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class SavitzkyGolay(Filter):
    """
    Applies the Savitzky-Golay smoothing filter.
    For more details see: https://en.wikipedia.org/wiki/Savitzky-Golay_filter
    """

    def __init__(self, polynomial_order: int = None, derivative_order: int = None,
                 num_points_left: int = None, num_points_right: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param polynomial_order: the polynomial order to use
        :type polynomial_order: int
        :param derivative_order: the derivative order to use
        :type derivative_order: int
        :param num_points_left: the number of points to the left of the current point
        :type num_points_left: int
        :param num_points_right: the number of points to the right of the current pint
        :type num_points_right: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.polynomial_order = polynomial_order
        self.derivative_order = derivative_order
        self.num_points_left = num_points_left
        self.num_points_right = num_points_right

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "savitzky-golay"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies the Savitzky-Golay smoothing filter. For more details see: https://en.wikipedia.org/wiki/Savitzky-Golay_filter"

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-p", "--polynomial_order", type=int, help="The polynomial order to use.", default=2, required=False)
        parser.add_argument("-d", "--derivative_order", type=int, help="The derivative order to use.", default=1, required=False)
        parser.add_argument("-L", "--num_points_left", type=int, help="The number of points to the left from the current point.", default=3, required=False)
        parser.add_argument("-R", "--num_points_right", type=int, help="The number of points to the right from the current point.", default=3, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.polynomial_order = ns.polynomial_order
        self.derivative_order = ns.derivative_order
        self.num_points_left = ns.num_points_left
        self.num_points_right = ns.num_points_right

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.polynomial_order is None:
            self.polynomial_order = 2
        if self.polynomial_order < 2:
            raise Exception("Polynomial order has to be >=2, provided: %s" % str(self.polynomial_order))
        if self.derivative_order is None:
            self.derivative_order = 1
        if self.derivative_order < 0:
            raise Exception("Derivative order has to be >=0, provided: %s" % str(self.derivative_order))
        if self.num_points_left is None:
            self.num_points_left = 3
        if self.num_points_left < 0:
            raise Exception("Number of points to the left must be at least 0, provided: %s" % str(self.num_points_left))
        if self.num_points_right is None:
            self.num_points_right = 3
        if self.num_points_right < 0:
            raise Exception("Number of points to the right must be at least 0, provided: %s" % str(self.num_points_right))
        if self.num_points_left + self.num_points_right < 1:
            raise Exception("Window size must be at least 1!")

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        trans = WaiSavitzkyGolay()
        trans.polynomial_order = self.polynomial_order
        trans.derivative_order = self.derivative_order
        trans.num_points_left = self.num_points_left
        trans.num_points_right = self.num_points_right

        for item in make_list(data):
            sp = item.spectrum
            mat = spectrum_to_matrix(sp, add_waveno=False)
            trans.configure(mat)
            self.logger().info("coefficients: %s" % str(trans.coefficients))
            mat_new = trans.transform(mat)
            w_new = sp.waves[self.num_points_left:-self.num_points_right]
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp.id, waveno=w_new, sample_data=safe_deepcopy(sp.sample_data))
            item_new = Spectrum2D(spectrum_name=item.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)

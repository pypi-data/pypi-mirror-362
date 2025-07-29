import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.ma.transformation import SavitzkyGolay2 as WaiSavitzkyGolay2

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class SavitzkyGolay2(Filter):
    """
    Applies the Savitzky-Golay smoothing filter.
    For more details see: https://en.wikipedia.org/wiki/Savitzky-Golay_filter
    """

    def __init__(self, polynomial_order: int = None, derivative_order: int = None, num_points: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param polynomial_order: the polynomial order to use
        :type polynomial_order: int
        :param derivative_order: the derivative order to use
        :type derivative_order: int
        :param num_points: the number of points to the left of the current point
        :type num_points: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.polynomial_order = polynomial_order
        self.derivative_order = derivative_order
        self.num_points = num_points

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "savitzky-golay2"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies the Savitzky-Golay smoothing filter, using a centered window of the specified size. For more details see: https://en.wikipedia.org/wiki/Savitzky-Golay_filter"

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
        parser.add_argument("-n", "--num_points", type=int, help="The size of the window (left + center + right), must be an odd number.", default=7, required=False)
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
        self.num_points = ns.num_points

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
        if self.num_points is None:
            self.num_points = 7
        if self.num_points < 3:
            raise Exception("Window size must be at least 3, provided: %s" % str(self.num_points))
        if self.num_points % 2 == 0:
            raise Exception("Window sie must be an odd number, provided: %s" % str(self.num_points))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        trans = WaiSavitzkyGolay2()
        trans.polynomial_order = self.polynomial_order
        trans.derivative_order = self.derivative_order
        trans.num_points = self.num_points // 2

        for item in make_list(data):
            sp = item.spectrum
            mat = spectrum_to_matrix(sp, add_waveno=False)
            trans.configure(mat)
            self.logger().info("coefficients: %s" % str(trans.coefficients))
            mat_new = trans.transform(mat)
            w_new = sp.waves[self.num_points // 2:-(self.num_points // 2)]
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp.id, waveno=w_new, sample_data=safe_deepcopy(sp.sample_data))
            item_new = Spectrum2D(spectrum_name=item.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)

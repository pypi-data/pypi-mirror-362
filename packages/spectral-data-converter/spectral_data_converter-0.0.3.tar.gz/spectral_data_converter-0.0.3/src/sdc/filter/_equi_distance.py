import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.ma.filter import Equidistance

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class EquiDistance(Filter):
    """
    Generates a spectrum with the specified number of equally spaced wave numbers.
    """

    def __init__(self, num_wavenos: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param num_wavenos: the number of wave numbers to resample to
        :type num_wavenos: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.num_wavenos = num_wavenos

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "equi-distance"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Generates a spectrum with the specified number of equally spaced wave numbers. The amplitudes gets interpolated accordingly."

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
        parser.add_argument("-n", "--num_wavenos", type=int, help="The number of wavenumbers to resample to.", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.num_wavenos = ns.num_wavenos

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.num_wavenos is None:
            raise Exception("Number of wave numbers not specified!")
        if self.num_wavenos < 2:
            raise Exception("At least 2 wave numbers required, provided: %s" % str(self.num_wavenos))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        flt = Equidistance(num_samples=self.num_wavenos)

        for item in make_list(data):
            sp = item.spectrum
            mat = spectrum_to_matrix(sp, add_waveno=True)
            mat_new = flt.transform(mat)
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp.id, sample_data=safe_deepcopy(sp.sample_data))
            item_new = Spectrum2D(spectrum_name=item.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)

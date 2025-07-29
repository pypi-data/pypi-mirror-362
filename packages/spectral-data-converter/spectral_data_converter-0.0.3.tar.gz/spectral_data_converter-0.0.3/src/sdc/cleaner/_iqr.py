import argparse
import numpy as np
from typing import List

from sdc.api import Cleaner, Spectrum2D
from wai.logging import LOGGING_WARNING


class IQRCleaner(Cleaner):

    def __init__(self, factor: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the handler.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.factor = factor

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "iqr-cl"

    def description(self) -> str:
        """
        Returns a description of the cleaner.

        :return: the description
        :rtype: str
        """
        return "Calculates for each wave number the inter-quartile range and removes any spectra that have any amplitudes that fall outside the ranges: lower = q1 - factor * iqr, upper = q3 + factor * iqr"

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
        parser.add_argument("-f", "--factor", type=float, help="The factor to apply to the IQR range to determine outliers.", default=4.25, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.factor = ns.factor

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.factor is None:
            self.factor = 4.25

    def _do_clean(self, data: List) -> List:
        """
        Cleans the data records.

        :return: the records to clean
        :rtype: the cleaned records
        """
        # compute lower/upper bounds for amplitudes
        ampls = [x.spectrum.amplitudes for x in data]
        q1 = np.percentile(ampls, 25, axis=0)
        q3 = np.percentile(ampls, 75, axis=0)
        iqr = q3 - q1
        upper = q3 + self.factor * iqr
        lower = q1 - self.factor * iqr

        # check whether amplitudes exceed limits
        upper_count = [0] * len(data)
        lower_count = [0] * len(data)
        for n, sp in enumerate(data):
            for i, ampl in enumerate(sp.spectrum.amplitudes):
                if ampl > upper[i]:
                    upper_count[n] += 1
                if ampl < lower[i]:
                    lower_count[n] += 1

        # remove spectra that exceed any lower/upper bounds
        result = []
        for n, sp in enumerate(data):
            if (upper_count[n] == 0) and (lower_count[n] == 0):
                result.append(sp)

        return result

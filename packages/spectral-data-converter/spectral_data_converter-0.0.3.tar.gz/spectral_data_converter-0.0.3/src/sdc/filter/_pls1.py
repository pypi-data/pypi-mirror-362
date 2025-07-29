from wai.ma.algorithm.pls import PLS1 as WaiPLS1

from ._abstractpls import AbstractSingleResponsePLS, PREPROCESSING_ENUM


class PLS1(AbstractSingleResponsePLS):
    """
    Applies PLS1 to the batches.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "pls1"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Applies PLS1 to the batches of spectra. For more information see: https://en.wikipedia.org/wiki/Partial_least_squares_regression#PLS1"

    def _initialize_algorithm(self):
        """
        Initializes the PLS algorithm, setting all the parameters.

        :return: the instance of the PLS algorithm
        """
        result = WaiPLS1()
        result.preprocessing_type = PREPROCESSING_ENUM[self.preprocessing]
        result.num_components = self.num_components
        return result

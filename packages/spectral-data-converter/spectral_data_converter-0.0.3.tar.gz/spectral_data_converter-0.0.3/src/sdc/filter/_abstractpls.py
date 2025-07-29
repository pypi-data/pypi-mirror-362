import abc
import argparse
import numpy as np
from typing import List, Dict

from wai.ma.core import PreprocessingType
from wai.ma.core.matrix import Matrix
from wai.logging import LOGGING_WARNING
from sdc.api import TrainableBatchFilter, Spectrum2D, safe_deepcopy, spectra_to_matrix, matrix_to_spectra


PREPROCESSING_NONE = "none"
PREPROCESSING_CENTER = "center"
PREPROCESSING_STANDARDIZE = "standardize"
PREPROCESSING = [
    PREPROCESSING_NONE,
    PREPROCESSING_CENTER,
    PREPROCESSING_STANDARDIZE,
]

PREPROCESSING_ENUM = {
    PREPROCESSING_NONE: PreprocessingType.NONE,
    PREPROCESSING_CENTER: PreprocessingType.CENTER,
    PREPROCESSING_STANDARDIZE: PreprocessingType.STANDARDIZE,
}


class AbstractPLS(TrainableBatchFilter, abc.ABC):
    """
    Ancestor for PLS algorithms.
    """

    def __init__(self, preprocessing: str = None, num_components: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param preprocessing: the type of preprocessing to apply
        :type preprocessing: str
        :param num_components: the number of PLS components
        :type num_components: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.preprocessing = preprocessing
        self.num_components = num_components
        self._algorithm = None

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
        parser.add_argument("-p", "--preprocessing", choices=PREPROCESSING, help="The type of preprocessing to apply.", default=PREPROCESSING_NONE, required=False)
        parser.add_argument("-n", "--num_components", type=int, help="The number of PLS components.", default=5, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.preprocessing = ns.preprocessing
        self.num_components = ns.num_components

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.preprocessing is None:
            self.preprocessing = PREPROCESSING_NONE
        if self.preprocessing not in PREPROCESSING:
            raise Exception("Unknown preprocessing (options: %s): %s" % ("|".join(PREPROCESSING), self.preprocessing))
        if self.num_components is None:
            self.num_components = 5

    def _initialize_algorithm(self):
        """
        Initializes the PLS algorithm, setting all the parameters.

        :return: the instance of the PLS algorithm
        """
        raise NotImplementedError()


class AbstractSingleResponsePLS(AbstractPLS, abc.ABC):
    """
    Ancestor for PLS algorithms that handle a single response vector.
    """

    def __init__(self, preprocessing: str = None, num_components: int = None, response: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param preprocessing: the type of preprocessing to apply
        :type preprocessing: str
        :param num_components: the number of PLS components
        :type num_components: int
        :param response: the name of the sample_data field to use as response
        :type response: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(preprocessing=preprocessing, num_components=num_components,
                         logger_name=logger_name, logging_level=logging_level)
        self.response = response
        self._algorithm = None

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-r", "--response", type=str, help="The name of the sample data field to use as response.", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.response = ns.response

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if (self.response is None) and (self.load_from is None):
            raise Exception("No sample data field specified to use as response!")

    def _supports_serialization(self):
        """
        Returns whether filter can be saved/loaded.

        :return: True if supported
        :rtype: bool
        """
        return True

    def _serialize(self) -> Dict:
        """
        Returns the filter's internal representation to save to disk.

        :return: the data to save
        :rtype: dict
        """
        return {
            "algorithm": self._algorithm,
            "response": self.response,
        }

    def _deserialize(self, data: Dict):
        """
        Applies the filter's internal representation loaded from disk.

        :param data: the data to instantiate from
        :type data: dict
        :return: whether the filter is considered trained after deserialiation
        :rtype: bool
        """
        self._algorithm = data.get("algorithm", None)
        self.response = data.get("response", None)
        return (self._algorithm is not None) and (self.response is not None)

    def _initialize_algorithm(self):
        """
        Initializes the PLS algorithm, setting all the parameters.

        :return: the instance of the PLS algorithm
        """
        raise NotImplementedError()

    def _process_batch(self, batch):
        """
        Processes the batch.

        :param batch: the batch to process
        :return: the potentially updated batch
        """
        result = []
        mat_old = spectra_to_matrix([x.spectrum for x in batch])

        if not self._trained:
            self._trained = True
            self._algorithm = self._initialize_algorithm()
            responses_old = [x.spectrum.sample_data[self.response] for x in batch]
            self._algorithm.initialize(mat_old, Matrix(np.asarray(responses_old).reshape(-1, 1)))

        mat_new = self._algorithm.transform(mat_old)
        responses_new = self._algorithm.predict(mat_old)
        batch_new = matrix_to_spectra(mat_new, waveno=[x for x in range(mat_new.num_columns())])
        i = 0
        for sp_old, sp_new in zip(batch, batch_new):
            sp_new.sample_data = safe_deepcopy(sp_old.spectrum.sample_data)
            sp_new.sample_data[self.response] = float(responses_new.data[i])
            item_new = Spectrum2D(spectrum_name=sp_old.spectrum_name, spectrum=sp_new)
            result.append(item_new)
            i += 1

        return result


class AbstractMultiResponsePLS(AbstractPLS, abc.ABC):
    """
    Ancestor for PLS algorithms that handle multiple response vectors.
    """

    def __init__(self, preprocessing: str = None, num_components: int = None, responses: List[str] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param preprocessing: the type of preprocessing to apply
        :type preprocessing: str
        :param num_components: the number of PLS components
        :type num_components: int
        :param responses: the names of the sample_data fields to use as responses
        :type responses: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(preprocessing=preprocessing, num_components=num_components,
                         logger_name=logger_name, logging_level=logging_level)
        self.responses = responses
        self._algorithm = None

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-r", "--responses", type=str, help="The name of the sample data fields to use as responses.", default=None, required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.responses = ns.responses

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if ((self.responses is None) or (len(self.responses) == 0)) and (self.load_from is None):
            raise Exception("No sample data fields specified to use as responses!")

    def _supports_serialization(self):
        """
        Returns whether filter can be saved/loaded.

        :return: True if supported
        :rtype: bool
        """
        return True

    def _serialize(self) -> Dict:
        """
        Returns the filter's internal representation to save to disk.

        :return: the data to save
        :rtype: dict
        """
        return {
            "algorithm": self._algorithm,
            "responses": self.responses,
        }

    def _deserialize(self, data: Dict):
        """
        Applies the filter's internal representation loaded from disk.

        :param data: the data to instantiate from
        :type data: dict
        :return: whether the filter is considered trained after deserialiation
        :rtype: bool
        """
        self._algorithm = data.get("algorithm", None)
        self.responses = data.get("responses", None)
        return (self._algorithm is not None) and (self.responses is not None)

    def _initialize_algorithm(self):
        """
        Initializes the PLS algorithm, setting all the parameters.

        :return: the instance of the PLS algorithm
        """
        raise NotImplementedError()

    def _process_batch(self, batch):
        """
        Processes the batch.

        :param batch: the batch to process
        :return: the potentially updated batch
        """
        result = []
        mat_old = spectra_to_matrix([x.spectrum for x in batch])

        if not self._trained:
            self._trained = True
            self._algorithm = self._initialize_algorithm()
            responses_old = []
            for sp in batch:
                responses_old.append([sp.spectrum.sample_data[x] for x in self.responses])
            self._algorithm.initialize(mat_old, Matrix(np.asarray(responses_old)))

        mat_new = self._algorithm.transform(mat_old)
        responses_new = self._algorithm.predict(mat_old)
        batch_new = matrix_to_spectra(mat_new, waveno=[x for x in range(mat_new.num_columns())])
        i = 0
        for sp_old, sp_new in zip(batch, batch_new):
            sp_new.sample_data = safe_deepcopy(sp_old.spectrum.sample_data)
            for n, response in enumerate(self.responses):
                sp_new.sample_data[response] = float(responses_new.data[i][n])
            item_new = Spectrum2D(spectrum_name=sp_old.spectrum_name, spectrum=sp_new)
            result.append(item_new)
            i += 1

        return result

import abc
import copy
import logging
import os.path
from typing import Dict, Optional, List, Any

from seppl import MetaDataHandler, LoggingHandler
from wai.logging import set_logging_level, LOGGING_INFO

from sdc.api._utils import safe_deepcopy

_logger = None


SAMPLE_ID = "Sample ID"
SAMPLE_TYPE = "Sample Type"


def logger() -> logging.Logger:
    """
    Returns the logger instance to use, initializes it if necessary.

    :return: the logger instance
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("sdc.api.data")
        set_logging_level(_logger, LOGGING_INFO)
    return _logger


class Spectrum(MetaDataHandler, LoggingHandler, abc.ABC):

    def __init__(self, source: str = None, spectrum_name: str = None, spectrum: Any = None):

        if (source is None) and (spectrum_name is None):
            raise Exception("Either source or name must be provided!")

        self._logger = None
        """ for logging. """
        self._source = source
        """ the full path to the spectrum file. """
        self._spectrum_name = spectrum_name
        """ the name of the spectrum file (no path). """
        self._spectrum = spectrum
        """ the spectrum itself. """

    def logger(self) -> logging.Logger:
        """
        Returns the logger instance to use.

        :return: the logger
        :rtype: logging.Logger
        """
        if self._logger is None:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    @property
    def source(self) -> Optional[str]:
        """
        Returns the source filename.

        :return: the full filename, if available
        :rtype: str
        """
        return self._source

    @property
    def spectrum(self) -> Optional[Any]:
        """
        Returns the spectrum.

        :return: the spectrum, can be None
        :rtype: Any
        """
        return self._spectrum

    @property
    def spectrum_name(self) -> Optional[str]:
        """
        Returns the name of the spectrum.

        :return: the spectrum name, can be None
        :rtype: str
        """
        if self._spectrum_name is not None:
            return self._spectrum_name
        elif self.source is not None:
            return os.path.basename(self.source)
        else:
            return None

    @spectrum_name.setter
    def spectrum_name(self, s: str):
        """
        Sets the new name.

        :param s: the new name
        :type s: str
        """
        self._spectrum_name = s

    def duplicate(self, source: str = None, force_no_source: bool = None,
                  name: str = None, spectrum: Any = None):
        """
        Duplicates the container overwriting existing data with any provided data.

        :param source: the source to use
        :type source: str
        :param force_no_source: if True, then source is set to None
        :type force_no_source: bool
        :param name: the name to use
        :type name: str
        :param spectrum: the spectrum to use
        :type spectrum: Any
        :return: the duplicated container
        """
        if (force_no_source is not None) and force_no_source:
            source = None
        else:
            if source is None:
                source = self._source
        if name is None:
            name = self._spectrum_name
        if spectrum is None:
            spectrum = copy.deepcopy(self._spectrum)

        return type(self)(source=source, spectrum_name=name, spectrum=spectrum)

    def to_dict(self, source: bool = True, spectrum: bool = True, metadata: bool = True):
        """
        Returns itself as a dictionary that can be saved as JSON.

        :param source: whether to include the source
        :type source: bool
        :param spectrum: whether to include the spectrum
        :type spectrum: bool
        :param metadata: whether to include the metadata
        :type metadata: bool
        :return: the generated dictionary
        :rtype: dict
        """
        result = dict()
        if source and (self.source is not None):
            result["source"] = self.source
        if self.spectrum_name is not None:
            result["name"] = self.spectrum_name
        if spectrum:
            result["spectrum"] = safe_deepcopy(self.spectrum)
        if metadata and (self.get_metadata() is not None):
            result["metadata"] = copy.deepcopy(self.get_metadata())
        return result


class SampleData(MetaDataHandler, LoggingHandler):

    def __init__(self, source: str = None, sampledata_name: str = None, sampledata: Dict[str, Any] = None):
        self._logger = None
        """ for logging. """
        self._source = source
        """ the full path to the sample data file. """
        self._sampledata_name = sampledata_name
        """ the name of the sample data file (no path). """
        self._sampledata = sampledata
        """ the sample data itself. """

    def logger(self) -> logging.Logger:
        """
        Returns the logger instance to use.

        :return: the logger
        :rtype: logging.Logger
        """
        if self._logger is None:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    @property
    def source(self) -> Optional[str]:
        """
        Returns the source filename.

        :return: the full filename, if available
        :rtype: str
        """
        return self._source

    @property
    def sampledata(self) -> Optional[Dict[str, Any]]:
        """
        Returns the sample data.

        :return: the sample data, can be None
        :rtype: Any
        """
        return self._sampledata

    @property
    def sampledata_name(self) -> Optional[str]:
        """
        Returns the name of the spectrum.

        :return: the spectrum name, can be None
        :rtype: str
        """
        if self._sampledata_name is not None:
            return self._sampledata_name
        elif self.source is not None:
            return os.path.basename(self.source)
        else:
            return None

    @sampledata_name.setter
    def sampledata_name(self, s: str):
        """
        Sets the new name.

        :param s: the new name
        :type s: str
        """
        self._sampledata_name = s

    def duplicate(self, source: str = None, force_no_source: bool = None,
                  name: str = None, sampledata: Dict[str, Any] = None):
        """
        Duplicates the container overwriting existing data with any provided data.

        :param source: the source to use
        :type source: str
        :param force_no_source: if True, then source is set to None
        :type force_no_source: bool
        :param name: the name to use
        :type name: str
        :param sampledata: the spectrum to use
        :type sampledata: Any
        :return: the duplicated container
        """
        if (force_no_source is not None) and force_no_source:
            source = None
        else:
            if source is None:
                source = self._source
        if name is None:
            name = self._sampledata_name
        if sampledata is None:
            sampledata = copy.deepcopy(self._sampledata)

        return type(self)(source=source, sampledata_name=name, sampledata=sampledata)

    def to_dict(self, source: bool = True, sampledata: bool = True):
        """
        Returns itself as a dictionary that can be saved as JSON.

        :param source: whether to include the source
        :type source: bool
        :param sampledata: whether to include the sampledata
        :type sampledata: bool
        :return: the generated dictionary
        :rtype: dict
        """
        result = dict()
        if source and (self.source is not None):
            result["source"] = self.source
        if self.sampledata_name is not None:
            result["name"] = self.sampledata_name
        if sampledata:
            result["sampledata"] = safe_deepcopy(self.sampledata)
        return result


def make_list(data, cls=MetaDataHandler) -> List:
    """
    Wraps the data item in a list if not already a list.

    :param data: the data item to wrap if necessary
    :param cls: the type of class to check for
    :return: the list
    :rtype: list
    """
    if isinstance(data, cls):
        data = [data]
    return data


def flatten_list(data: List):
    """
    If the list contains only a single item, then it returns that instead of a list.

    :param data: the list to check
    :type data: list
    :return: the list or single item
    """
    if len(data) == 1:
        return data[0]
    else:
        return data

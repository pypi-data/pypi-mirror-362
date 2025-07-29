import abc
from typing import List, Any

from wai.logging import LOGGING_WARNING

from seppl import PluginWithLogging, SessionHandler, Session, InputConsumer, OutputProducer, Initializable


class Cleaner(PluginWithLogging, SessionHandler, Initializable, InputConsumer, OutputProducer, abc.ABC):
    """
    Ancestor of classes that read data.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the handler.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self._session = None

    @property
    def session(self) -> Session:
        """
        Returns the current session object

        :return: the session object
        :rtype: Session
        """
        return self._session

    @session.setter
    def session(self, s: Session):
        """
        Sets the session object to use.

        :param s: the session object
        :type s: Session
        """
        self._session = s

    def _do_clean(self, data: List) -> List:
        """
        Cleans the data records.

        :return: the records to clean
        :rtype: the cleaned records
        """
        raise NotImplementedError()

    def clean(self, data: List) -> List:
        """
        Cleans the data records.

        :return: the records to clean
        :rtype: the cleaned records
        """
        self.logger().info("# records before clean: %d" % len(data))
        result = self._do_clean(data)
        self.logger().info("# records after clean: %d" % len(result))
        return result


def parse_cleaner(cleaner: str) -> Cleaner:
    """
    Parses the command-line and instantiates the filter.

    :param cleaner: the command-line to parse
    :type cleaner: str
    :return: the cleaner
    :rtype: Cleaner
    """
    from seppl import split_args, split_cmdline, args_to_objects
    from sdc.registry import available_cleaners

    if cleaner is None:
        raise Exception("No cleaner command-line supplied!")
    valid = dict()
    valid.update(available_cleaners())
    args = split_args(split_cmdline(cleaner), list(valid.keys()))
    objs = args_to_objects(args, valid, allow_global_options=False)
    if len(objs) == 1:
        if isinstance(objs[0], Cleaner):
            result = objs[0]
        else:
            raise Exception("Expected instance of Cleaner but got: %s" % str(type(objs[0])))
    else:
        raise Exception("Expected to obtain one cleaner from '%s' but got %d instead!" % (cleaner, len(objs)))
    return result

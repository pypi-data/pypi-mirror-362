import abc
import argparse
import os
import pickle

from typing import Dict, List

from seppl import MetaDataHandler, get_metadata
from seppl.io import Filter as SFilter
from wai.logging import LOGGING_WARNING

from sdc.api import make_list


class Filter(SFilter, abc.ABC):
    """
    Ancestor for filters.
    """
    pass


class BatchFilter(Filter, abc.ABC):
    """
    Ancestor for filters that work on batches.
    """

    def __init__(self, metadata_key: str = None, batch_order: List[str] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param metadata_key: the key in the metadata that identifies the batches
        :type metadata_key: str
        :param batch_order: the list of batch names for enforcing an order other than alphabetical
        :type batch_order: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.metadata_key = metadata_key
        self.batch_order = batch_order

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-k", "--metadata_key", type=str, help="The key in the meta-data that identifies the batches. NB: sorts the batch names alphabetically by default.", default=None, required=False)
        parser.add_argument("--batch_order", type=str, help="Lists the names of the batches to enforce an order other than alphabetical. Batches that do not appear in this list get appended to the order.", default=None, required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.metadata_key = ns.metadata_key
        self.batch_order = ns.batch_order

    def _requires_list_input(self) -> bool:
        """
        Returns whether lists are expected as input for the _process method.

        :return: True if list inputs are expected by the filter
        :rtype: bool
        """
        return True

    def _pre_process_batch(self, batch):
        """
        Hook method that gets executed before a batch is being processed.

        :param batch: the batch that is about to be processed
        """
        pass

    def _process_batch(self, batch):
        """
        Processes the batch.

        :param batch: the batch to process
        :return: the potentially updated batch
        """
        raise NotImplementedError()

    def _post_process_batch(self, batch):
        """
        Hook method that gets executed after a batch got processed.

        :param batch: the updated batch
        """
        pass

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        if self.metadata_key is None:
            self._pre_process_batch(data)
            batch_new = self._process_batch(data)
            self._post_process_batch(batch_new)
            return batch_new
        else:
            # split data into batches
            batch_data = dict()
            for item in make_list(data):
                # get meta data
                meta = get_metadata(item)
                if meta is None:
                    if not isinstance(item, MetaDataHandler):
                        raise Exception("Cannot access meta-data for type: %s" % str(type(item)))

                batch_name = meta[self.metadata_key]
                if batch_name not in batch_data:
                    batch_data[batch_name] = []
                batch_data[batch_name].append(item)

            # split into batches
            batches = []
            if self.batch_order is not None:
                batch_names = self.batch_order[:]
                for batch_name in sorted(batch_data.keys()):
                    if batch_name not in batch_names:
                        batch_names.append(batch_name)
                self.logger().info("batch names (custom order): %s" % str(batch_names))
            else:
                batch_names = sorted(batch_data.keys())
                self.logger().info("batch names (alphabetical): %s" % str(batch_names))
            for batch_name in batch_names:
                batches.append(batch_data[batch_name])

            # process batches
            result = []
            for batch in batches:
                self._pre_process_batch(batch)
                batch_new = self._process_batch(batch)
                self._post_process_batch(batch_new)
                result.extend(batch_new)
            return result


class TrainableBatchFilter(BatchFilter, abc.ABC):
    """
    Batch filter that get trained with first batch.
    """

    def __init__(self, metadata_key: str = None, always_reset: bool = None, save_to: str = None, load_from: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the handler.

        :param metadata_key: the key in the metadata that identifies the batches
        :type metadata_key: str
        :param always_reset: whether to reset the filter with each new batch
        :type always_reset: bool
        :param save_to: the file to save the trained filter to
        :type save_to: str
        :param load_from: the file to load the trained filter from
        :type load_from: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(metadata_key=metadata_key, logger_name=logger_name, logging_level=logging_level)
        self.always_reset = always_reset
        self.save_to = save_to
        self.load_from = load_from
        self._trained = False
        self._first_batch = None

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--always_reset", action="store_true", help="If enabled, the filter's 'trained' flag gets reset with every batch and the filter retrained each time, rather than only getting trained on the 1st batch and then applied in that form to subsequent batches.")
        parser.add_argument("--save_to", type=str, metavar="FILE", help="The file to save the trained filter to.", default=None, required=False)
        parser.add_argument("--load_from", type=str, metavar="FILE", help="The file to load a trained filter from (instead of training it on the first batch).", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.always_reset = ns.always_reset
        self.save_to = ns.save_to
        self.load_from = ns.load_from

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._trained = False
        if self.always_reset is None:
            self.always_reset = False
        if (self.save_to is not None) and (len(self.save_to) == 0):
            self.save_to = None
        if (self.load_from is not None) and (len(self.load_from) == 0):
            self.load_from = None

    def _supports_serialization(self):
        """
        Returns whether filter can be saved/loaded.

        :return: True if supported
        :rtype: bool
        """
        return False

    def _serialize(self) -> Dict:
        """
        Returns the filter's internal representation to save to disk.

        :return: the data to save
        :rtype: dict
        """
        raise NotImplementedError()

    def _deserialize(self, data: Dict) -> bool:
        """
        Applies the filter's internal representation loaded from disk.

        :param data: the data to instantiate from
        :type data: dict
        :return: whether the filter is considered trained after deserialiation
        :rtype: bool
        """
        raise NotImplementedError()

    def _pre_process_batch(self, batch):
        """
        Hook method that gets executed before a batch is being processed.

        :param batch: the batch that is about to be processed
        """
        super()._pre_process_batch(batch)
        if self.always_reset:
            self._trained = False
        if not self._trained:
            self._first_batch = True
            # load from disk?
            if self._supports_serialization() and (self.load_from is not None):
                path = self.session.expand_placeholders(self.load_from)
                if os.path.exists(path) and os.path.isfile(path):
                    self.logger().info("Loading filter from: %s" % path)
                    with open(path, "rb") as fp:
                        self._trained = self._deserialize(pickle.load(fp))
                else:
                    self.logger().warning("Filter model does not exist or is not a file: %s" % path)

    def _post_process_batch(self, batch):
        """
        Hook method that gets executed after a batch got processed.

        :param batch: the updated batch
        """
        super()._post_process_batch(batch)
        # save to disk?
        if self._supports_serialization():
            if self._first_batch and (self.save_to is not None):
                path = self.session.expand_placeholders(self.save_to)
                pdir = os.path.dirname(path)
                if not os.path.exists(pdir):
                    self.logger().info("Creating dir: %s" % pdir)
                    os.makedirs(pdir)
                self.logger().info("Saving filter to: %s" % path)
                with open(path, "wb") as fp:
                    pickle.dump(self._serialize(), fp)
        self._first_batch = False


def parse_filter(filter_: str) -> Filter:
    """
    Parses the command-line and instantiates the filter.

    :param filter_: the command-line to parse
    :type filter_: str
    :return: the filter
    :rtype: Filter
    """
    from seppl import split_args, split_cmdline, args_to_objects
    from sdc.registry import available_filters

    if filter_ is None:
        raise Exception("No filter command-line supplied!")
    valid = dict()
    valid.update(available_filters())
    args = split_args(split_cmdline(filter_), list(valid.keys()))
    objs = args_to_objects(args, valid, allow_global_options=False)
    if len(objs) == 1:
        if isinstance(objs[0], Filter):
            result = objs[0]
        else:
            raise Exception("Expected instance of Filter but got: %s" % str(type(objs[0])))
    else:
        raise Exception("Expected to obtain one filter from '%s' but got %d instead!" % (filter_, len(objs)))
    return result

import argparse
import os
import zipfile
from io import BytesIO
from zipfile import ZipFile
from typing import List

from seppl import Initializable, init_initializable
from seppl.io import DirectStreamWriter, DirectWriter, DirectBatchWriter
from seppl.placeholders import placeholder_list, PlaceholderSupporter
from wai.logging import LOGGING_WARNING

from sdc.api import StreamWriter, parse_writer, make_list, Spectrum2D, SampleData, DefaultExtensionWriter

COMPRESSION_STORED = "stored"
COMPRESSION_DEFLATED = "deflated"
COMPRESSION_BZIP2 = "bzip2"
COMPRESSION_LZMA = "lzma"
COMPRESSION = [
    COMPRESSION_STORED,
    COMPRESSION_DEFLATED,
    COMPRESSION_BZIP2,
    COMPRESSION_LZMA,
]
COMPRESSION_TYPE = {
    COMPRESSION_STORED: zipfile.ZIP_STORED,
    COMPRESSION_DEFLATED: zipfile.ZIP_DEFLATED,
    COMPRESSION_BZIP2: zipfile.ZIP_BZIP2,
    COMPRESSION_LZMA: zipfile.ZIP_LZMA,
}

DEFAULT_BINARY_EXT = ".bin"
DEFAULT_TEXT_EXT = ".txt"


class ZipWriter(StreamWriter, DirectStreamWriter, DefaultExtensionWriter, PlaceholderSupporter):

    def __init__(self, output_file: str = None, compression: str = None, writer: str = None, extension: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the zip archive to create
        :type output_file: str
        :param compression: the compression to use
        :type compression: str
        :param writer: the base writer commandline to use for writing the spectra/sample data
        :type writer: str
        :param extension: the file extension to use for the spectra/sample data in the zip file (incl dot)
        :type extension: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.compression = compression
        self.writer = writer
        self.extension = extension
        self._fp = None
        self._zipfile = None
        self._writer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-zip"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectra or sample data in a zip file using the specified direct writer."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        if self._writer is None:
            return [Spectrum2D, SampleData]
        else:
            return self._writer.accepts()

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".zip"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The zip file to store the spectra or sample data files in. " + placeholder_list(obj=self), required=True)
        parser.add_argument("-c", "--compression", choices=COMPRESSION, help="The compression to use.", default=COMPRESSION_STORED, required=False)
        parser.add_argument("-w", "--writer", type=str, help="The direct writer to use for writing the data in the zip file.", required=True)
        parser.add_argument("-e", "--extension", type=str, help="The extension to use for the files in the zip file, overrides any default extension that the direct writer may provide.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.compression = ns.compression
        self.writer = ns.writer
        self.extension = ns.extension

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._writer = parse_writer(self.writer)
        if not isinstance(self._writer, DirectWriter):
            raise Exception("Base writer is not a direct writer: %s" % str(type(self._writer)))
        self._writer.session = self.session
        if isinstance(self._writer, Initializable) and not init_initializable(self._writer, "writer"):
            self.logger().error("Failed to initialize writer: %s" % self.writer)
        if self.compression is None:
            self.compression = COMPRESSION_STORED
        self._fp = None
        self._zipfile = None

    def _init_zipfile(self, fp):
        """
        Initializes the zip file.

        :param fp: the file-like object to initialize with
        """
        if self._zipfile is None:
            self._zipfile = ZipFile(fp, mode='w', compression=COMPRESSION_TYPE[self.compression])

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        if self._fp is None:
            self._fp = open(self.session.expand_placeholders(self.output_file), "wb")
        self.write_stream_fp(data, self._fp, True)

    def write_stream_fp(self, data, fp, as_bytes: bool):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        :param fp: the file-like object to write to
        :param as_bytes: whether to write as str or bytes
        :type as_bytes: bool
        """
        self._init_zipfile(fp)
        for item in make_list(data):
            # name for zip file
            if isinstance(item, Spectrum2D):
                name = item.spectrum_name
            elif isinstance(item, SampleData):
                name = item.sampledata_name
            else:
                raise Exception("Unhandled data type: %s" % str(type(item)))
            if self.extension is not None:
                ext = self.extension
            elif isinstance(self._writer, DefaultExtensionWriter):
                ext = self._writer.default_extension
            else:
                if as_bytes:
                    ext = DEFAULT_BINARY_EXT
                else:
                    ext = DEFAULT_TEXT_EXT
                self.logger().warning("Base writer does not have a default extension and no explicit extension specified, falling back on '%s' as extension!" % ext)
            name = os.path.splitext(name)[0] + ext

            # write to buffer
            buffer = BytesIO()
            if isinstance(self._writer, DirectBatchWriter):
                self._writer.write_batch_fp(data, buffer, as_bytes)
            elif isinstance(self._writer, DirectStreamWriter):
                self._writer.write_stream_fp(data, buffer, as_bytes)
            else:
                raise Exception("Unhandled type of direct writer: %s" % str(type(self._writer)))

            # write data to zip file
            self._zipfile.writestr(name, buffer.getvalue())

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        if self._zipfile is not None:
            self._zipfile.close()
            self._zipfile = None
        if self._fp is not None:
            self._fp.close()
            self._fp = None

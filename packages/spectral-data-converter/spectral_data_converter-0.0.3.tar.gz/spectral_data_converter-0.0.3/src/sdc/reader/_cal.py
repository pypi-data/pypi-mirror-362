from wai.spectralio.cal import Reader as SReader

from ._nir import NIRReader


class CALReader(NIRReader):

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-cal"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the spectra in FOSS CAL format."

    def _init_reader(self):
        """
        Initializes the reader.

        :return: the reader
        """
        reader = SReader()
        reader.options = self._compile_options()
        return reader

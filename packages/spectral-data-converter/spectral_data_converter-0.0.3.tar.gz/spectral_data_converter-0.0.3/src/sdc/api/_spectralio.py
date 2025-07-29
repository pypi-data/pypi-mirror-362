from typing import List


class SpectralIOBased:
    """
    Mixin for wai.spectralio-based readers/writers.
    """

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying reader.

        :return: the list of options to use
        :rtype: list
        """
        return []

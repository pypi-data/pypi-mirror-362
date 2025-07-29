import os
from typing import List

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, SampleData, safe_deepcopy, SAMPLE_ID


class SpectrumToSampleData(Filter):
    """
    Extracts the sample data from the spectrum and forwards it.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "spectrum-to-sampledata"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Extracts the sample data from the spectrum and forwards it. Ensures that the sample ID is present."

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
        return [SampleData]

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            name = os.path.splitext(item.spectrum_name)[0]
            sd = safe_deepcopy(item.spectrum.sample_data)
            if SAMPLE_ID not in sd:
                sd[SAMPLE_ID] = item.spectrum.id
            result.append(SampleData(sampledata_name=name, sampledata=sd))

        return flatten_list(result)

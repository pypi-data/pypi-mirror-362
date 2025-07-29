from typing import List

from wai.ma.transformation import RowNorm as WaiRowNorm

from seppl import AliasSupporter
from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class RowNorm(Filter, AliasSupporter):
    """
    Subtracts mean and divides by standard deviation.
    """

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "row-norm"

    def aliases(self) -> List[str]:
        """
        Returns the aliases under which the plugin is known under/available as well.

        :return: the aliases
        :rtype: list
        """
        return ["standard-normal-variate"]

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Subtracts mean and divides by standard deviation. Also known as standard normal variate."

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

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        trans = WaiRowNorm()

        for item_old in make_list(data):
            sp_old = item_old.spectrum
            mat_old = spectrum_to_matrix(sp_old, add_waveno=False)
            mat_new = trans.transform(mat_old)
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp_old.id, waveno=safe_deepcopy(sp_old.waves), sample_data=safe_deepcopy(sp_old.sample_data))
            item_new = Spectrum2D(spectrum_name=item_old.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)

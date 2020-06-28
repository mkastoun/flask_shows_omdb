import pandas as pandas
from ...shows.services.showService import shows_import


def read_excel(file):
    """Gets spreadsheet's and convert to to a dic

        Parameters
        ----------
        file : excel file

        Returns
        -------
        response message
            Returns a success status with a message
        """
    parsed_file = pandas.read_excel(file, 'Sheet1', index_col=None)
    # convert file after parsing it
    array_file = parsed_file.to_dict()
    # call show import function
    shows_import(array_file)
    # prepare response array
    result = {'status': 'success', 'message': 'Excel imported successfully'}

    return result

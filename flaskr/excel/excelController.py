from flask import Blueprint, request, jsonify
from .services.excelService import read_excel

excel = Blueprint('excel', 'excel', url_prefix='/api/excel')


@excel.route("/upload", methods=['POST'])
def excel_upload():
    """Controller responsible to return upload

        Parameters
        ----------
        file : excel file

        Returns
        -------
        JSON
            JSON RESPONSE
        """
    uploaded_excel_file = request.files.get('file')
    import_result = read_excel(uploaded_excel_file)
    return jsonify({'result': import_result})

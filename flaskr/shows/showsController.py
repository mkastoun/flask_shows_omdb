from flask import Blueprint, request, jsonify, make_response, render_template
from .services.showService import get_list_of_shows_type, generate_shows_pdf
from ..exceptionHandler import InvalidUsage

shows = Blueprint('shows', 'shows', url_prefix='/api/shows')


@shows.route('/<show_type>', methods=['GET'])
def get_show_index(show_type):
    """Controller responsible to return list of shows type

        Parameters
        ----------
        show_type : show type string

        Returns
        -------
        JSON
            list of shows
        """
    args = request.args
    available_show_types = ['movie', 'episode', 'series']
    if show_type not in available_show_types:
        raise InvalidUsage('Invalid Type title, expected titles: movie,episode,series', status_code=422)
    else:
        offset = args.get('offset') if 'offset' in args else 0
        limit = args.get('limit') if 'limit' in args else 10
        result = get_list_of_shows_type(show_type, offset, limit)

    return jsonify({'result': result})


@shows.route('/pdf-export', methods=['GET'])
def pdf_export():
    """Controller responsible to link of the pdf

        Returns
        -------
        JSON
            list of shows
        """
    generated_pdf_path = generate_shows_pdf()
    public_path = request.host + '/' + generated_pdf_path
    return jsonify({'result': {'url': public_path}})

from ...models import Shows
from ...sql_extensions import db
import omdb
from ...exceptionHandler import InvalidUsage
from ...models import Directors
from datetime import date
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


def shows_import(data):
    """Gets the shows names, type and directors and insert them to the database

        Parameters
        ----------
        data : dic of list of movies

        """
    # loop through the data and get the first cell that indicate the show type
    for show_type in data:
        available_show_types = ['movie', 'episode', 'series']
        # if the sent type not within the required list an exception is thrown
        if show_type not in available_show_types:
            raise InvalidUsage('Invalid Type title, expected titles: movie,episode,series', status_code=422)
        else:
            # loop through the rest of the array
            for show_key, show_name in data[show_type].items():
                # call function to get the director id from the movie's name
                director_id = get_movie_director(show_name, show_type)
                # insert the new record to the database
                shows = Shows(show_name=show_name, show_type=show_type, director_id=director_id)
                db.session.add(shows)
                db.session.commit()


def get_movie_director(show_name, show_type='movie'):
    """Make API call to OMDB to get the director name, save it to the database, and return the id

        Parameters
        ----------
        show_name : Show name string
        show_type : Show type string

        Returns
        -------
        Id
            Return the director id OR None
        """
    # make API call to the OMDB
    show_info = omdb.get(title=show_name, media_type=show_type, fullplot=False)
    # get the director Id
    movie_director = show_info.get('director')
    # if its available the we insert/get and return their ID
    if movie_director is not None:
        movie_director_id = get_or_create_director_id(movie_director)
        return movie_director_id
    else:
        return None


def get_or_create_director_id(director_name):
    """Find or create the given director name and return its id

        Parameters
        ----------
        director_name : director name string

        Returns
        -------
        Id
            Return the director id
        """
    # search for a director
    director_name_search = "%{}%".format(director_name)
    director_obj = Directors.query.filter(Directors.director_name.like(director_name_search)).first()
    # if not found create one
    if director_obj is None:
        director = Directors(director_name=director_name)
        db.session.add(director)
        db.session.commit()
        director_obj = director
    return director_obj.id


def get_list_of_shows_type(show_type='movie', offset: int = 0, limit: int = 10):
    """Return list of shows and their directors based on the type offset and limit

        Parameters
        ----------
        show_type : show type string
        offset : start int
        limit : end int

        Returns
        -------
        dict
            Return the list shows
        """
    result = []
    # query to get the shows
    shows = db.session.query(Shows, Directors).outerjoin(Directors).filter(Shows.show_type == show_type).offset(
        offset).limit(limit).all()
    for row in shows:
        # if the director name is not available replace name with 'N/A'
        if row.Directors is None:
            director_name = 'N/A'
        else:
            director_name = row.Directors.director_name
        # build the response
        shows_list = {'show_name': row.Shows.show_name, 'director_name': director_name}
        result.append(shows_list)
    return result


def get_list_of_all_shows():
    """Return all shows and their directors
        Returns
        -------
        dict
            Return the list shows
        """
    result = []
    # query to get the shows
    shows = db.session.query(Shows, Directors).outerjoin(Directors).all()
    for row in shows:
        if row.Directors is None:
            director_name = 'N/A'
        else:
            director_name = row.Directors.director_name
        # build the response
        shows_list = {
            'show_type': row.Shows.show_type, 'show_name': row.Shows.show_name, 'director_name': director_name
            }
        result.append(shows_list)
    return result


def generate_shows_pdf():
    """Build the pdf of all the shows

        Returns
        -------
        string
            Url of the string
        """
    # get the list of shows
    list_of_shows_details = get_list_of_all_shows()
    # get today in iso format
    today = date.today().isoformat()
    # concat file name and file path
    file_name = "show_report_" + today + ".pdf"
    file_path = "flaskr/static/exports/pdf/" + file_name
    # set w and h of the A4 paper
    width, height = A4
    # init canvas
    pdf = Canvas(file_path)
    # set document title
    pdf.setTitle(file_name)
    # Set pdf Title
    pdf.setFont("Courier-Bold", 16)
    pdf.drawString(200, 770, "Shows report on " + today)
    # set sub title
    pdf.setFont("Courier-Bold", 14)
    pdf.drawCentredString(100, 720, "Show Type")
    pdf.drawCentredString(280, 720, "Show Name")
    pdf.drawCentredString(460, 720, "Director Name")
    pdf.setFont("Courier-Bold", 10)
    # building a table for returned shows
    data = []
    # prepare shows data
    for show_details in list_of_shows_details:
        data.append([show_details['show_type'], show_details['show_name'], show_details['director_name']])
    # apply it to the table
    table = Table(data, colWidths=[2.4 * inch] * 3)
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 75, 640)
    # save it
    pdf.save()

    return "static/exports/pdf/" + file_name

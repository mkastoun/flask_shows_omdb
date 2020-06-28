# Module Imports
import mariadb
import sys
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        try:
            conn = mariadb.connect(
                user="root",
                password="",
                host="127.0.0.1",
                port=3306,
                database="neo_theater"
                )
            g.db = conn.cursor()
        except mariadb.Error as e:
                print("Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('migrations\\disable_foreign_key_check.sql') as c:
            db.execute(c.read().decode('utf8'))
    with current_app.open_resource('migrations\\clean_schema.sql') as c:
            db.execute(c.read().decode('utf8'))
    with current_app.open_resource('migrations\\directors_schema.sql') as d:
            db.execute(d.read().decode('utf8'))
    with current_app.open_resource('migrations\\shows_schema.sql') as d:
            db.execute(d.read().decode('utf8'))
    with current_app.open_resource('migrations\\enable_foreign_key_check.sql') as c:
            db.execute(c.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

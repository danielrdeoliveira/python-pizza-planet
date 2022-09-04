import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
from seeder.seeder import seed_database
# flake8: noqa
from app.repositories.models import Ingredient, Order, OrderDetail, Size, Beverage


manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])


@manager.command('seed_it')
def seed():
    return seed_database()


@manager.command('delete_everything')
def delete_all():
    models = [Beverage, Ingredient, Order, OrderDetail, Size]
    try:
        for model in models:
            num_rows_deleted = model.query.delete()
            print(f'{num_rows_deleted} deleted for the {model.__name__} model')
        db.session.commit()
    except RuntimeError:
        print('An error occurred, rolling back the commit')
        db.session.rollback()


if __name__ == '__main__':
    manager()

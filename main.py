from flask_restful import Api
from flasgger import Swagger
from src.rest.rest_api import FindAllData, output_json, output_xml, GroupWithLessCount, CourseWithStudent
from src.config import Config
from src.rest.crud_rest import AddStudent, DeleteStudent, AddStudentToTheCourse, RemoveStudentFromTheCourse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.db.models import db
from sqlalchemy import create_engine


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Flask Restful Swagger",
            "description": "API for Report",
            "version": "0.0.1",
            "contact": {
                "responsibleDeveloper": "Oleksandr Adrianov",
                "email": "sanyadrian@ukr.net"
            },
            "license": {
                "name": "Apache License 2.0"
            },
        },
        "schemes": ["http", "https"]
    }

    app.config["SWAGGER"] = {
        "title": "SQL",
        "uiversion": 3,
        "doc_dir": "/SQL/"
    }
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app, default_mediatype='application/json', prefix='/api/v1')
    swagger = Swagger(app, template=template)
    api.representations['application/xml'] = output_xml
    api.representations['application/json'] = output_json
    api.add_resource(FindAllData, '/all_data')
    api.add_resource(GroupWithLessCount, '/groups')
    api.add_resource(CourseWithStudent, '/courses')
    api.add_resource(AddStudent, '/new_students')
    api.add_resource(DeleteStudent, '/deleted_student')
    api.add_resource(AddStudentToTheCourse, '/student_course')
    api.add_resource(RemoveStudentFromTheCourse, '/removed_student')
    return app


if __name__ == '__main__':
    app = create_app(Config)
    app.run(debug=True)

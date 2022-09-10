from flask_restful import Resource
from src.db.models import StudentModel, GroupModel, CourseModel, db
from flask import make_response, request, session
from src.rest.rest_config import session_scope
from sqlalchemy import select, func
from simplexml import dumps
from flask.views import MethodView
import typing as t
import json


def output_json(data, code, headers=None):
    resp = make_response(json.dumps({'response': data}, default=str), code)
    resp.headers.extend(headers or {})
    return resp


def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp


def dict_info(info: t.List[StudentModel]) -> t.List[t.Dict]:
    info = [
        {
            'group_id': i.group_id,
            'first_name': i.first_name,
            'last_name': i.last_name
        } for i in info
    ]
    return info


def get_students():
    students = StudentModel.query.all()
    return students


class FindAllData(Resource):
    def get(self):
        """
        file: yaml/find_all.yml
        """
        return dict_info(get_students())


def get_groups_with_less_or_equal_count(count):
    q = select([
        GroupModel.name,
        func.count()]
    ).join(StudentModel.groups).group_by(GroupModel.name).having(
        func.count() <= count)
    result = db.session.execute(q)
    return result


def dict_groups(info: t.List[StudentModel]) -> t.List[t.Dict]:
    data = [
        {
            'name': i.name,
            'count': i.count
        } for i in info
    ]
    return data


class GroupWithLessCount(MethodView):
    def get(self):
        """
        file: yaml/groups_equals_or_less.yml
        """
        if 'count' in request.args:
            count = request.args.get('count')
            groups = dict_groups(get_groups_with_less_or_equal_count(count))
            return groups


def get_student_with_course(name):
    query = select(StudentModel, CourseModel.name
                   ).join(
        CourseModel, StudentModel.courses).where(CourseModel.name == name)
    result = list(db.session.execute(query))
    return result


def convert_to_dict(info: t.List[t.List]) -> t.List[t.Dict]:
    data = [
        {
            'id': i[0].id,
            'group_id': i[0].group_id,
            'first_name': i[0].first_name,
            'last_name': i[0].last_name,
            'name': i[1]
        } for i in info
    ]
    return data


class CourseWithStudent(MethodView):
    def get(self):
        """
        file: yaml/courses.yml
        """
        if 'name' in request.args:
            name = request.args.get('name')
            course = convert_to_dict(get_student_with_course(name))
            return course

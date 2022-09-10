from flask_restful import Resource
from sqlalchemy import delete
from src.db.models import StudentModel, CourseModel
from flask import request
from src.rest.rest_config import session_scope
import typing as t
from src.db.models import db
import json


def add_new_student(group_id, first_name, last_name):
    student = StudentModel(group_id, first_name, last_name)
    db.session.add(student)
    db.session.commit()
    return [student]


def convert_to_dict(info: t.List[StudentModel]) -> t.List[t.Dict]:
    data = [
        {
            'id': i.id,
            'group_id': i.group_id,
            'first_name': i.first_name,
            'last_name': i.last_name,
        } for i in info
    ]
    return data


class AddStudent(Resource):
    def post(self):
        """
        file: yaml/add_student.yml
        """
        result = convert_to_dict(add_new_student(**json.loads(request.data)))

        return result


def delete_new_student(student_id):
    student = delete(StudentModel).where(StudentModel.id == student_id).returning(StudentModel)
    result = db.session.execute(student).fetchall()
    db.session.commit()
    return result


def convert_to_dict_delete_student(info: t.List[t.Tuple]) -> t.List[t.Dict]:
    data = [
        {
            'student_id': i[0]
        } for i in info
    ]
    return data


class DeleteStudent(Resource):
    def delete(self):
        """
        file: yaml/delete_student.yml
        """
        result = convert_to_dict_delete_student(delete_new_student(**json.loads(request.data)))
        return result


def remove_student_from_his_courses(student_id, course_id):
    students = StudentModel.query.filter_by(id=student_id)[0]
    course = CourseModel.query.filter_by(id=course_id)[0]
    students.courses.remove(course)
    db.session.commit()
    return [(student_id, course_id),]


def convert_to_dict_remove_student(info: t.List[StudentModel]) -> t.List[t.Dict]:
    data = [
        {
            'student_id': i[0],
            'course_id':  i[1]
        } for i in info
    ]
    return data


class RemoveStudentFromTheCourse(Resource):
    def post(self):
        """
        file: yaml/remove_student.yml
        """
        result = convert_to_dict_remove_student(
            remove_student_from_his_courses(**json.loads(request.data)))

        return result


def add_student_to_the_course(student_id, course_id):
    students = StudentModel.query.filter_by(id=student_id)[0]
    course = CourseModel.query.filter_by(id=course_id)[0]
    students.courses.append(course)
    db.session.commit()
    return [(student_id, course_id)]


def convert_to_dict_add_student(info: t.List[StudentModel]) -> t.List[t.Dict]:
    data = [
        {
            'student_id': i[0],
            'course_id': i[0],
        } for i in info
    ]
    return data


class AddStudentToTheCourse(Resource):
    def post(self):
        """
        file: yaml/add_student_to_the_course.yml
        """
        result = convert_to_dict_add_student(
            add_student_to_the_course(**json.loads(request.data)))

        return result

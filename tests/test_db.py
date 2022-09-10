import pytest
from src.db.models import *
from src.rest.crud_rest import add_student_to_the_course


COURSES = {
    'Software engineering': 'description Software engineering',
    'Data Science': 'description Data Science'
}

@pytest.mark.usefixtures('db')
class TestStudentModel:
    def test_student_get_by_id(self):
        """Get student by ID."""
        student = StudentModel(1, 'asda', 'asd')
        db.session.add(student)
        retrieved = StudentModel.query.filter_by(id=1).first()
        assert retrieved == student

    def test_course_get_by_id(self):
        course = CourseModel('test', 'test')
        db.session.add(course)
        retrieved = CourseModel.query.filter_by(id=1).first()
        assert retrieved == course

    def test_group_get_by_id(self):
        group = GroupModel('test')
        db.session.add(group)
        retrieved = GroupModel.query.filter_by(id=1).first()
        assert retrieved == group

    def test_add_student_to_the_course(self):
        student = StudentModel(1, 'test', 'test')
        course = CourseModel('asd', 'asd')
        course_2 = CourseModel('asdas', 'asdd')
        db.session.add(student)
        db.session.add(course)
        db.session.add(course_2)
        add_student_to_the_course(1, 1)
        assert course in student.courses
        assert course_2 not in student.courses
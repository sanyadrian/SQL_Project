import pytest
from src.db.models import *
from src.config import Config
from tests.conftest import client


@pytest.mark.usefixtures('db')
def test_groups_with_less_or_equal_count(client, count=1):
    student_1 = StudentModel(1, 'asda', 'asd')
    student_2 = StudentModel(2, 'asdaa', 'asdd')
    student_3 = StudentModel(1, 'aasda', 'adsd')
    group_1 = GroupModel('test')
    group_2 = GroupModel('test_2')
    db.session.add(student_1)
    db.session.add(student_2)
    db.session.add(student_3)
    db.session.add(group_1)
    db.session.add(group_2)
    response = client.get(f'/api/v1/groups?count={count}')
    assert response.status_code == 200


@pytest.mark.usefixtures('db')
def test_students_with_courses(client):
    student_1 = StudentModel(1, 'asda', 'asd')
    student_2 = StudentModel(2, 'asdaa', 'asdd')
    student_3 = StudentModel(1, 'aasda', 'adsd')
    course_1 = CourseModel('test', 'test')
    course_2 = CourseModel('test_2', 'test_2')
    student_1.courses.append(course_1)
    student_2.courses.append(course_2)
    student_3.courses.append(course_1)
    db.session.add(student_1)
    db.session.add(student_2)
    db.session.add(student_3)
    db.session.add(course_1)
    db.session.add(course_2)
    db.session.commit()
    response = client.get(f'/api/v1/courses?name=test')
    assert 'asda' in response.json['response'][0]['first_name']
    assert response.status_code == 200



@pytest.mark.usefixtures('db')
def test_groups_with_less_or_equal_count(client):
    import json
    group_1 = GroupModel('test')
    db.session.add(group_1)
    data = {
            'group_id': 1,
            'first_name': 'asd',
            'last_name': 'asd',
        }
    response = client.post(f'/api/v1/new_students', data=json.dumps(data))
    assert 'asd' in response.json['response'][0]['first_name']
    assert response.status_code == 200


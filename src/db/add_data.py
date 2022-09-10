from src.db.models import *
from src.db.data import *
from sqlalchemy import select
from src.rest.rest_config import session_scope

db.create_all()


def add_data_into_course():
    for k, v in COURSES.items():
        db.session.add(CourseModel(k, v))
        db.session.commit()


def add_data_into_groups():
    groups = data_creator_groups()
    for k in groups:
        db.session.add(GroupModel(k))
        db.session.commit()


def add_data_into_students():
    students = data_creator_students(FIRST_NAMES, LAST_NAMES)
    groups = {i: list() for i in range(1, 11)}
    groups = assign_students_to_groups(students, groups)
    for k, v in groups.items():
        for i in v:
            f_name, l_name = i
            db.session.add(StudentModel(k, f_name, l_name))
    db.session.commit()


def add_data_into_student_course():
    # with session_scope() as s:
    for i in range(1, 201):
        courses_id = assign_students_to_courses()
        students_query = select(StudentModel).where(StudentModel.id == i)
        student = list(s.execute(students_query))[0][0]
        courses_query = select(CourseModel).where(CourseModel.id.in_(courses_id))
        courses = [i[0] for i in s.execute(courses_query)]
        student.courses.extend(courses)
    # db.session.commit()


if __name__ == "__main__":
    # add_data_into_course()
    # add_data_into_groups()
    # add_data_into_students()
    add_data_into_student_course()
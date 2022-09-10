from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


db = SQLAlchemy()


association_table = db.Table(
    'student_course',
    db.Column('student_id', db.ForeignKey('student.id', ondelete="CASCADE"), primary_key=True),
    db.Column('course_id', db.ForeignKey('course.id'), primary_key=True)
)


class GroupModel(db.Model):
    __tablename__ = 'group'
    id = Column(Integer(), primary_key=True)
    name = Column(String(25), nullable=False)
    student = db.relationship('StudentModel', back_populates='groups', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class StudentModel(db.Model):
    __tablename__ = 'student'
    id = Column(Integer(), primary_key=True)
    group_id = Column(Integer(), ForeignKey('group.id'))
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)

    groups = db.relationship('GroupModel', backref=db.backref('students', lazy=True))
    courses = db.relationship('CourseModel', cascade='all, delete', passive_deletes=True,
                              secondary=association_table,
                              backref=db.backref('students', lazy=True))

    def __init__(self, group_id, first_name, last_name):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name


class CourseModel(db.Model):
    __tablename__ = 'course'
    id = Column(Integer(), primary_key=True)
    name = Column(String(25), nullable=False)
    description = Column(String(50), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description


if __name__ == "__main__":
    db.create_all()

# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:root@localhost/51cto?charset=utf8mb4')
Base = declarative_base()
metadata = MetaData(engine)

class Train(Base):
    __tablename__ = 'train'
    id = Column(Integer,primary_key=True,autoincrement=True)
    train_id = Column(Integer, nullable=False)
    train_name = Column(VARCHAR(60), nullable=False)
    course_num = Column(Integer, nullable=False)
    status = Column(Integer,default=0)

class Train_course(Base):
    __tablename__ = 'train_course'
    id = Column(Integer,primary_key=True,autoincrement=True)
    tra_id = Column(Integer, ForeignKey('train.id'), nullable=False)
    train_course_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    course_name = Column(VARCHAR(100), nullable=False)
    number = Column(Integer, nullable=False)
    lesson_num = Column(Integer, nullable=False)
    status = Column(Integer,nullable=False, default=0)

class Course_lesson(Base):
    __tablename__ = 'course_lesson'
    id = Column(Integer,primary_key=True,autoincrement=True)
    cou_id = Column(Integer, ForeignKey('train_course.id'), nullable=False)
    lesson_name = Column(VARCHAR(60), nullable=False)
    lesson_id = Column(Integer, nullable=False)
    video_id  = Column(Integer, nullable=False)
    video_url = Column(VARCHAR(100), nullable=False)
    video_num = Column(Integer, nullable=False)

#创建表 create table
metadata.create_all()

# #创建session
# session = sessionmaker(bind=engine)
# session = session()
#
# #增
# tra = Train(train_id=train_id, train_name = train['name'], course_num = train['course_num'])
# session.add(tra)
# session.commit()
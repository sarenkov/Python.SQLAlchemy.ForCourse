from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
import urllib
from urllib import parse

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=New;UID=Tester;PWD=123456")

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, echo=True)

Base = declarative_base()


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String)
    second_name = Column(String)
    poem = relationship('Poem', backref='Authors')


class Poem(Base):
    __tablename__ = 'PoemsTitles'
    id = Column(Integer, primary_key=True, nullable=False)
    poem_title = Column(String)
    author_id = Column(Integer, ForeignKey('Authors.id'), nullable=False)


class FirstQuatrain(Base):
    __tablename__ = 'FirstQuatrains'
    id = Column(Integer, primary_key=True, nullable=False)
    quatrain = Column(Text)
    poem_title_id = Column(Integer, ForeignKey('PoemsTitles.id'), nullable=False)


class SecondQuatrain(Base):
    __tablename__ = 'SecondQuatrains'
    id = Column(Integer, primary_key=True, nullable=False)
    parts = Column(Text)
    order_number = Column(Integer)
    first_quatrain_id = Column(Integer, ForeignKey('FirstQuatrains.id'), nullable=False)


class Result(Base):
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True, nullable=False)
    student_name = Column(String)
    poem_author = Column(String)
    poem_title = Column(String)
    poem_text = Column(Text)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

author_first = Author(first_name='Ivan', second_name='Rud')
session.add(author_first)
session.commit()

poem = Poem(
    poem_title='Чудное мгновение1111',
    author_id = session.query(Author).filter_by(
        first_name=author_first.first_name,
        second_name=author_first.second_name).first().id)

session.add(poem)
session.commit()



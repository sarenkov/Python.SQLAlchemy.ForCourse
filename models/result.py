from sqlalchemy import Column, Integer, String, Text, create_engine
from db_connector.db_connector import Base


class Result(Base):
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True, nullable=False)
    student_name = Column(String)
    poem_author = Column(String)
    poem_title = Column(String)
    poem_text = Column(Text)

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

from sqlalchemy import Column, Integer, String, Text, create_engine
from db_connector.db_connector import Base


class Result(Base):
    __tablename__ = 'Answers'
    id = Column(Integer, primary_key=True, nullable=False)
    student_name = Column(String(collation='Cyrillic_General_CS_AS'))
    poem_author = Column(String(collation='Cyrillic_General_CS_AS'))
    poem_title = Column(String(collation='Cyrillic_General_CS_AS'))
    poem_text = Column(Text(collation='Cyrillic_General_CS_AS'))

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

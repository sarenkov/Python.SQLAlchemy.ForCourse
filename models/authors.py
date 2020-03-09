import uuid

from sqlalchemy import Column, Integer, String, create_engine, BLOB, CHAR
from sqlalchemy.orm import relationship

from db_connector.db_connector import Base


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(CHAR(32), primary_key=True, nullable=False, default=lambda: uuid.uuid4().hex, autoincrement=False)
    objectid = Column(String(collation='Cyrillic_General_CS_AS'))
    first_name = Column(String(collation='Cyrillic_General_CS_AS'))
    second_name = Column(String(collation='Cyrillic_General_CS_AS'))
    poem = relationship('Poem', backref='Authors')

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

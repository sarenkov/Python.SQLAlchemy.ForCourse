from sqlalchemy import Column, Integer, String, create_engine, Binary
from sqlalchemy.orm import relationship

from db_connector.db_connector import Base


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True, nullable=False)
    objectid = Column(String(collation='Cyrillic_General_CS_AS'))
    first_name = Column(String(collation='Cyrillic_General_CS_AS'))
    second_name = Column(String(collation='Cyrillic_General_CS_AS'))
    poem = relationship('Poem', backref='Authors')

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

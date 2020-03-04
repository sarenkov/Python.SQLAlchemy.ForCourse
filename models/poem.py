from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Binary
from sqlalchemy.orm import relationship

from db_connector.db_connector import Base


class Poem(Base):
    __tablename__ = 'PoemsTitles'
    id = Column(Integer, primary_key=True, nullable=False)
    objectid = Column(String(collation='Cyrillic_General_CS_AS'))
    poem_title = Column(String(collation='Cyrillic_General_CS_AS'))
    author_id = Column(Integer, ForeignKey('Authors.id'), nullable=False)
    firstQuatrain = relationship('FirstQuatrain', backref='PoemsTitles')

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, BLOB, CHAR
from sqlalchemy.orm import relationship

from db_connector.db_connector import Base


class Poem(Base):
    __tablename__ = 'PoemsTitles'
    id = Column(CHAR(32), primary_key=True, nullable=False, default=lambda: uuid.uuid4().hex, autoincrement=False)
    objectid = Column(String(collation='Cyrillic_General_CS_AS'))
    poem_title = Column(String(collation='Cyrillic_General_CS_AS'))
    author_id = Column(CHAR(32), ForeignKey('Authors.id'), nullable=True)
    firstQuatrain = relationship('FirstQuatrain', backref='PoemsTitles')

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

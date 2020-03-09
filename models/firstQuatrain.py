import uuid

from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine, String, CHAR
from sqlalchemy.orm import relationship

from db_connector.db_connector import Base


class FirstQuatrain(Base):
    __tablename__ = 'FirstQuatrains'
    id = Column(CHAR(32), primary_key=True, nullable=False, default=lambda: uuid.uuid4().hex, autoincrement=False)
    objectid = Column(String(collation='Cyrillic_General_CS_AS'))
    quatrain = Column(Text(collation='Cyrillic_General_CS_AS'))
    poem_title_id = Column(CHAR(32), ForeignKey('PoemsTitles.id'), nullable=False)
    secondQuatrain = relationship('SecondQuatrain', backref='FirstQuatrains')

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

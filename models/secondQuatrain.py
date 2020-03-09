import uuid

from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine, String, CHAR
from db_connector.db_connector import Base


class SecondQuatrain(Base):
    __tablename__ = 'SecondQuatrains'
    id = Column(CHAR(32), primary_key=True, nullable=False, default=lambda: uuid.uuid4().hex, autoincrement=False)
    objectid = Column(String)
    parts = Column(String)
    order_number = Column(Integer)
    first_quatrain_id = Column(CHAR(32), ForeignKey('FirstQuatrains.id'), nullable=False)

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

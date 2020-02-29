from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine, String
from db_connector.db_connector import Base


class SecondQuatrain(Base):
    __tablename__ = 'SecondQuatrains'
    id = Column(Integer, primary_key=True, nullable=False)
    objectid = Column(String)
    parts = Column(String)
    order_number = Column(Integer)
    first_quatrain_id = Column(Integer, ForeignKey('FirstQuatrains.id'), nullable=False)

    def create(cls, connector):
        engine = create_engine(connector.engine_url_to_db)
        Base.metadata.create_all(engine)

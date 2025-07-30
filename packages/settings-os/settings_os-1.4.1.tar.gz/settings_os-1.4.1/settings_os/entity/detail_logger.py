from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from datetime import datetime


Base: DeclarativeMeta = declarative_base()


class DetailLogger(Base):
    __tablename__ = 'TBL_RPA_DETAIL_LOGGER'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    RPA = Column(String)
    level = Column('TIPO', String, nullable=True)
    message = Column('MENSAGEM', String, nullable=True)
    file = Column('MODULO', String, nullable=True)
    line = Column('LINHA', String, nullable=True)
    function = Column('FUNCAO', String, nullable=True)
    timestamp = Column('DT_CARGA', DateTime, default=datetime.now)


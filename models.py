import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currency'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    rate = relationship("Rate", back_populates="currency")


class Rate(Base):
    __tablename__ = 'rate'
    id = sa.Column(sa.Integer, primary_key=True)
    currency_id = sa.Column(sa.ForeignKey(Currency.id))
    date = sa.Column(sa.DateTime)
    rate = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    currency = relationship("Currency", back_populates="rate")


def create_tables(engine):
    Base.metadata.create_all(engine)


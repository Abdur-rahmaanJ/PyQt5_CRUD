from sqlalchemy import Column, String, Integer, Date

from base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    barcode = Column(String)
    name = Column(String)
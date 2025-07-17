from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MasterFile(Base):
    __tablename__ = 'MASTER_FILE'
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    suppliernumber = Column(String)
    suppliername = Column(String)
    suppliercontactname = Column(String)
    suppliercontactemail = Column(String)
    suppliermanufacturinglocation = Column(String)
    PartNumber = Column(String, index=True)
    partname = Column(String)
    material = Column(String)
    currency = Column(String)
    # Volumen y precios: solo ejemplo, agregar más columnas según sea necesario
    voljan2023 = Column(Numeric)
    volfeb2023 = Column(Numeric)
    volmar2023 = Column(Numeric)
    # ... continuar para todos los meses ...
    pricejan2023 = Column(Numeric)
    pricefeb2023 = Column(Numeric)
    pricejun2023 = Column(Numeric)
    # ... continuar para todos los meses ...
    Pricemktindexjan2023 = Column(Numeric)
    Pricemktindexfeb2023 = Column(Numeric)
    # ... continuar para todos los meses ... 
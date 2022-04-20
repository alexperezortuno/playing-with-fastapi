from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    description = Column(String, index=True)
    type = Column(String, index=True)
    color = Column(String, index=True)
    year = Column(Integer, index=True)

    def __repr__(self):
        return "<Car(brand='%s', model='%s', year='%s', type='%s', color='%s', year='%s')>" % (self.brand, self.model, self.year, self.type, self.color, self.year)

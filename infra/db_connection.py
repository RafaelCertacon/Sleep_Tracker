from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


db = create_engine("mssql+pymssql://rafael.rocha:Certa%402024@192.168.0.26/teste")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class SleepTracker(Base):
    __tablename__ = 'sleep_tracker'
    id = Column(Integer, primary_key=True)
    dia_dormir = Column(String, nullable=False)
    dia_acordar = Column(String, nullable=False)
    hora_dormir = Column(String, nullable=False)
    hora_acordar = Column(String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'dia_dormir': self.dia_dormir,
            'dia_acordar': self.dia_acordar,
            'hora_dormir': self.hora_dormir,
            'hora_acordar': self.hora_acordar
        }

Base.metadata.create_all(db)

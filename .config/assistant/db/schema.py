import os
from sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base = declarative_base()
Session = sessionmaker(bind=engine)

clt_sequnce = Sequence("clt_sequence")
oss_sequnce = Sequence("oss_sequence")
exp_sequnce = Sequence("exp_sequence")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String) # CLT, OSS, EXP
    project_type_id = Column(Integer, nullable=False)
    status = Column(String) # Active, Completed, Frozen, Cancelled
    client_name = Column(String)
    priority = Column(String) # Weak, Normal, High, Code Red
    description = Column(String)
    created_at = Column(DateTime)
    due_at = Column(DateTime)

# To create the table in the database:
Base.metadata.create_all(engine)
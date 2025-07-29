from sqlalchemy import create_engine, Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class BuildJob(Base):
    __tablename__ = 'build_jobs'

    job_id = Column(String, primary_key=True)
    soc = Column(String)
    device = Column(String)
    interface = Column(String)
    os_type = Column(String)
    status = Column(String)      # queued, running, done, error
    progress = Column(Integer)
    logs = Column(Text)
    output_file = Column(String)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime)
    Query_Input = Column(String)
    Query_Output = Column(String)

engine = create_engine("postgresql://dd_user:dd_pass@localhost/dd_forge_db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

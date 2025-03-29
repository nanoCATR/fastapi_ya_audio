from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, ForeignKey

metadata = MetaData()


user = Table(
    "user",
    metadata,
    Column('id', Integer, primary_key=True, index=True), 
    Column('client_id', String, nullable=False), 
    Column('login', String, nullable=False), 
    Column('display_name', String, nullable=False), 
    Column('default_email', String, nullable=False),
    Column('is_admin', Boolean, default=False, nullable=False)
)

audio = Table(
    "audio",
    metadata,
    Column('id', Integer, primary_key=True, index=True), 
    Column('filename', String, nullable=False), 
    Column('location', String, nullable=False), 
    Column('user_owner', Integer, ForeignKey("user.id"))
)
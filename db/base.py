from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, ForeignKey, String, Integer, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase, mapped_column, Mapped

from db.session import engine, get_session

from datetime import date

class Base(DeclarativeBase):
    pass

class DefaultTable(Base):
    __tablename__ = "default_table"
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    first_name: str = Column(String(255))
    last_name: str = Column(String(255))
    date_of_birth: date = Column(Date)
    
    user = relationship("User", back_populates="default_table")
    
class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    default_table = relationship("DefaultTable", back_populates="user")
    
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
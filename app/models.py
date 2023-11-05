from .database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__="S_posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content =Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE', nullable=False)
    owner_id = Column(Integer,ForeignKey("S_users.id",ondelete="CASCADE"),nullable =False)
    owner = relationship("User")
    # created_at = Column(TIMESTAMP(timezone=True),
    #                     nullable=False,server_default=text('GETDATE()'))

class User(Base):
    __tablename__="S_users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String(255),nullable=False,unique=True)
    password = Column(String,nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True),
    #                     nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__="S_votes"

    user_id = Column(Integer,ForeignKey("S_users.id",ondelete="CASCADE"),primary_key=True,nullable =False)
    post_id = Column(Integer,ForeignKey("S_posts.id",ondelete="NO ACTION"),primary_key=True,nullable =False)

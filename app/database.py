from sqlalchemy import create_engine, Integer, String, Float, Column, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine('sqlite:///posts.db', echo=True)

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    author = Column(String)
    created_at = Column(Float)
    genres = Column(String)
    
    classes = relationship("AttendingClasses", back_populates="post")   

class AttendingClasses(Base):
    __tablename__ = 'attending_classes'
    post_id = Column(Integer, ForeignKey('blog_posts.id', ondelete='CASCADE'), primary_key=True)
    class_id = Column(SmallInteger, primary_key=True)

    post = relationship("BlogPost", back_populates="classes")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

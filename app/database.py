from sqlalchemy import create_engine, Integer, String, Float, Column, Text, SmallInteger, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine('sqlite:///posts.db', echo=True)

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String)
    date = Column(String)
    genre = Column(String, nullable=False)
    cover_image = Column(Integer)

    classes = relationship("AttendingClasses", back_populates="post")
    photos = relationship("Photo", back_populates="post")   

class AttendingClasses(Base):
    __tablename__ = 'attending_classes'
    post_id = Column(Integer, ForeignKey('blog_posts.id', ondelete='CASCADE'), primary_key=True)
    class_id = Column(SmallInteger, primary_key=True)

    post = relationship("BlogPost", back_populates="classes")

class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('blog_posts.id', ondelete='CASCADE'), nullable=True)
    file_path = Column(String, nullable=False)
    taken_at = Column(String, nullable=True) #probably make nullable false once i have a date picker

    post = relationship("BlogPost", back_populates="photos")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

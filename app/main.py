from fastapi import FastAPI, Request, Depends, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, BlogPost, Photo, AttendingClasses
import os
import uuid
import unicodedata
import re

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/lg-assets", StaticFiles(directory="node_modules/lightgallery"), name="lgassets")


templates = Jinja2Templates(directory="templates")


def slugify(value: str) -> str:
    # Normalize unicode characters (e.g., č -> c)
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    # Lowercase and replace non-word characters/spaces with dashes
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', '-', value)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
     # Get the latest two posts
    latest_posts = db.query(BlogPost).order_by(BlogPost.id.desc()).limit(2).all()

    # Prepare data for the two latest posts
    latest_post = None
    second_latest_post = None

    if len(latest_posts) > 0:
        latest_post = {
            "title": latest_posts[0].title,
            "genre": latest_posts[0].genre,
            "image": db.query(Photo.file_path).filter(Photo.id == latest_posts[0].cover_image).scalar() or "/static/default.jpg"
        }

    if len(latest_posts) > 1:
        second_latest_post = {
            "title": latest_posts[1].title,
            "genre": latest_posts[1].genre,
            "image": db.query(Photo.file_path).filter(Photo.id == latest_posts[1].cover_image).scalar() or "/static/default.jpg"
        }

    # Render the template with the data
    return templates.TemplateResponse("index.jinja2", {
        "request": request,
        "latest_post": latest_post,
        "second_latest_post": second_latest_post,
    })

@app.get("/blog", response_class=HTMLResponse)
async def read_root(request: Request):
    
    return templates.TemplateResponse(request=request, name="blog.jinja2")

@app.get("/galerie", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    all_photos = db.query(Photo).all()
    
    return templates.TemplateResponse("gallery.jinja2" , {
        "request": request,
        "photos": all_photos
        })

@app.get("/o-nas", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="about.jinja2")

@app.get("/admin", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="admin.jinja2")

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="post.jinja2")


# Route to get all posts
@app.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(BlogPost).all()
    return posts


 #TODO udelej aby to tam nemohly byt duplikatni nazvy
# Route to create a new post
@app.post("/posts")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(None), 
    class_ids: list[int] = None, 

    db: Session = Depends(get_db),
):
     # Handle file upload if provided
    upload_dir = "static/uploads" 
    cover_image_id = None
    if image:
        # Generate a unique filename
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Save the file
        with open(file_path, "wb") as f:
            f.write(image.file.read())

        # Store only the relative path (without 'static/')
        relative_path = os.path.relpath(file_path, "static")


        # Create a new Photo entry
        new_photo = Photo(file_path=relative_path)
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)

        # Get the ID of the new photo
        cover_image_id = new_photo.id


    new_post = BlogPost(
        title=title,
        slug=slugify(title),  # Generate a slug from the title
        content=content,
        author=author,
        genre=genre,
        date=date,
        cover_image = cover_image_id
    )   
    db.add(new_post)
    db.flush()

    # Handle attending classes if provided
    if class_ids:
        for class_id in class_ids:
            attending_class = AttendingClasses(
                post_id=new_post.id,
                class_id=class_id
            )
            db.add(attending_class)

    db.commit()
    db.refresh(new_post)

    if cover_image_id:
       new_photo.post_id = new_post.id
       db.commit()

    return {"message": "Post created successfully", "post": new_post}

@app.post("/add-photos")
def add_photos(
    images: list[UploadFile] = File(...),  # Accept multiple files
    taken_at: str = Form(...),

    db: Session = Depends(get_db),
):
    # Ensure the 'uploads' directory exists
    upload_dir = "static/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Process each uploaded file
    photo_entries = []
    for image in images:
        # Generate a unique filename
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        relative_path = os.path.relpath(file_path, "static")

        # Save the file
        with open(file_path, "wb") as f:
            f.write(image.file.read())

        # Create a new Photo entry
        new_photo = Photo(
            file_path=relative_path,
            taken_at=taken_at,  # Optional: Add a timestamp if needed
        )
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)

        # Append the new photo entry to the list
        photo_entries.append(new_photo)

    return {"message": "Photos added successfully", "photos": photo_entries}
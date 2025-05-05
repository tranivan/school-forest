from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, BlogPost

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


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.jinja2")

@app.get("/blog", response_class=HTMLResponse)
async def read_root(request: Request):
    
    return templates.TemplateResponse(request=request, name="blog.jinja2")

@app.get("/galerie", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="gallery.jinja2")

@app.get("/o-nas", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="about.jinja2")

@app.get("/post", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="post.jinja2")


# Route to get all posts
@app.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(BlogPost).all()
    return posts

# Route to create a new post
@app.post("/posts")
def create_post(title: str, db: Session = Depends(get_db)):
    new_post = BlogPost(title=title)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
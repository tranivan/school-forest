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
async def read_root(request: Request, db: Session = Depends(get_db)):
    latest_posts = db.query(BlogPost.title, BlogPost.genres).order_by(BlogPost.id.desc()).limit(2).all()

    latest_post = latest_posts[0] if len(latest_posts) > 0 else "No posts available"
    second_latest_post = latest_posts[1] if len(latest_posts) > 1 else "No second post available"

    return templates.TemplateResponse("index.jinja2", 
        {
            "request": request, 
            "latest_post_title": latest_post[0],
            "latest_post_genre": latest_post[1],
            "second_latest_post_title": second_latest_post[0],
            "second_latest_post_genre": second_latest_post[1],
        }
    )

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
def create_post(
    title: str,
    content: str,
    author: str,
    genres: str,
    db: Session = Depends(get_db),
):
    new_post = BlogPost(
        title=title,
        content=content,
        author=author,
        genres=genres,
    )   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
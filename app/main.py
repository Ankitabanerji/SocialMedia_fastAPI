from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# models.base.metadata.create_all(bind=engine) not needed, since we have added in alembic

app = FastAPI ()
origins = ["https://www.google.com/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.post_router)
app.include_router(user.user_router)
app.include_router(auth.auth_router)
app.include_router(vote.vote_router)

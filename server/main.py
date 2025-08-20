from fastapi import FastAPI
from server.database import engine, Base
import server.api.auth as auth_router
import server.api.comment as comment_router
import server.api.post as post_router
import server.api.subreddit as subreddit_router
import server.api.vote as vote_router
import server.api.user as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(comment_router.router, prefix="/api", tags=["comments"])
app.include_router(post_router.router, prefix="/api/posts", tags=["posts"])
app.include_router(subreddit_router.router, prefix="/api/subreddits", tags=["subreddits"])
app.include_router(vote_router.router, prefix="/api", tags=["votes"])
app.include_router(user_router.router, prefix="/api", tags=["users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}



# FastAPI Application Structure
#  Authentication - Who the user is
#     Request Parsing & Validation
#     Authroization
#     ---------------
#     response - Business Logic usecases/
#     ---------------
#     Convert to Response Model
#     Return the Response
#     - Error Handling
#     - Performance
#     - Logging - Observability
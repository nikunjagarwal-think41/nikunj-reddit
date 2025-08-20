from fastapi import FastAPI
import server.api.auth as auth_router
import server.api.comment as comment_router
import server.api.post as post_router

app = FastAPI()
app.include_router(
auth_router.router, prefix="/auth", tags=["auth"])

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
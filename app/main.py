import uvicorn
from fastapi import FastAPI

from app.api.routes.search import router as search_router

app = FastAPI(title="Search Engine API", version="0.1.0")
app.include_router(search_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Search API is running. Open /docs for API docs."}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

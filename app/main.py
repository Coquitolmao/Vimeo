from fastapi import FastAPI
from app.api.routes import videos
from app.core.logging import setup_logging
from app.core.config import settings

setup_logging()

app = FastAPI(
    title="Vimeo API Wrapper",
    description="A production-ready API to consume Vimeo services.",
    version="1.0.0", root_path="/vimeo-api"
)

app.include_router(videos.router, prefix="/v1/videos", tags=["Videos"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)



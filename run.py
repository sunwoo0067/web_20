from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 
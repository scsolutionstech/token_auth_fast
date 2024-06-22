from fastapi import FastAPI
from routes import auth_router, subscription_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(subscription_router, prefix="/subscription")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

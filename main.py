# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer
# from contextlib import asynccontextmanager

# from app.models.database import create_db_and_tables
# from app.api import users, moods, journals, food, insights
# from app.utils.config import settings

# security = HTTPBearer()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     print("✅ Database tables created")
#     yield
#     print("🛑 Application shutting down")

# app = FastAPI(
#     title="MoodBite API",
#     description="AI-powered food-mood correlation analysis",
#     version="1.0.0",
#     lifespan=lifespan
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(moods.router, prefix="/api/v1/moods", tags=["moods"])
# app.include_router(journals.router, prefix="/api/v1/journals", tags=["journals"])
# app.include_router(food.router, prefix="/api/v1/food", tags=["food"])
# app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to MoodBite API",
#         "version": "1.0.0",
#         "status": "healthy"
#     }

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)











from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

# Fix these imports to match your actual files
from database import create_db_and_tables  # ✅ Direct import
import users, moods, journals, food, insights  # ✅ Direct import
from config import settings  # ✅ Direct import

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("✅ Database tables created")
    yield
    print("🛑 Application shutting down")

app = FastAPI(
    title="MoodBite API",
    description="AI-powered food-mood correlation analysis",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update these routes to match your actual router objects
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(moods.router, prefix="/api/v1/moods", tags=["moods"])
app.include_router(journals.router, prefix="/api/v1/journals", tags=["journals"])
app.include_router(food.router, prefix="/api/v1/food", tags=["food"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to MoodBite API",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

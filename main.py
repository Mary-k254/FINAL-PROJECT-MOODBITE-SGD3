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





# from __future__ import annotations  # ← ADD THIS
# import sys
# import warnings
# sys.setrecursionlimit(5000)  # Increase recursion limit
# warnings.filterwarnings("ignore", category=UserWarning)  # Hide warnings





# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import HTTPBearer
# from contextlib import asynccontextmanager

# # Fix these imports to match your actual files
# from database import create_db_and_tables  # ✅ Direct import
# import users, moods, journals, food, insights  # ✅ Direct import
# from config import settings  # ✅ Direct import

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

# # Update these routes to match your actual router objects
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




# 3rd

from __future__ import annotations
import sys
import warnings
sys.setrecursionlimit(5000)
warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import flet as ft
from flet_fastapi import FletApp

# Your existing imports
from database import create_db_and_tables
import users, moods, journals, food, insights
from config import settings
from auth import AuthManager

security = HTTPBearer()

# Your Flet frontend
async def flet_main(page: ft.Page):
    page.title = "MoodBite"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    auth_manager = AuthManager(page)
    
    async def route_change(route):
        page.views.clear()
        
        if page.route == "/login":
            from auth import create_login_page
            login_view = create_login_page(page, auth_manager)
            page.views.append(login_view)
        
        elif page.route == "/register":
            from auth import create_register_page
            register_view = create_register_page(page, auth_manager)
            page.views.append(register_view)
        
        elif page.route == "/dashboard":
            from dashboard import create_dashboard_page
            dashboard_view = create_dashboard_page(page, auth_manager)
            page.views.append(dashboard_view)
        
        await page.update_async()
    
    page.on_route_change = route_change
    await page.go_async("/login")

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
    allow_headers=["*"],
)

# Include Flet app
app.mount("/app", FletApp(flet_main))

# Your existing API routes
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
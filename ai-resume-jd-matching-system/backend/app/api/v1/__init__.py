from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.auth import router as auth_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.jds import router as jds_router
from app.api.v1.matching import router as matching_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.export import router as export_router
from app.api.v1.shortlist import router as shortlist_router

api_router.include_router(auth_router,      prefix="/auth",      tags=["Authentication"])
api_router.include_router(resumes_router,   prefix="/resumes",   tags=["Resumes"])
api_router.include_router(jds_router,       prefix="/jds",       tags=["Job Descriptions"])
api_router.include_router(matching_router,  prefix="/match",     tags=["Matching"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(export_router,    prefix="/export",    tags=["Export"])
api_router.include_router(shortlist_router, prefix="/shortlist", tags=["Shortlist"])
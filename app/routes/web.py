"""Web routes for HTML templates"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Projects page"""
    return templates.TemplateResponse("projects.html", {"request": request})


@router.get("/projects/{project_id}/issues", response_class=HTMLResponse)
async def project_issues_page(request: Request, project_id: int):
    """Project issues page"""
    return templates.TemplateResponse("issues.html", {"request": request, "project_id": project_id})


@router.get("/issues/new", response_class=HTMLResponse)
async def create_issue_page(request: Request):
    """Create issue page"""
    return templates.TemplateResponse("create_issue.html", {"request": request})


@router.get("/issues/{issue_id}", response_class=HTMLResponse)
async def issue_detail_page(request: Request, issue_id: int):
    """Issue detail page"""
    return templates.TemplateResponse("issue_detail.html", {"request": request, "issue_id": issue_id})

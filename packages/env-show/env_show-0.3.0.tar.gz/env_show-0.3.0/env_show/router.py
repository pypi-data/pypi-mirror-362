# env_show/router.py

from fastapi import APIRouter
from dotenv import dotenv_values
from typing import Dict

env_router = APIRouter()

@env_router.get("/env", response_model=Dict[str, str])
def show_env_vars():
    """
    Read and return the calling project's .env file as JSON.
    """
    env = dotenv_values(".env")  # Always reads .env from the app's current working directory
    return env

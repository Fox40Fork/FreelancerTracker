#Login/Logout endpoints
#cookies :P

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.session import Session
from database import getDBConnection
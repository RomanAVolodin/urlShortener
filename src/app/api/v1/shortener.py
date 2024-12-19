from fastapi import APIRouter, Depends, Body, HTTPException, status
from starlette.responses import RedirectResponse

from app.services.shortener import get_shorten_service, ShortenerService

router = APIRouter()


@router.post('/')
def get_short_link(service: ShortenerService = Depends(get_shorten_service), url: str = Body(..., embed=True)):
    short_link = service.shorten_link(url)
    return {'short_link': short_link}


@router.get('/{short_link}')
def redirect(short_link: str, service: ShortenerService = Depends(get_shorten_service)):
    return RedirectResponse(url=service.get_original_link(short_link))

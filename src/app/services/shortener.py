from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import ShortenedUrl, get_db_session
from app.services.helpers import create_short_link


class ShortenerService:
    def __init__(self, session: Session):
        self.session = session

    def shorten_link(self, url: str) -> str:
        link = self.session.query(ShortenedUrl).filter_by(original_url=url).first()
        if link:
            return link.short_link
        timestamp = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        short_link = create_short_link(url, timestamp)
        obj = ShortenedUrl(original_url=url, short_link=short_link)
        self.session.add(obj)
        self.session.commit()
        return short_link

    def get_original_link(self, short_link: str) -> str:
        obj = self.session.query(ShortenedUrl).filter_by(short_link=short_link).order_by(ShortenedUrl.id.desc()).first()
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Ссылка не существует!')
        return obj.original_url


def get_shorten_service(session: Session = Depends(get_db_session)) -> ShortenerService:
    return ShortenerService(session=session)

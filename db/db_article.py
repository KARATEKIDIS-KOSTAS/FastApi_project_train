
from fastapi import HTTPException,status
from exceptions import StoryException
from exceptions import StoryException
from schemas import ArticleBase
from db.models import DBArticle
from sqlalchemy.orm.session import Session

def create_article(db:Session, request:ArticleBase):
    if request.content.startswith('Once upon a time'):
        raise StoryException('No worries please')
    new_article =DBArticle(   
        user_id=request.creator_id,
        title=request.title,
        content=request.content,
        published=request.published
        )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_article(db:Session,id: int):
    article=db.query(DBArticle).filter(DBArticle.id==id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Article with id {id} not found')
    return article



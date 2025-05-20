
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay, Current_user_ArticleDisplay, UserBase
from auth.oauth2 import get_current_user, oauth2_schema

router=APIRouter(
    prefix='/article',
    tags=['article']
    )

#create article
@router.post('/',response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session= Depends(get_db),current_user: UserBase=Depends(get_current_user)):
    return db_article.create_article(db,request)

# get specific article
@router.get('/{id}',response_model =Current_user_ArticleDisplay)
def get_article(id:int, db: Session=Depends(get_db),current_user: UserBase=Depends(get_current_user)):
    return {'data': db_article.get_article(db,id),
            'current_user': current_user
            }
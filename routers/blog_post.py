from fastapi import APIRouter,status,Response,Query,Path,Body
from enum import Enum
from typing import Optional,List,Dict
from pydantic import BaseModel

router=APIRouter(prefix='/blog',tags=['blog'])

class Image(BaseModel):
    url:str
    alias:str

class Blogmodel(BaseModel):
    title: str
    content: str
    nb_comments: str
    published: Optional[bool]
    tags: List[str]=[]
    metadata: Dict[str,str]={'key1': 'val1'}
    image: Optional[Image]=None

@router.post('/new/{id}')
def create_blog(blog:Blogmodel, id: int, version: int= 1):
    blog.title
    return {'id': id,'data': blog, 'version': version}

@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
                    blog: Blogmodel,
                    id: int,
                    comment_title: int = Query(None,
                                           title='Title of the comment',
                                           description='Some description for comment_title',
                                           alias='commentTitle',
                                           deprecated=True
                                           ),
                    content: str = Body(Ellipsis,min_length=10, max_length=50,regex=r'^[a-z\s]*$'),
                    v: Optional[List[str]]= Query(['1.0','1.1','1.2']),
                    comment_id: int = Path(gt=5,le=10)
                    ): return   {
                                'blog':blog,
                                'id':id,
                                'commnet_title': comment_title,
                                'content':content,
                                'version': v,
                                'comment_id': comment_id
                                }

def required_functionality():
    return {'message': 'Learning FastAPI is important.'}

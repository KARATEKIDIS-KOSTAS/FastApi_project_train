from routers.blog_post import required_functionality
from typing import Optional
from fastapi import APIRouter,status,Response,Depends
from enum import Enum


router=APIRouter(prefix='/blog',tags=['blog'])

@router.get(
    '/all',
    summary='retrieve all blogs',
    description='This API call simulates fetching all blogs',
    response_description='The list of available blogs'
    )
def get_all_blogs(page=1,page_size: Optional[int]=None,req_parameter: dict= Depends(required_functionality)):
    return {'message':f'All {page_size} blogs on page {page}','req':req_parameter}

@router.get('/{id}/comments/{comment_id}',tags=['comments'])
def get_comment(id: int, comment_id: int, valid: bool=True, username: Optional[str]=None):
    """
    Simulates retrieving a comment of a blog

    - **id** mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {'message': f'blog_id {id}, comment_id {comment_id},valid {valid},username {username}'}

class blogtype(str,Enum):
    short='short'
    story='story'
    howto='howto'

@router.get('/type/{type}')
def get_blog_type(type: blogtype,req_parameter: dict= Depends(required_functionality)):
    return {'message': f'Blog type {type}'}

@router.get('/{id}',status_code=status.HTTP_200_OK)
def get_blog(id : int, response : Response):
    if id>5:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'error': f'BLOG {id} NOT FOUND'}
    else:
        response.status_code=status.HTTP_200_OK
        return {'message':f'Blog with id {id}'}
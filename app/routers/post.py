from fastapi import Body, Depends, FastAPI, Response,status, HTTPException,APIRouter
from sqlalchemy import func

from app import oauth2
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from typing import Optional,List
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user :int = 
                 Depends(oauth2.get_current_user),limit:int=10,skip:int=0, search: Optional[str]=""):
    # cursor.execute("SELECT * FROM [dbo].[S_api_posts]")
    # posts=pd.read_sql("SELECT * FROM [dbo].[S_api_posts]", conn)
    # print(posts)
    # posts=[]                                                        # list that will store all the posts
    # for row in cursor:
    #     p = {"id":row[0], "title":row[1], "content":row[2], "published":row[3], "created_at":row[4]}
    #     posts.append(p)
    # return posts
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    # print(current_user)
    

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id,models.Post.title,models.Post.content,models.Post.published,models.Post.owner_id).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user :int = 
                 Depends(oauth2.get_current_user)):
    # new_post=cursor.execute("INSERT INTO  [dbo].[S_api_posts](title,content)VALUES(?,?)",(post.title,post.content))
    # new_post=cursor.fetchone()
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    # print(current_user.id)
    new_post=models.Post(owner_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id :int,response:Response,db: Session = Depends(get_db),current_user :int = 
                 Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM [dbo].[S_api_posts] where id = (?)",str((id)))
    # post=cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id,models.Post.title,models.Post.content,models.Post.published,models.Post.owner_id).filter(models.Post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id:{id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user :int = 
                 Depends(oauth2.get_current_user)):  
    # cursor.execute("DELETE FROM [dbo].[S_api_posts] where id = (?)",str((id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = f"post with id:{id} does not exist")
    
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED!!tch...tch...tch...u can't delete what's not yours!!")

    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),user_id :int = 
                 Depends(oauth2.get_current_user)):
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id:{id} does not exist")
    if post.owner_id !=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT AUTHORIZED!!tch...tch...tch...u can't update what's not yours!!")

    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index]=post_dict
    return post_query.first()

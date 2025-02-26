from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.base import get_db
from app.models.user import User
# from app.schemas.user import User

router = APIRouter()


@router.get("/users")
def get_user(db: Session = Depends(get_db)):
    db_user = db.query(User.email).all()
    print(db_user)
    # process the data
    email_list = [user.email for user in db_user]
    return email_list

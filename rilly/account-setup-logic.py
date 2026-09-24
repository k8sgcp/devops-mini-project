from sqlalchemy import Column, String, Integer, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)

    # Composite Unique Index on (email, mobile)
    __table_args__ = (
        UniqueConstraint('email', 'mobile', name='uq_email_mobile_combination'),
    )

def create_user_account(session, name: str, email: str, mobile: str):
    clean_email = email.strip().lower()
    clean_mobile = mobile.strip().replace(" ", "").replace("-", "")

    new_user = User(name=name, email=clean_email, mobile=clean_mobile)
    
    try:
        session.add(new_user)
        session.commit()
        return {"success": True, "user_id": new_user.id}
    except IntegrityError:
        session.rollback()
        return {
            "success": False,
            "error": "DUPLICATE_COMBINATION",
            "message": "This mobile and email combination is already registered."
        }

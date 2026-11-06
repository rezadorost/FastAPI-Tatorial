from .database import SessionLocal
from .models import Users

db = SessionLocal()

user = db.query(Users).filter(Users.email=="reza@gmail.com").first()

if not user:
    print("User not found.")
else:
    user.role = "admin"
    db.commit()
    print(f"{user.email} is now an admin.")
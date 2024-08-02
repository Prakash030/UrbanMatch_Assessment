from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from sqlalchemy import func


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user API endpoint and made the interests field as a comma-separated string as the SQL database does not support array data type but sending the response as a list/array
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    interests_str = ",".join(user.interests) # Convert list to comma-separated string
    
    db_user = models.User(
        name=user.name,
        age=user.age,
        gender=user.gender,
        email=user.email,
        city=user.city,
        interests=interests_str  # Store as a comma-separated string
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    interests_list = db_user.interests.split(",") if db_user.interests else []
    response_user = {
        "id": db_user.id,
        "name": db_user.name,
        "age": db_user.age,
        "gender": db_user.gender,
        "email": db_user.email,
        "city": db_user.city,
        "interests": interests_list  # Convert back to list for the response
    }
    return response_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    def convert_user(user):
        return {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "email": user.email,
            "city": user.city,
            "interests": user.interests.split(",") if user.interests else []
        }
    return [convert_user(user) for user in users]

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    interests_list = user.interests.split(",") if user.interests else []
    response_user = {
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "email": user.email,
        "city": user.city,
        "interests": interests_list
    }
    return response_user

# Update user API endpoint based on user_id
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.age = user.age
    db_user.gender = user.gender
    db_user.email = user.email
    db_user.city = user.city
    db_user.interests = ",".join(user.interests)
    db.commit()
    db.refresh(db_user)

    interests_list = db_user.interests.split(",") if db_user.interests else []
    response_user = {
        "id": db_user.id,
        "name": db_user.name,
        "age": db_user.age,
        "gender": db_user.gender,
        "email": db_user.email,
        "city": db_user.city,
        "interests": interests_list  # Convert back to list for the response
    }
    return response_user

# Delete user API endpoint based on user_id
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Matchmaking API made on the logic of matching users based on their age, interests, and opposite gender
@app.get("/users/{user_id}/matches", response_model=list[schemas.User])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_interests = set(interest.lower() for interest in user.interests.split(","))
    min_age = user.age - 5
    max_age = user.age + 5
    gender = "female" if user.gender.lower() == "male" else "male"

    potential_matches = db.query(models.User).filter(
        models.User.id != user_id,
        func.lower(models.User.gender) == func.lower(gender),
        models.User.age.between(min_age, max_age)

    ).all()

    matches = []
    for potential_match in potential_matches:
        match_interests = set(interest.lower() for interest in potential_match.interests.split(","))
        if user_interests.intersection(match_interests):
            matches.append({
                "id": potential_match.id,
                "name": potential_match.name,
                "age": potential_match.age,
                "gender": potential_match.gender,
                "email": potential_match.email,
                "city": potential_match.city,
                "interests": list(match_interests)
            })
    
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found")
    
    return matches

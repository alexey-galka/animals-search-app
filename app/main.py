from fastapi import FastAPI
from app.database import engine
from app.routers import auth, admin, users, shelters, search, settings, animals
import app.models.animals as animal
import app.models.users as user
import app.models.shelters as shelter

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(animals.router)
app.include_router(shelters.router)
app.include_router(search.router)
app.include_router(settings.router)
app.include_router(admin.router)


animal.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
shelter.Base.metadata.create_all(bind=engine)

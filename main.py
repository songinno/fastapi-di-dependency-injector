import sys

import uvicorn
from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from model import Base

from containers import ApplicationContainer, ApplicationSettings
from service import Service
from schema import UserRegisterInSchema

from dependency_injector.wiring import Provide, inject

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
@inject
def get_all_users(usecase: Service = Depends(Provide[ApplicationContainer.service])):
    return usecase.get_all()


@app.get("/users/{user_id}")
@inject
def get_user_by_id(user_id: str, usecase: Service = Depends(Provide[ApplicationContainer.service])):
    return usecase.get_by_id(id=user_id)


@app.post("/users")
@inject
def register(request: UserRegisterInSchema, usecase: Service = Depends(Provide[ApplicationContainer.service])):
    try:
        usecase.add_new_user(name=request.name, email=request.email)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "유저 생성이 실패했습니다"})


@app.delete("/users/{user_id}")
@inject
def delete_user(user_id: str, usecase: Service = Depends(Provide[ApplicationContainer.service])):
    try:
        usecase.delete_user(user_id=user_id)
    except:
        return JSONResponse(status_code=500, content={"message": "유저 삭제가 실패했습니다"})

if __name__ == '__main__':
    container = ApplicationContainer()
    json_config = ApplicationSettings().model_dump_json()
    container.config.from_json(json_config)

    container.wire([sys.modules[__name__]])
    Base.metadata.create_all(container.engine()) #3
    uvicorn.run(app=app)
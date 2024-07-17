from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from DataBase import delete_tables, create_tables
from Router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='127.0.0.1', port=8080)

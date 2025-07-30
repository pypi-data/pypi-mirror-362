# fastapi-stats-page

# usage
```
from fastapi import FastAPI
from fastapi_stats_page import StatsRouter, TrackVisitsMiddleware

app = FastAPI()

app.include_router(StatsRouter(title="Statistics of website").router)

app.add_middleware(TrackVisitsMiddleware)

@app.get("/")
async def homepage():
    return "hello world"
```
this will save visitors ip and user agens to a list

you can also save visitors to a file by doing this
```
from fastapi import FastAPI
from fastapi_stats_page import StatsRouter, TrackVisitsMiddleware

app = FastAPI()

app.include_router(StatsRouter(title="Statistics of website", get_from="users.txt").router)

app.add_middleware(TrackVisitsMiddleware, save_to="users.txt")

@app.get("/")
async def homepage():
    return "hello world"
```
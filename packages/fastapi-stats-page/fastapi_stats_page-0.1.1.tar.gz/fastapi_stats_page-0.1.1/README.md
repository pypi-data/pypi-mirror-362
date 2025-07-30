# fastapi-stats-page

# usage
```
from fastapi import FastAPI
from stats import StatsRouter, TrackVisitsMiddleware

app = FastAPI()

app.include_router(StatsRouter(title="Statistics of website").router)

app.add_middleware(TrackVisitsMiddleware)

@app.get("/")
async def homepage():
    return "hello world"
```
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers.pages import main as pages_router
from routers.root import main as root_router
from util.env import get_env

# from fastapi.staticfiles import StaticFiles

# get environment mode
env_mode = get_env("ENV_MODE", "development")

# logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if env_mode == "development":
    logger.setLevel(level=logging.DEBUG)

# production時，docsを表示しない
app_params = {}
if env_mode == "production":
    app_params["docs_url"] = None
    app_params["redoc_url"] = None
    app_params["openapi_url"] = None

# create app
app = FastAPI(**app_params)

origins = [
    "http://localhost:3000",
    "https://wdapi.scpwiki.jp"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# mount static folder
# app.mount("/static", StaticFiles(directory="/app/static"), name="static")

# check credentials
@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # Authorizationヘッダーを取得
    authorization = request.headers.get("Authorization")

    # Authorizationヘッダーがない場合はエラー
    # AuthorizationヘッダーがBearerで始まらない場合はエラー
    if authorization is None or not authorization.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Authorization header is required."})

    # Bearerトークンを取得
    token = authorization.split(" ")[1]

    # Bearerトークンが正しいか確認
    if token != get_env("API_CREDENTIAL"):
        return JSONResponse(status_code=401, content={"message": "Bearer token is invalid."})

    # 次のミドルウェアまたはエンドポイントの処理を呼び出し
    return await call_next(request)


# add routers
app.include_router(
    root_router.router
)
app.include_router(
    pages_router.router
)

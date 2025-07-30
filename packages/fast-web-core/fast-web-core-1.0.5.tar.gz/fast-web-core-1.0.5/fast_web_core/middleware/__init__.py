from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


def register_middleware(app: FastAPI, middlewares: List[Middleware] = []):
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_credentials=True,
    #     allow_origins=['*'],
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # 默认支持跨域
    middlewares.append(Middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=["*"], allow_headers=["*"]))

    if middlewares:
        for middleware in middlewares:
            # if app.middleware_stack is not None:  # pragma: no cover
            #     raise RuntimeError("Cannot add middleware after an application has started")
            app.user_middleware.insert(0, middleware)

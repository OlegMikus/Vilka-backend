from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root() -> Dict[str, Any]:
    return {'message': 'Hello World'}


@app.get('/hello/{name}')
async def say_hello(name: str) -> Dict[str, Any]:
    print('name')
    return {'message': f'Hello {name}'}

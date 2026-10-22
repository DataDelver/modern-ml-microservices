"""Mock MLflow model server used by the orchestrator benchmarks.

Mimics the two endpoints the orchestrator talks to:
  GET  /ping        -> 200
  POST /invocations -> {"predictions": [...]} with a simulated inference delay.

The delay is configurable via MODEL_DELAY_MS (default 50) so that the
concurrency characteristics of each orchestrator version are observable.
"""

import asyncio
import os

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()
DELAY_MS = float(os.getenv('MODEL_DELAY_MS', '50'))


@app.get('/ping')
async def ping() -> dict:
    return {'message': 'OK'}


@app.post('/invocations')
async def invocations(request: Request) -> dict:
    body = await request.json()
    n = len(body.get('dataframe_split', {}).get('index', []))
    await asyncio.sleep(DELAY_MS / 1000.0)
    return {'predictions': [123456.78 + i for i in range(n)]}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=int(os.getenv('PORT', '18099')), log_level='warning')

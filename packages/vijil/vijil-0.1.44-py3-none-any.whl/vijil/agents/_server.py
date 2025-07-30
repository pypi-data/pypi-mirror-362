from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from pyngrok import ngrok
from threading import Thread
from .models import ChatCompletionRequest
from typing import Callable, Optional
from .executor import LocalAgentExecutor
import secrets
from dataclasses import asdict
import uvicorn
import asyncio
from pyngrok.conf import PyngrokConfig


class LocalServer:
    def __init__(self, url: str, api_key: str, shutdown_fn: Callable):
        self.url = url
        self.api_key = api_key
        self.shutdown = shutdown_fn


def start_ngrok_server(
    evaluator: LocalAgentExecutor,
    token: Optional[str] = None,
    domain: Optional[str] = None,
    port: int = 12345,
) -> LocalServer:
    app = FastAPI()
    api_key = secrets.token_hex(16)

    # Instantiate ngrok based on whether or not the user was able to get a token and domain
    if token is not None and domain is not None:
        conf = PyngrokConfig(auth_token=token)
        tunnel = ngrok.connect(port, domain=domain, pyngrok_config=conf)
    else:
        tunnel = ngrok.connect(port)

    @app.post("/v1/chat/completions")
    async def complete(request: Request, authorization: str = Header(None)):
        if authorization != f"Bearer {api_key}":
            raise HTTPException(status_code=401, detail="Unauthorized")

        request_json = await request.json()
        chat_request = ChatCompletionRequest(**request_json)
        response = await evaluator.completions(chat_request)
        return JSONResponse(content=asdict(response))

    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="error")
    server = uvicorn.Server(config=config)

    def run_server():
        asyncio.run(server.serve())

    thread = Thread(target=run_server, daemon=True)
    thread.start()

    def shutdown():
        print("[INFO] Shutting down server and ngrok tunnel...")
        server.should_exit = True
        ngrok.disconnect(tunnel.public_url)
        ngrok.kill()

    return LocalServer(
        url=str(tunnel.public_url), api_key=api_key, shutdown_fn=shutdown
    )

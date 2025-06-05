
from fastapi import FastAPI, HTTPException,Request
from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from exceptions import StoryException
from routers import blog_get,user,product,article,blog_post,file,dependencies
from auth import authentication
from db import models
from templates import templates
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
import json
from client import html

app= FastAPI()#dependencies=[]# this for global dependencies for all app not just router
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(blog_get.router)
app.include_router(file.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)

@app.get('/hello')# method on index() function # after/ put the name/path the method will be called within the browser link search
def index(): # function
    return {'message':'HELLO WORLD!!!'}


@app.exception_handler(StoryException)
def story_exception_handler(request:Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


@app.get("/chat")
async def get():
    return HTMLResponse(html)

clients=[]
usernames = {}
chat_history = []

@app.websocket("/chat/message")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        # Wait for the client to send the join message with their username
        join_data = await websocket.receive_text()
        join_json = json.loads(join_data)
        if join_json.get("type") == "join" and "user" in join_json:
            usernames[websocket] = join_json["user"]

            # Send chat history to new user, prefixing messages with usernames
            for msg in chat_history:
                await websocket.send_text(msg)

        else:
            await websocket.close()
            return

        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)

            if data_json.get("type") == "chat":
                user = usernames.get(websocket, "Unknown")
                message = f"{user}: {data_json.get('message', '')}"

                if data_json.get("message") == "almight_delete" and user == "kokar":
                    chat_history.clear()
                    for client in clients:
                        await client.send_text("🧹 All messages were deleted.")
                    continue

                chat_history.append(message)

                # Broadcast to all clients except sender
                for client in clients:
                    if client != websocket:
                        await client.send_text(message)

            else:
                # Ignore unknown message types or handle as needed
                pass

    except WebSocketDisconnect:
        clients.remove(websocket)
        usernames.pop(websocket, None)

@app.exception_handler(HTTPException)
def custom_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(exc),status_code=400)

@app.middleware("http")# it will run when any endpoint is being executed calculating the time it needs for the endpoint function to be completed
async def add_middleware(request: Request, call_next):
    start_time=time.time()
    response= await call_next(request)
    duration= time.time()-start_time
    response.headers["duration"]=str(duration)
    return response

add_origins=['http://localhost:3000'] # allow call from local application to this local API

app.add_middleware(
    CORSMiddleware,
    allow_origins = add_origins,
    allow_credentials = True,
    allow_methods =['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/files',StaticFiles(directory="files"),name='files')
app.mount('/templates/static',StaticFiles(directory="templates/static"),name='static')

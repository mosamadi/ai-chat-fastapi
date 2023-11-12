from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from .exception_handlers import request_validation_exception_handler, unhandled_exception_handler
from .middleware import log_request_middleware
from .auth.router import router as auth_router
from .chat.router import router as chat_router

app = FastAPI()


app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router)
app.include_router(chat_router)
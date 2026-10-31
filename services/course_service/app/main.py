from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.api.routes import router
from app.core.exceptions import CourseNotFoundError

app = FastAPI(
    title="Course Service",
    version="0.1.0"
)

app.include_router(router)


@app.exception_handler(CourseNotFoundError)
async def check_exception(request: Request, error: CourseNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404,
                        content={"detail": "Course not found"})

from fastapi import APIRouter, Query, HTTPException, status
from model import Todo
todo_router = APIRouter()

todo_list = []

@todo_router.post("/todo/add")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Todo item added successfully."}



@todo_router.get("/todo/get")
async def get_single_todo(todo_id: int = Query(
    default=1, title = "The ID of the todo to get", ge=1
)) -> dict:
    for todo in todo_list:
        if todo.id == todo_id: return {"todo": todo}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo item not found."
    )

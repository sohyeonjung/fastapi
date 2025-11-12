from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI()

# CORS 설정 
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
      allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 저장소 (임시 딕셔너리)
# Key: todo_id (str), Value: todo_item_content (str)
todo_list = {}

# 4. Pydantic 모델 정의 (To Do Item 추가 시 데이터 유효성 검증용)
class TodoItem(BaseModel):
    id: str
    item: str

# ----------------------------------------------------
# [ To Do Item 조회 서비스 ]
# HTTP GET Request 사용 Path = /todo/get?id=todo_id
# ----------------------------------------------------
@app.get("/todo/get")
async def get_todo_item(
    # Query 클래스를 기반으로 Path 파라미터 검증 적용
    id: str = Query(..., description="조회할 To Do Item의 고유 ID", min_length=1)
):
    """
    특정 ID에 해당하는 To Do Item을 조회합니다.
    """
    if id not in todo_list:
        # Item이 없는 경우 404 Not Found 오류 메시지 출력
        raise HTTPException(
            status_code=404, 
            detail=f"Error: To Do Item with ID '{id}' not found."
        )
    
    return {
        "status": "success",
        "id": id,
        "item": todo_list[id]
    }

# ----------------------------------------------------
# [ To Do Item 추가 서비스 ]
# HTTP POST Request 사용 Path = /todo/add
# Message Body = { "id": todo_id, "item": "todo_item_content" }
# ----------------------------------------------------
@app.post("/todo/add")
async def add_todo_item(
    # Pydantic 기반으로 Message 데이터 검증 적용 (TodoItem 모델 사용)
    todo_data: TodoItem 
):
    """
    새로운 To Do Item을 List에 추가합니다.
    """
    # ID 중복 체크
    if todo_data.id in todo_list:
        raise HTTPException(
            status_code=400,
            detail=f"Error: To Do Item with ID '{todo_data.id}' already exists."
        )

    # List에 추가
    todo_list[todo_data.id] = todo_data.item
    
    return {
        "status": "success",
        "message": f"To Do Item '{todo_data.id}' added successfully.",
        "added_item": {"id": todo_data.id, "item": todo_data.item}
    }

# 기본 경로 (선택 사항)
@app.get("/")
async def root():
    return {"message": "FastAPI To Do List Service is running."}
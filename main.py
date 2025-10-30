from fastapi import FastAPI,Depends,HTTPException
from database import SessionLocal,Base,engine
from models import Todo
from schemas import Todo as TodoSchema ,TodoCreate

from sqlalchemy.orm import Session

# for creating the table 
Base.metadata.create_all(bind=engine)
 
app = FastAPI()

# Depeendency for DB session
def get_sb():
    db=SessionLocal()
    try:
        yield db # yield works as like return 
    finally:
        db.close() # after send data to route the we need to close this 
        
# post - create todo
@app.post('/todos',response_model=TodoSchema)
def create(todo: TodoCreate, db: Session = Depends(get_sb)):
    # Todo model il schema data ne kond vnn db il store chyunn
    db_todo= Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo) # to get the id from table once stored the data
    return db_todo # this response convert to json via schema
    

#get -all todos
@app.get('/todos',response_model=list[TodoSchema])
def read_todos( db: Session = Depends(get_sb)):
    return db.query(Todo).all()

# get single todo
@app.get('/todos/{todo_id}',response_model=TodoSchema)
def single_todo(todo_id:int,db: Session = Depends(get_sb)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo
    
#put = update todo
@app.put('/todos/{todo_id}',response_model=TodoSchema)
def update_todo(todo_id:int,updated: TodoCreate,db: Session = Depends(get_sb)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    #get updated data
    for key , value in updated.dict().items():
        setattr(todo,key,value)
    db.commit()
    db.refresh(todo)
    return todo

#delete
@app.delete('/todos/{todo_id}')
def delete_todo(todo_id:int,db: Session = Depends(get_sb)):
    todo= db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.delete(todo)
    db.commit()
    return {'message' : ' Todo deletd successfully'}

# for run
# uvicorn main:app --host 0.0.0.0 --port 8000
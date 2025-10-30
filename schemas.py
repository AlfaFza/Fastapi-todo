from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str | None =None
    completed: bool = False

class TodoCreate(TodoBase): 
    pass

class Todo(TodoBase): #dta creating time only 
    id:int
    class Config: 
        orm_mode =True # we getting from as pyhton object , Here we need to convert to json ,response data is coming from orm then it will automatically chnage to json 
        # its serializtion 
from fastapi import Depends,FastAPI,HTTPException,Query
import models
import schemas as sc
import services as se
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import database as dab
from typing import List
import json
from fastapi.responses import JSONResponse
from typing import Union

import logging

app = FastAPI()



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('apptraces.log')
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)


models.Base.metadata.create_all(bind=engine)

@app.post("/PhoneBook/add",response_model=sc.PhoneBook)
def create_phonebookuser(user:sc.PhoneBookCreate,db: Session = Depends(se.get_db)):
    if(len(user.name) == 0  or len(user.phone_number)==0): 
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
    db_usr = se.get_user_by_name(db=db,name=user.name)
    db_phone = se.get_user_by_phone(db=db,phone_number=user.phone_number)
    if db_usr:
        logger.debug("User already exists"+ user.name)
        return JSONResponse(status_code=404, content="User already exists")
    if db_phone:
        logger.debug("Phone number already exists "+ user.phone_number)
        return JSONResponse(status_code=404, content="Phone number already exists for a different user")
    return se.create_phonebook_user(db=db,user=user)



@app.get("/PhoneBook/list",response_model=List[sc.PhoneBook])
def get_users(db: Session = Depends(se.get_db)):
    users = se.get_all_users(db)
    logger.debug("List of all users returned")
    return users




@app.put("/PhoneBook/deleteByName/{name}")
def delete_user_by_name(name=str, db: Session = Depends(se.get_db)):
    if(len(name)==0):
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
 
    if(se.validate(name)):
        db_user_details = se.get_user_by_name(db=db, name=name)
        if not db_user_details:
            logger.exception("User not found")
            return JSONResponse(status_code=404, content="No record found to delete. Unable to delete")

        try:
            se.delete_user_by_name(db=db, name=name)
            logger.debug("User is deleted " +name)
        except Exception as e:
            logger.exception("Exception occured")
            return JSONResponse(status_code=400, content="Unable to delete the record")
    else:
        logger.exception("Error with the name .Try with the appropriate format")
        return JSONResponse(status_code=400,content="The name is not in the appropriate format. Try again")
   
    return JSONResponse(status_code=200, content="Success.The record is deleted")
    
@app.put("/PhoneBook/deleteByNumber/{phonenumber}")
def delete_user_by_phone(phonenumber=str,db: Session = Depends(se.get_db)):
    if(len(phonenumber)==0):
        return JSONResponse (status_code=400,content="The inputs are not in the appropriate format. Try again")
 
    if(se.validate_phone(phonenumber)):
        db_user_details = se.get_user_by_phone(db=db, phone_number=phonenumber)
        if not db_user_details:
            logger.exception("Phone number not found")
            return JSONResponse(status_code=404, content="No record found to delete")

        try:
            se.delete_user_by_phone(db=db, phone_number=phonenumber)
        except Exception as e:
            return JSONResponse(status_code=400, content="Unable to delete the record")
    else:
        logger.exception("Invalid Phone Number.Try with the appropriate format")
        return JSONResponse(status_code=400,content="The phone number is not in the appropriate format. Try again")

    return JSONResponse(status_code=200, content="Success.The record is deleted")








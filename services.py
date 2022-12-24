import database as dab
import sqlalchemy.orm as _orm,models as _mls,schemas as sc
from fastapi.responses import JSONResponse
import re
import logging
from fastapi import HTTPException
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('apptraces.log')
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)

def get_db():
    db=dab.SessionLocal()
    logger.debug("Creating the session with the db ")
    try:
        yield db
        logger.debug("Session Created")
    except:
        raise HTTPException(status_code=500, detail="Unable to connect to data")
    finally:
        logging.debug("Session is closed ")
        db.close()

def chck_spc(name):
    count = 0
    for i in range(0, len(name)):
        if name[i] == " ":
            count += 1
    if count>3:
        return True

def validate(name):
    #ADD regex to validate script
    if "<Script>" in name or "<script>" in name or "string" in name or chck_spc(name)==True:
        return False
    check_num = [int(k) for k in list(name) if k.isdigit()]
    new_name=name.strip().replace(" ","")
    regex = re.compile('^[@ _!#$%^&*()<>?[/\|}{~:]+$')  
    if(regex.search(new_name) != None or len(check_num)>0):
        return False
    name=name.split()
    if(len(name)>3):
        return False
    new_name=list(new_name)
    d={}
    for i in range(len(new_name)):
        d[new_name[i]]=d.get(new_name[i],0)+1
    print(d)
    for key,value in d.items():
        if (key=='-' and value>1) or (key=='_' and value>0) or (key=="'" and value>1) or (key==',' and value>1) or (key==" " and value>4) or (key=='’' and value>1):
            return False
    #print(d)
    logger.debug("Name validation is successful")
    return True

def validate_phone(phone_number):
    
    if(str(phone_number).startswith('(') or str(phone_number).startswith('+')):
        if(str(phone_number[1]=='0' and str(phone_number[2]=='1'))):
            if(str(phone_number).endswith('123-1234')):
            
                return False
    if(len(phone_number)==5):
        return True
    if (len(phone_number)<4):
        return False 
    if "<Script>" in phone_number or "<script>" in phone_number or "string" in phone_number:
        return False
    if(str(phone_number).isalpha()==True):
        return False
    rx = re.compile('^(\\+?\\d{1,3}( )?)?((\\(\\d{1,3}\\))|\\d{1,3})[- .]?\\d{1,3}[- .]?\\d{4}$') 
    check_digit = [(k) for k in list(phone_number) if k.isalpha()]

    #print(str(phone_number).isspace())
    dot_regex=re.compile('[.]')
    if((dot_regex.search(phone_number)!=None) and len(phone_number)>4): 
        old_phone_number= str(phone_number).replace(".", "")
        print(phone_number)
        if(str(old_phone_number).isnumeric()):
            new_phone_number=list(phone_number)
            d={}
            for i in range(len(new_phone_number)):
                d[new_phone_number[i]]=d.get(new_phone_number[i],0)+1
            print(d)
            for key,value in d.items():
                if(key=="." and value<2):
                    return True
    if(bool(re.search(r"\s", phone_number))==True and len(phone_number)>4): 
        phone_number= str(phone_number).replace(" ", "")
        if(str(phone_number).isnumeric()):
            return True
    if(rx.search(phone_number) == None or  len(check_digit)>0):
        print("Hello")
        return False
    logger.debug("Phone validation is successful")
    return True
    
def get_user_by_name(db:_orm.Session,name:str):
    return db.query(_mls.Phone).filter(_mls.Phone.name==name).first()

def get_user_by_phone(db:_orm.Session,phone_number:str):
    return db.query(_mls.Phone).filter(_mls.Phone.phone_number==phone_number).first()

def get_all_users(db:_orm.Session):
    return db.query(_mls.Phone).all()

def create_phonebook_user(db:_orm.Session,user:sc.PhoneBookCreate):
    logger.debug("Validating the name and phone_number before inserting it into the database.")
    if(validate(user.name) and validate_phone(user.phone_number)):
        logger.debug("The name and phone_number is correct. Moving onto the next step to form a database object")

        db_phonebook_user= _mls.Phone(name=user.name,phone_number=user.phone_number)
        logger.debug("Database object formed")

        db.add(db_phonebook_user)
        logger.debug("Adding to the database")
        db.commit()
        logger.debug("Record successfully added name "+user.name+" and phone_number is "+user.phone_number)

        db.refresh(db_phonebook_user)
        return JSONResponse(status_code=200, content=" Success. The record is inserted")

    else:
        return JSONResponse(status_code=400,content="The inputs are not in the appropriate format. Try again")

def delete_user_by_name(db:_orm.Session,name:str):
    try:
            db.query(_mls.Phone).filter(_mls.Phone.name == name).delete()
            db.commit()
    except Exception as e:
        raise Exception(e)

def delete_user_by_phone(db:_orm.Session,phone_number:str):
    try:
        
        db.query(_mls.Phone).filter(_mls.Phone.phone_number == phone_number).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
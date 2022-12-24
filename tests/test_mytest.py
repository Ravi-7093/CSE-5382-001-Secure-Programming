
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sys,os
from httpx import AsyncClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base
from main import app
from services import get_db

#_file_="main.py"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client =  TestClient(app)


#valid input for post request . This test case is for valid inputs
def test_add_phone_records():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Terry",
            "phone_number":"+1 (887)-299-8925"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#valid input for post request . This test case is for valid inputs for 1st record given in doc
def test_add_phone_records_one():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Schneier, Bruce",
            "phone_number":"123-1234"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg



#valid input for post request . This test case is for valid inputs for 2nd record given in doc
def test_add_phone_records_two():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Raj",
            "phone_number":"+32 (21) 212-2324"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#valid input for post request . This test case is for valid inputs for 3rd record given in doc
def test_add_phone_records_three():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "O’Malley, John F.",
            "phone_number":"011 701 111 1234"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg

#valid input for post request . This test case is for valid inputs for 4th record given in doc
def test_add_phone_records_four():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "John O’Malley-Smith",
            "phone_number":"12345.12345"
        }
    )
    msg=" Success. The record is inserted"
    assert response.status_code == 200
    assert response.json()==msg
#ivalid input for post request . This test case is for invalid name given for the one record in doc

def test_add_phone_records_invalid_name_one():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Ron O’’Henry",
            "phone_number":"+1 (682)-347-2028"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#ivalid input for post request . This test case is for invalid name given for the second record in doc

def test_add_phone_records_invalid_name_two():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Ron O’Henry-Smith-Barnes",
            "phone_number":"+1 (682)-347-2028"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#ivalid input for post request . This test case is for invalid name given for the third record in doc

def test_add_phone_records_invalid_name_three():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "L33t Hacker",
            "phone_number":"+1 (682)-347-2028"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg
#ivalid input for post request . This test case is for invalid name given for the four record in doc

def test_add_phone_records_invalid_name_four():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "<Script>alert(“XSS”)</Script>",
            "phone_number":"+1 (682)-347-2028"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#ivalid input for post request . This test case is for invalid name given for the five record in doc

def test_add_phone_records_invalid_name_five():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "select * from users;",
            "phone_number":"+1 (682)-347-2028"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the first record in doc

def test_add_phone_records_invalid_phone_one():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"123"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the second record in doc

def test_add_phone_records_invalid_phone_two():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"1/703/123/1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the third record in doc

def test_add_phone_records_invalid_phone_three():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"Nr 102-123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the four record in doc

def test_add_phone_records_invalid_phone_four():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"<script>alert(“XSS”)</script>"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the five record in doc

def test_add_phone_records_invalid_phone_five():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"+1234 (201) 123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg

#invalid input for post request . This test case is for invalid phone number  given for the six record in doc

def test_add_phone_records_invalid_phone_six():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Darshan",
            "phone_number":"(001) 123-1234"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"

    assert response.status_code == 400
    assert response.json()==msg


#invalid input for post request . This test case is for invalid inputs ie missing value for one of the fields
def test_add_phone_miss_records():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "",
            "phone_number":"+1 (887)-299-8425"
        }
    )
    msg="The inputs are not in the appropriate format. Try again"
    assert response.status_code == 400
    assert response.json()==msg


#valid input for post request. This test case is for valid inputs but the user or number already exits.
def test_add_phone_records_exist():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Terry",
            "phone_number":"+1 (887)-299-8425"
        }
    )
    msg="User already exists"
    assert response.status_code == 404
    assert response.json()==msg

#invalid input for post request .This test case is for invalid request but the user or number is not in appropriate format.
def test_add_phone_records_exist_invalid():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Terry",
            "phone_number":"123"
        }
    )
    msg="User already exists"
    assert response.status_code == 404
    assert response.json()==msg

#Test case to get the users list   
def test_get_user_list():
    response = client.get(
        "/PhoneBook/list"
    )
    assert response.status_code == 200

#Test case for deleting using the user by name
def test_delete_user_by_phone_name():
  
    response = client.put(
        "/PhoneBook/deleteByName/Terry"
    )
    msg="Success.The record is deleted"
    print(response)
    assert response.status_code == 200
    assert response.json()==msg

#Test case for deleting using the user by name without providing the name
def test_delete_user_by_phone_name_missing_record():
  
    response = client.put(
        "/PhoneBook/deleteByName/"
   
    )
    assert response.status_code == 404



#Test case for deleting using the user by phonenumber
def test_delete_user_by_phone_phonenumber():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Akash",
            "phone_number":"+1 (987)-219-8925"
        }
    )
    response = client.put(
        "/PhoneBook/deleteByNumber/+1 (987)-219-8925",
   
    )
    msg="Success.The record is deleted"
    print(response)
    assert response.status_code == 200
    assert response.json()==msg

#Test case for deleting using the user by phonenumber
def test_delete_user_by_phone_phonenumber_missing_num():
   
    response = client.put(
        "/PhoneBook/deleteByNumber/"
    )
    assert response.status_code == 404


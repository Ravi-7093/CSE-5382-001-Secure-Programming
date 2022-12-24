# CSE-5382-001-Secure-Programming

The  goal  of  this  assignment  is  to  produce  a  REST  API  that  validates  its  input  using  regular 
expressions. 
 
This will be an individual assignment (no teams). 
 
Detail: 
Produce a REST API application that maintains a phone book of names and phone numbers.  The 
program shall be capable of receiving and storing a list of people with their full name and telephone.  
The application shall include the following API endpoints: 
 
• GET /PhoneBook/list – Produce a list of the members of the database. 
• POST /PhoneBook/add – Add a new person to the database. 
o Argument is an object with name and phone number string elements. 
• PUT /PhoneBook/deleteByName – Remove someone from the database by name. 
o Argument is the name as a string. 
• PUT /PhoneBook/deleteByNumber – Remove someone by telephone #. 
o Argument is the phone number as a string. 
See the PhoneBook.json file attached to the assignment in Canvas for a full OpenAPI 3.0 spec to be 
used as requirements for the interface.  Return values should all be in JSON. 
Create  regular  expressions  for  <Person>  and  <Telephone  #>.    Use  these  regular  expressions  to 
verify that the user is supplying valid data.  More flexible specifications will be graded higher.  For 
example: 
• Allowing for international or US format telephone numbers 
• Allowing for <first middle last>, <first last> or <last, first MI>) 

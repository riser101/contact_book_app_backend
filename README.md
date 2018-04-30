
**Python v2.7** 
### The app is hosted at http://contactapp.pythonanywhere.com/, feel free to take it out on a ride on this base path.

Please use an API interaction tool like postman to communicate with the APIs. All endpoints are protected except the user registration and login endpoints.

# APIs

Note: All request parameters are sent as form data unless stated otherwise.

## /register
This route registers a new user for the contact application. Reminder, please post with **form data**.

**Method : Post**

Sample Request:

	username : sample_user
	password : sample_password	
							    
Sample Response:
	
	{
	    "msg": "user created successfully",
	    "status": "ok"
	}
			
## /login
This route logs-in a registered user

**Method : Post**

Sample Request:

	
	username : registered_user 
	password : registered_user_pass 
	 	          

Sample Response:

	{
	    "msg": "logged-in successfully",
	    "status": "ok"
	}
	
## /create
This route creates a new contact.

**Method : Post**

Sample Request:
	
	name : Chandler 
	contact_number : +919887889877 
	email : cbing@gmail.com
    
Sample Response:

    {
   	 	"msg": "contact created",
    	"status": "ok"
	}
## /edit
This route edits an existing contact 

**Method:PUT**

Sample Request:							    
	

	contact_id : 3242
	name : chandler
	email = engaged_chandlerb@gmail.com
	contact_number = +917887667655
	

Sample Response:
	
    {
   	 	"msg": "updated successfully",
    	"status": "ok"
	}

## /delete
This routes deletes an existing contact.

**Method:DELETE**

	contact_id = 23432
	
Sample Response:		
	
	{
	    "code": 200,
	    "message": "deleted successfully",
	    "status": "ok"
	}

## /search
This route supports three modes of searches, and takes **input parameters as part of url**. Following are the three modes:

1. Contact can be searched by only name
2. Contact can be searched by only email
3. Contact can be searched by both, name and email

**Method:GET**

Sample request urls for search:

1. http://contactapp.pythonanywhere.com/search?name=chandler
2. http://contactapp.pythonanywhere.com/search?email=bing@gmail.com
3. http://contactapp.pythonanywhere.com/search?name=chandler&email=bing@gmail.com

The endpoint is **paginated** and defaults to **10 contacts per request**.

Sample request url for paginated request:
	
	http://contactapp.pythonanywhere.com/search?email=bing@gmail.com&page=1&per_page=5

Sample Response:		
    
	{
	    "msg": "found",
	    "result": [
	        {
	            "id":234,
	            "contact_number": "1887667877",
	            "email": "bing@gmail.com",
	            "name": "chandler",
	        }
	    ],
	    "status": "ok"
	}
					    
## Test Coverage
<br>

![Alt text](test_coverage_snap.png?raw=true "Test Coverage Report")
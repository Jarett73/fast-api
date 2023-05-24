Create a virtual environment:   
```virtualenv venv -p C:\Python311\python.exe```

Install all the requirements
```pip install -r requirements.txt```

#### OR

Manually installing the requirements

Install fast API:  
```pip install fastapi```

Install webserver for Fast API:  
```pip install "uvicorn[standard]"```

db setup:  
```pip install sqlalchemy```

hash password  
```pip install passlib["bcrypt"]```

jwt setup  
```pip install "python-jose[cryptography]"```

```pip install python-multipart```

Run the Fast API application  
```uvicorn main:app --reload```

Access the Swagger document on: http://127.0.0.1:8000/docs

Authenticate using the following credentials:
#### username: ```test```
#### password: ```test1234```

![alt text](/images/fast_api_main.png)

![alt text](/images/fast_api_admin_user.png)

![alt text](/images/fast_api_schemas.png)

![alt text](/images/fast_api_auth.png)

![alt text](/images/fast_api_auth2.png)
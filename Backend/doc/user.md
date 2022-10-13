# User API


## api/v1/token/auth
- method: POST
- permission: customer, staff, admin
- description: get access token to auth
- required fields: username, password
- payload example:
    ```
    {
        "username": "admin",
        "password": "admin"
    }
    ```
- result:
    ```
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjIzNDQ5MiwiaWF0IjoxNjYzNjQyNDkyLCJqdGkiOiJmMzQ1NGYwZWRhYjE0Y2RlYTM1OGUyNTI0MmUwMzMyMyIsInVzZXJfaWQiOiIyMzJhODM5Yy04ZGNiLTRlYzgtOGJkMi05ZmFmOGUxODA1NWIifQ.O5m7x0A08_simLU8ZMv97ZUDhKPTJTPrGe4NnOlv5fg",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzNzI4ODkyLCJpYXQiOjE2NjM2NDI0OTIsImp0aSI6Ijg5NjI3ZmZiZjU0OTQ3MmY4NDU5Y2U0YThjMTYyNWEzIiwidXNlcl9pZCI6IjIzMmE4MzljLThkY2ItNGVjOC04YmQyLTlmYWY4ZTE4MDU1YiJ9.uuZ5hfnAIWasAQpbHZ2xFIUdwpXupukJlfRTDnHgBTw"
    }
    ```


## api/v1/token/refresh
- method: POST
- permission: customer, staff, admin
- description: renew access token from refresh token
- required fields: refresh
- payload example:
    ```
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjIzNDQ5MiwiaWF0IjoxNjYzNjQyNDkyLCJqdGkiOiJmMzQ1NGYwZWRhYjE0Y2RlYTM1OGUyNTI0MmUwMzMyMyIsInVzZXJfaWQiOiIyMzJhODM5Yy04ZGNiLTRlYzgtOGJkMi05ZmFmOGUxODA1NWIifQ.O5m7x0A08_simLU8ZMv97ZUDhKPTJTPrGe4NnOlv5fg"
    }
    ```
- result:
    ```
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjIzNDQ5MiwiaWF0IjoxNjYzNjQyNDkyLCJqdGkiOiJmMzQ1NGYwZWRhYjE0Y2RlYTM1OGUyNTI0MmUwMzMyMyIsInVzZXJfaWQiOiIyMzJhODM5Yy04ZGNiLTRlYzgtOGJkMi05ZmFmOGUxODA1NWIifQ.O5m7x0A08_simLU8ZMv97ZUDhKPTJTPrGe4NnOlv5fg",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzNzI4ODkyLCJpYXQiOjE2NjM2NDI0OTIsImp0aSI6Ijg5NjI3ZmZiZjU0OTQ3MmY4NDU5Y2U0YThjMTYyNWEzIiwidXNlcl9pZCI6IjIzMmE4MzljLThkY2ItNGVjOC04YmQyLTlmYWY4ZTE4MDU1YiJ9.uuZ5hfnAIWasAQpbHZ2xFIUdwpXupukJlfRTDnHgBTw"
    }
    ```


## api/v1/self/info
- method: GET
- description: get self information
- result:
    ```
    {
        "id": "f5c95765-87cd-482f-9e97-1d9d2d471e59",
        "username": "longvu",
        "email": "longvu@gmail.com",
        "address": null,
        "full_name": null,
        "role": "customer",
        "gender": "male",
        "phone_number": null,
        "is_active": true,
        "date_joined": "2022-10-10",
        "description": null,
        "price": null,
        "number_of_surveys": null,
        "number_of_surveys_question": null
    }
    ```

- method: PUT
- description: update self information
- mutable fields: full_name, address, phone_number, gender
- payload example:
    ```
    {
        "full_name": "Long Vu",
        "phone_number": "0999999999",
        "address": "Dong Da, Ha Noi"
    }
    ```
- result:
    ```
    {
        "id": "f5c95765-87cd-482f-9e97-1d9d2d471e59",
        "username": "longvu",
        "email": "longvu@gmail.com",
        "address": "Dong Da, Ha Noi",
        "full_name": "Long Vu",
        "role": "customer",
        "gender": "male",
        "phone_number": "0999999999",
        "is_active": true,
        "date_joined": "2022-10-10",
        "description": null,
        "price": null,
        "number_of_surveys": null,
        "number_of_surveys_question": null
    }
    ```


## api/v1/users
- method: GET
- permission: admin & staff
- description: get all user (admin get all staff/customer, staff get all customer)
- additional params: page & size, active (true/false)
- url example: .../api/v1/users?active=true
- result:
    ```
    {
        "users": [
            {
            "id": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
            "username": "manhkhuat",
            "email": "dungkk0105@gmail.com",
            "address": null,
            "full_name": null,
            "role": "staff",
            "gender": "male",
            "phone_number": null,
            "is_active": true,
            "date_joined": "2022-10-10"
            },
            {
            "id": "f5c95765-87cd-482f-9e97-1d9d2d471e59",
            "username": "longvu",
            "email": "longvu@gmail.com",
            "address": null,
            "full_name": null,
            "role": "customer",
            "gender": "male",
            "phone_number": null,
            "is_active": true,
            "date_joined": "2022-10-10"
            }
        ],
        "page": 1,
        "size": 2,
        "total": 2
    }
    ```

- method: POST
- permission: admin
- description: admin can create staff, customer -- staff can create customer
- option 1: admin create staff
    - required fields: username, password, confirm_password, email, role (admin/staff/customer), is_active
    - additional fields: full_name, address, gender (male/female), phone_number
- option 2: admin create customer
    - required fields: username, password, confirm_password, email, role (admin/staff/customer), is_active
    - additional fields: full_name, address, gender (male/female), phone_number, description, price, number_of_surveys, number_of_surveys_question
- payload example:
    ```
    {
        "email": "dungkk0105@gmail.com",
        "username": "manhkhuat",
        "password": "admin",
        "confirm_password": "admin",
        "gender": "male",
        "role": "staff",
        "is_active": true
    }
    ```
- result:
    ```
    {
        "id": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
        "username": "manhkhuat",
        "email": "dungkk0105@gmail.com",
        "address": null,
        "full_name": null,
        "role": "staff",
        "gender": "male",
        "phone_number": null,
        "is_active": true,
        "date_joined": "2022-10-10"
    } 
    ```


##  api/v1/users/{user_id}
- method: GET
- permission: admin & staff
- description: get user by user_id
- example url: ...api/v1/users/f5c95765-87cd-482f-9e97-1d9d2d471e59
- result:
    ```
    {
        "id": "f5c95765-87cd-482f-9e97-1d9d2d471e59",
        "username": "longvu",
        "email": "longvu@gmail.com",
        "address": "Dong Da, Ha Noi",
        "full_name": "Long Vu",
        "role": "customer",
        "gender": "male",
        "phone_number": "0999999999",
        "is_active": true,
        "date_joined": "2022-10-10",
        "description": null,
        "price": null,
        "number_of_surveys": null,
        "number_of_surveys_question": null
    }
    ```

- method: PUT
- permission: admin
- description: update user by user_id
- option 1: update staff
    - mutable fields: username, email, password, address, full_name, gender, phone_number, role, is_active
- option 2: update customer
    - mutable fields: username, email, password, address, full_name, gender, phone_number, role, is_active, description, price, number_of_surveys, number_of_surveys_question
- example url: .../api/v1/users/3bf6777b-a907-41e1-99e0-fdfd62245d91
- payload example:
    ```
    {
        "full_name": "Khuat Manh",
        "address": "Thach That, Ha Noi",
        "phone_number": "0987654321"
    }
    ```
- result:
    ```
    {
        "id": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
        "username": "manhkhuat",
        "email": "dungkk0105@gmail.com",
        "address": "Thach That, Ha Noi",
        "full_name": "Khuat Manh",
        "role": "staff",
        "gender": "male",
        "phone_number": "0987654321",
        "is_active": true,
        "date_joined": "2022-10-10"
    }
    ```

- method: DELETE
- permission: admin
- description: delete user by user_id
- example url: .../api/v1/users/08e277b2-b4d8-483b-ad10-5f0ccaaa88d9
- result:
    ```
    {
        "message": "User deleted successfully",
        "status_code": 204
    }
    ```


## api/v1/self/password
- method: PUT
- description: change self password
- required fields: current_password, new_password
- payload example:
    ```
    {
        "current_password": "admin",
        "new_password": "admin123"
    }
    ```
- result:
    ```
    {
        "message": "Password changed successfully",
        "status_code": 200
    }
    ```

## api/v1/otp/reset
- method: POST
- description: get otp to renew a password if you forgot
- required fields: email
- payload example:
    ```
    {
        "email": "nguyenvana@gmail.com"
    }
    ```
- result:
    ```
    {
        "message": "OTP has been sent",
        "status_code": 200
    }
    ```

## api/v1/password/reset
- method: PUT
- description: reset password
- required: email, otp, new_password
- payload example:
    ```
    {
        "email": "nguyenvana@gmail.com",
        "otp": "128126",
        "new_password": "admin"
    }
    ```
- result:
    ```
    {
        "message": "Password reset successfully",
        "status_code": 200
    }
    ```


## api/v1/staff/requests
- method: GET
- permission: staff & admin
- description: get all request of staff
- additional params: page & size, status (pending, approved, rejected)
- result:
    ```
    {
        "requests": [
            {
                "id": "64336862-06fc-4377-98d3-fdefb039e85d",
                "method": "post",
                "data": {
                    "confirm_password": "admin",
                    "username": "hoangha",
                    "email": "hoangha@gmail.com",
                    "address": null,
                    "full_name": null,
                    "role": "customer",
                    "gender": null,
                    "phone_number": null,
                    "is_active": true,
                    "description": null,
                    "price": null,
                    "number_of_surveys": null,
                    "number_of_surveys_question": null
                },
                "status": "pending",
                "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91"
            },
            {
                "id": "947598f1-c93f-42e7-a86b-c0e6281bde17",
                "method": "post",
                "data": {
                    "confirm_password": "admin",
                    "username": "anvu",
                    "email": "anvu@gmail.com",
                    "address": null,
                    "full_name": null,
                    "role": "customer",
                    "gender": null,
                    "phone_number": null,
                    "is_active": true,
                    "description": null,
                    "price": null,
                    "number_of_surveys": null,
                    "number_of_surveys_question": null
                },
                "status": "pending",
                "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91"
            }
        ],
        "page": 1,
        "size": 2,
        "total": 2
    }
    ```


## api/v1/staff/requests/{request_id}
- method: GET
- permission: admin & staff
- description: get request by request id
- result:
    ```
    {
        "id": "947598f1-c93f-42e7-a86b-c0e6281bde17",
        "method": "post",
        "data": {
            "confirm_password": "admin",
            "username": "anvu",
            "email": "anvu@gmail.com",
            "address": null,
            "full_name": null,
            "role": "customer",
            "gender": null,
            "phone_number": null,
            "is_active": true,
            "description": null,
            "price": null,
            "number_of_surveys": null,
            "number_of_surveys_question": null
        },
        "status": "pending",
        "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91"
    }
    ```

- method: PUT
- permission: admin
- description: approved or reject request of staff
- required fields: status
- payload example:
    ```
    {
        "status": "approved"
    }
    ```
- result:
    ```
    {
        "message": "Customer updated successfully",
        "status_code": 200
    }
    ```

- method: DELETE
- permission: admin
- description: delete request by request id
- result:
    ```
    {
        "message": "Request deleted successfully",
        "status_code": 204
    }
    ```


## api/v1/staff/requests/create
- method: POST
- permission: staff
- description: staff create a create customer request
- required fields: username, password, confirm_password, email, role, is_active
- additional fields: phone_number, gender, address, full_name
- payload example:
    ```
    {
        "username": "anvu",
        "email": "anvu@gmail.com",
        "role": "customer",
        "password": "admin",
        "confirm_password": "admin",
        "is_active": true
    }
    ```
- result:
    ```
    {
        "id": "947598f1-c93f-42e7-a86b-c0e6281bde17",
        "method": "post",
        "data": {
            "confirm_password": "admin",
            "username": "anvu",
            "email": "anvu@gmail.com",
            "address": null,
            "full_name": null,
            "role": "customer",
            "gender": null,
            "phone_number": null,
            "is_active": true,
            "description": null,
            "price": null,
            "number_of_surveys": null,
            "number_of_surveys_question": null
        },
        "status": "pending",
        "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
        "customer_id": null
    }
    ```


## api/v1/staff/requests/update/{customer_id}
- method: POST
- permission: staff
- description: create a request to update customer info
- mutable fields: username, email, password, full_name, address, gender, is_active, description, price, number_of_surveys, number_of_surveys_question
- payload example:
    ```
    {
        "address": "Ha Dong, Ha Noi",
        "is_active": true,
        "price": 200000
    }
    ```
- result:
    ```
    {
        "id": "44f9d1fe-921b-4b57-b388-6193e43fe831",
        "method": "put",
        "data": {
            "address": "Ha Dong, Ha Noi",
            "full_name": null,
            "gender": null,
            "phone_number": null,
            "is_active": true,
            "description": null,
            "price": 200000.0,
            "number_of_surveys": null,
            "number_of_surveys_question": null
        },
        "status": "pending",
        "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
        "customer_id": "f5c95765-87cd-482f-9e97-1d9d2d471e59"
    }
    ```


## api/v1/staff/requests/delete/{customer_id}
- method: DELETE
- permission: staff
- description: create a request to delete user
- result:
    ```
    {
        "id": "5afdb2e4-810b-434c-b734-4d3ce7844160",
        "method": "delete",
        "data": null,
        "status": "pending",
        "owner": "3bf6777b-a907-41e1-99e0-fdfd62245d91",
        "customer_id": "f5c95765-87cd-482f-9e97-1d9d2d471e59"
    }
    ```
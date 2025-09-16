================
CODE SNIPPETS
================
TITLE: Python requirements.txt example
DESCRIPTION: An example of a requirements.txt file, listing packages and their specific versions required for a Python project. This file is used by pip and other package managers to install dependencies.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: text
CODE:
```
fastapi[standard]==0.113.0
pydantic==2.8.0
```

--------------------------------

TITLE: Install FastAPI with Standard Extras using uv
DESCRIPTION: Installs the FastAPI package with 'standard' extras using the 'uv' package manager. 'uv' is a fast, modern alternative to pip for package installation.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: shell
CODE:
```
uv pip install "fastapi[standard]"
```

--------------------------------

TITLE: Install FastAPI with Standard Extras using pip
DESCRIPTION: Installs the FastAPI package along with its 'standard' extras using pip. This command is used after activating a virtual environment to manage project dependencies.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: shell
CODE:
```
pip install "fastapi[standard]"
```

--------------------------------

TITLE: Install Harry Package Version 1 (Python)
DESCRIPTION: This command installs version 1 of the 'harry' package using pip. It's an example demonstrating the need for version management in Python projects.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: bash
CODE:
```
pip install "harry==1"
```

--------------------------------

TITLE: Install Packages from requirements.txt using uv
DESCRIPTION: Installs packages from a requirements.txt file using the 'uv' package manager. This ensures all specified dependencies are installed efficiently.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: shell
CODE:
```
uv pip install -r requirements.txt
```

--------------------------------

TITLE: FastAPI - Basic Setup and Routing
DESCRIPTION: This snippet demonstrates the fundamental setup of a FastAPI application, including creating an instance of the FastAPI class and defining a basic path operation with a GET request. It serves as the starting point for building web APIs with FastAPI.

SOURCE: https://fastapi.tiangolo.com/az/advanced/security

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: Install Harry Package Version 3 (Python)
DESCRIPTION: This command installs version 3 of the 'harry' package using pip, demonstrating how different projects might require different versions of the same library, leading to conflicts in a global environment.

SOURCE: https://fastapi.tiangolo.com/de/virtual-environments

LANGUAGE: bash
CODE:
```
pip install "harry==3"
```

--------------------------------

TITLE: FastAPI - Basic Setup
DESCRIPTION: This snippet demonstrates the fundamental setup of a FastAPI application, including importing the FastAPI class and creating an instance. It's the starting point for any FastAPI project.

SOURCE: https://fastapi.tiangolo.com/az/how-to

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI - Basic Setup
DESCRIPTION: This snippet demonstrates the fundamental setup of a FastAPI application, including importing the FastAPI class and creating an instance. It's the starting point for any FastAPI project.

SOURCE: https://fastapi.tiangolo.com/az/management

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: Install Specific Package Version with Pip
DESCRIPTION: Demonstrates how to install a specific version of a Python package using pip. This command is crucial for managing dependencies in different projects that may require distinct versions of the same library. For example, 'harry==1' installs version 1 of the 'harry' package.

SOURCE: https://fastapi.tiangolo.com/fr/virtual-environments

LANGUAGE: shell
CODE:
```
pip install "harry==1"
```

LANGUAGE: shell
CODE:
```
pip install "harry==3"
```

--------------------------------

TITLE: Run Python Script with Incorrect Environment
DESCRIPTION: This example demonstrates running a Python script ('main.py') that attempts to import a package ('sirius') which is not installed in the currently active virtual environment, leading to an ImportError.

SOURCE: https://fastapi.tiangolo.com/pl/virtual-environments

LANGUAGE: bash
CODE:
```
cd ~/code/prisoner-of-azkaban
python main.py
```

--------------------------------

TITLE: FastAPI Tutorial - First Steps
DESCRIPTION: This section introduces the fundamental steps for getting started with FastAPI, including setting up a basic application and understanding the core concepts.

SOURCE: https://fastapi.tiangolo.com/az/help-fastapi

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI Setup and Imports (Python)
DESCRIPTION: Includes necessary imports and basic FastAPI app initialization for the authentication example.

SOURCE: https://fastapi.tiangolo.com/hu/tutorial/security/oauth2-jwt

LANGUAGE: python
CODE:
```
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# ... rest of the code

app = FastAPI()
```

--------------------------------

TITLE: Mock User Database and Setup
DESCRIPTION: Contains a mock database for users and initial setup for FastAPI, including defining constants and initializing the `FastAPI` application instance.

SOURCE: https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from passlib.context import CryptContext

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

app = FastAPI()

# Assuming get_user is defined elsewhere
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Other necessary imports and definitions would go here
```

--------------------------------

TITLE: Example User Endpoint
DESCRIPTION: A simple example GET endpoint demonstrating a path parameter.

SOURCE: https://fastapi.tiangolo.com/ko/how-to/custom-docs-ui-assets

LANGUAGE: APIDOC
CODE:
```
## Get User by Username

### Description
Retrieves user information based on the provided username.

### Method
GET

### Endpoint
/users/{username}

### Parameters
#### Path Parameters
- **username** (str) - Required - The username of the user to retrieve.

#### Query Parameters
None

#### Request Body
None

### Request Example
```python
# GET /users/john_doe
```

### Response
#### Success Response (200)
- **message** (str) - A greeting message including the username.

#### Response Example
```json
{
    "message": "Hello john_doe"
}
```

```

--------------------------------

TITLE: FastAPI Tutorial - First Steps
DESCRIPTION: This section introduces the fundamental steps to get started with FastAPI, including setting up a basic application and understanding the core concepts.

SOURCE: https://fastapi.tiangolo.com/az/resources

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

```

--------------------------------

TITLE: Example User Endpoint
DESCRIPTION: A simple example endpoint demonstrating a basic GET request with a path parameter, included to show a functional part of the API alongside the documentation setup.

SOURCE: https://fastapi.tiangolo.com/hu/how-to/custom-docs-ui-assets

LANGUAGE: APIDOC
CODE:
```
## Example User Endpoint

### Description
This is an example of a standard API endpoint within the FastAPI application. It demonstrates how to define a route that accepts a path parameter (`username`) and returns a personalized greeting.

### Method
GET

### Endpoint
/users/{username}

### Parameters
#### Path Parameters
- **username** (str) - Required - The username to greet.

#### Query Parameters
N/A

#### Request Body
N/A

### Request Example
```python
@app.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}
```

### Response
#### Success Response (200)
- **message** (str) - A greeting message including the provided username.
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Defines an API endpoint that handles GET requests to retrieve a list of items. It demonstrates a basic setup for a FastAPI application with an included router.

SOURCE: https://fastapi.tiangolo.com/es/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
An API endpoint that handles GET requests to retrieve a list of items. This example showcases a basic FastAPI application setup including an included router.

### Method
GET

### Endpoint
/items/

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
```json
{
  "example": "No request body needed for this GET request"
}
```

### Response
#### Success Response (200)
- **name** (str) - The name of the item.

#### Response Example
```json
[
  {
    "name": "Empanada"
  },
  {
    "name": "Arepa"
  }
]
```
```

--------------------------------

TITLE: FastAPI Tutorial - First Steps
DESCRIPTION: This section introduces the fundamental steps for getting started with FastAPI, including setting up a basic API structure and understanding initial concepts.

SOURCE: https://fastapi.tiangolo.com/az/deployment/versions

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI - First Steps Tutorial
DESCRIPTION: This snippet covers the initial steps for creating a FastAPI application, focusing on setting up the basic structure and handling path parameters.

SOURCE: https://fastapi.tiangolo.com/az/how-to/graphql

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

--------------------------------

TITLE: FastAPI Basic Setup
DESCRIPTION: Illustrates the fundamental setup for a FastAPI application, including importing the FastAPI class and creating an instance.

SOURCE: https://fastapi.tiangolo.com/about

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI - Basic Setup and Routing
DESCRIPTION: Demonstrates the fundamental structure of a FastAPI application, including creating an app instance, defining a root path operation, and handling GET requests.

SOURCE: https://fastapi.tiangolo.com/az/advanced/templates

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI Setup and Dependencies
DESCRIPTION: Initializes a FastAPI application instance and sets up OAuth2 authentication with a token URL. It also includes a dummy user database.

SOURCE: https://fastapi.tiangolo.com/zh/tutorial/security/simple-oauth2

LANGUAGE: python
CODE:
```
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

--------------------------------

TITLE: FastAPI Project Setup with Dependencies
DESCRIPTION: Initializes a FastAPI application instance and imports necessary libraries for security, data modeling, and datetime operations.

SOURCE: https://fastapi.tiangolo.com/em/tutorial/security/oauth2-jwt

LANGUAGE: python
CODE:
```
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()
```

--------------------------------

TITLE: FastAPI Tutorial - First Steps
DESCRIPTION: This section guides users through the initial steps of creating a FastAPI application, focusing on setting up a basic API endpoint.

SOURCE: https://fastapi.tiangolo.com/az/benchmarks

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

--------------------------------

TITLE: FastAPI Tutorial - First Steps
DESCRIPTION: This section introduces the basic steps to get started with FastAPI, demonstrating how to create a simple API endpoint and run it.

SOURCE: https://fastapi.tiangolo.com/az/newsletter

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

```

--------------------------------

TITLE: Example PATH for Windows
DESCRIPTION: Demonstrates a common PATH environment variable setup on Windows, including custom Python installations and system directories. This ensures the system can find Python executables.

SOURCE: https://fastapi.tiangolo.com/az/environment-variables

LANGUAGE: batch
CODE:
```
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Defines a path operation using an HTTP GET method to retrieve a list of items. Includes an example of a simple GET request.

SOURCE: https://fastapi.tiangolo.com/fr/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
This endpoint retrieves a list of items. It demonstrates a basic GET request within a FastAPI application.

### Method
GET

### Endpoint
/items/

### Parameters
#### Path Parameters
None

#### Query Parameters
None

#### Request Body
None

### Request Example
None

### Response
#### Success Response (200)
- **items** (list) - A list of dictionaries, where each dictionary represents an item.

#### Response Example
```json
[
    {
        "name": "Empanada"
    },
    {
        "name": "Arepa"
    }
]
```
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: An example of a GET path operation in FastAPI that returns a list of items.

SOURCE: https://fastapi.tiangolo.com/az/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
Returns a list of items.

### Method
GET

### Endpoint
/items/

### Parameters
#### Query Parameters
- `q` (Optional[str]) - Optional - Query parameter to filter items.

### Request Example
```json
{
  "query": "example_query"
}
```

### Response
#### Success Response (200)
- `List[Dict[str, str]]` - A list of dictionaries, where each dictionary represents an item with a 'name' key.

#### Response Example
```json
[
  {
    "name": "Empanada"
  },
  {
    "name": "Arepa"
  }
]
```
```

--------------------------------

TITLE: FastAPI JWT Authentication Setup and Token Endpoint
DESCRIPTION: Sets up a FastAPI application with user models, a fake database, password hashing, and an OAuth2 token endpoint for JWT authentication. It includes dependencies to get and validate users.

SOURCE: https://fastapi.tiangolo.com/bn/tutorial/security/simple-oauth2

LANGUAGE: python
CODE:
```
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing_extensions import Annotated

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

```

LANGUAGE: python
CODE:
```
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={\"WWW-Authenticate\": \"Bearer\"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)

```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Retrieves an item by its ID. The ID is validated to ensure it starts with 'isbn-' or 'imdb-'. If no ID is provided, a random item is returned.

SOURCE: https://fastapi.tiangolo.com/tr/tutorial/query-params-str-validations

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
Retrieves an item by its ID. The ID is validated to ensure it starts with 'isbn-' or 'imdb-'. If no ID is provided, a random item is returned.

### Method
GET

### Endpoint
/items/

### Parameters
#### Query Parameters
- **id** (str | None) - Optional - The unique identifier for the item. Must start with 'isbn-' or 'imdb-'.

### Request Example
GET /items/?id=isbn-9781529046137

### Response
#### Success Response (200)
- **id** (str) - The identifier of the item.
- **name** (str) - The name of the item.

#### Response Example
{
  "id": "isbn-9781529046137",
  "name": "The Hitchhiker's Guide to the Galaxy"
}
```

--------------------------------

TITLE: FastAPI Deployment - Uvicorn
DESCRIPTION: Guide on running FastAPI applications using Uvicorn, an ASGI server. This covers basic commands for starting your application.

SOURCE: https://fastapi.tiangolo.com/az/deployment

LANGUAGE: bash
CODE:
```
uvicorn main:app --reload

```

--------------------------------

TITLE: GET /items/
DESCRIPTION: An example GET endpoint that returns a list of items.

SOURCE: https://fastapi.tiangolo.com/pt/reference/fastapi

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
This endpoint retrieves a list of items.

### Method
GET

### Endpoint
/items/

### Parameters
#### Query Parameters
- **skip** (int) - Optional - Number of items to skip
- **limit** (int) - Optional - Maximum number of items to return

### Request Example
```json
{
  "message": "No request body for GET request"
}
```

### Response
#### Success Response (200)
- **name** (str) - The name of the item

#### Response Example
```json
[
  {
    "name": "Empanada"
  },
  {
    "name": "Arepa"
  }
]
```

### Other Parameters for Path Operations
FastAPI provides several parameters for path operation decorators to customize behavior and documentation:

- **path** (str): The URL path for the operation. Defaults to the decorated function's path.
- **response_model** (Any): Specifies the Pydantic model or type for the response. Used for documentation, serialization, filtering, and validation.
- **status_code** (Optional[int]): Sets the default HTTP status code for the response.
- **tags** (Optional[List[Union[str, Enum]]]): A list of tags for organizing path operations in the OpenAPI documentation.
- **dependencies** (Optional[Sequence[Depends]]): A list of dependencies to apply to the path operation.
- **summary** (Optional[str]): A short summary for the path operation, shown in the OpenAPI documentation.
- **description** (Optional[str]): A detailed description for the path operation, can include Markdown. Extracted from the docstring if not provided.
- **response_description** (str): The description for the default response. Defaults to 'Successful Response'.
- **responses** (Optional[Dict[Union[int, str], Dict[str, Any]]]): Additional responses to document, including their schemas and descriptions.
- **deprecated** (Optional[bool]): Marks the path operation as deprecated in the OpenAPI documentation.
- **operation_id** (Optional[str]): A custom identifier for the operation in the OpenAPI specification.
- **response_model_include** (Optional[IncEx]): Pydantic configuration to include specific fields in the response.
- **response_model_exclude** (Optional[IncEx]): Pydantic configuration to exclude specific fields from the response.
- **response_model_by_alias** (bool): Whether to use aliases when serializing the response model. Defaults to True.
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: This endpoint retrieves a list of items. It's a basic example demonstrating how to define a GET request in FastAPI.

SOURCE: https://fastapi.tiangolo.com/es/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
Retrieves a list of predefined items.

### Method
GET

### Endpoint
/items/

### Parameters

#### Query Parameters
- **skip** (int) - Optional - Number of items to skip.
- **limit** (int) - Optional - Maximum number of items to return.

#### Request Body
None

### Request Example
```
GET /items/?skip=0&limit=10 HTTP/1.1
Host: example.com
Accept: */*
```

### Response
#### Success Response (200)
- **name** (str) - The name of the item.

#### Response Example
```json
[
    {"name": "Empanada"},
    {"name": "Arepa"}
]
```
```

--------------------------------

TITLE: Main FastAPI Application Setup
DESCRIPTION: Demonstrates the main FastAPI application setup, including including routers and setting global dependencies.

SOURCE: https://fastapi.tiangolo.com/hu/tutorial/bigger-applications

LANGUAGE: APIDOC
CODE:
```
## Main FastAPI Application Setup

### Description
Demonstrates the main FastAPI application setup, including including routers and setting global dependencies.

### Method
N/A

### Endpoint
N/A

### Parameters
None

### Request Example
None

### Response
None

### Included Routers:
- `users.router`
- `items.router`
- `admin.router` (with prefix `/admin`, tags `["admin"]`, and dependencies)

### Global Dependencies:
- `get_query_token`

### Root Endpoint:
- `GET /`: Returns a welcome message.
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Retrieves an item by its ID. The ID is validated to ensure it starts with either 'isbn-' or 'imdb-'. If no ID is provided, a random item is returned.

SOURCE: https://fastapi.tiangolo.com/he/tutorial/query-params-str-validations

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
Retrieves an item by its ID. The ID is validated to ensure it starts with either 'isbn-' or 'imdb-'. If no ID is provided, a random item is returned.

### Method
GET

### Endpoint
/items/

#### Query Parameters
- **id** (str | None) - Optional - The ID of the item to retrieve. Must start with 'isbn-' or 'imdb-'.

### Response
#### Success Response (200)
- **id** (str) - The ID of the item.
- **name** (str) - The name of the item.

#### Response Example
```json
{
    "id": "isbn-9781529046137",
    "name": "The Hitchhiker's Guide to the Galaxy"
}
```
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Defines a path operation for an HTTP GET request to retrieve a list of items. It includes an example of a simple FastAPI application structure with an APIRouter.

SOURCE: https://fastapi.tiangolo.com/bn/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
This endpoint retrieves a list of items. It's an example of defining a GET path operation using FastAPI's APIRouter.

### Method
GET

### Endpoint
/items/

### Request Body
None

### Response
#### Success Response (200)
- **name** (str) - The name of the item.

#### Response Example
```json
[
  {
    "name": "Empanada"
  },
  {
    "name": "Arepa"
  }
]
```

### Example Usage
```python
from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

@router.get("/items/")
def read_items():
    return [{"name": "Empanada"}, {"name": "Arepa"}]

app.include_router(router)
```
```

--------------------------------

TITLE: FastAPI Main Application Setup (Python)
DESCRIPTION: Illustrates the main FastAPI application setup, including importing and including routers, setting global dependencies, and defining a root path operation.

SOURCE: https://fastapi.tiangolo.com/he/tutorial/bigger-applications

LANGUAGE: python
CODE:
```
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

--------------------------------

TITLE: GET /status/ - Get System Status
DESCRIPTION: Checks the status of the system.

SOURCE: https://fastapi.tiangolo.com/ko/advanced/security/oauth2-scopes

LANGUAGE: APIDOC
CODE:
```
## GET /status/

### Description
Provides a simple status check for the system. Requires authentication.

### Method
GET

### Endpoint
/status/

### Parameters
#### Authentication
Requires a valid Bearer token.

### Response
#### Success Response (200 OK)
- **status** (string) - Indicates the system status, typically "ok".

#### Response Example
```json
{
  "status": "ok"
}
```

#### Error Response (401 Unauthorized)
- **detail** (string) - "Could not validate credentials" if the token is invalid or missing.
```

--------------------------------

TITLE: GET /items/
DESCRIPTION: Defines a GET endpoint that returns a list of items. This example demonstrates a basic GET request with a predefined response.

SOURCE: https://fastapi.tiangolo.com/de/reference/fastapi

LANGUAGE: APIDOC
CODE:
```
## GET /items/

### Description
Returns a list of items. Example: `[{'name': 'Empanada'}, {'name': 'Arepa'}]`.

### Method
GET

### Endpoint
/items/

### Request Body
This endpoint does not accept a request body.

### Response
#### Success Response (200)
- **name** (str) - The name of the item.

#### Response Example
```json
[
  {
    "name": "Empanada"
  },
  {
    "name": "Arepa"
  }
]
```
```

--------------------------------

TITLE: Initialize FastAPI App
DESCRIPTION: Creates a basic FastAPI application instance.

SOURCE: https://fastapi.tiangolo.com/bn/reference/fastapi

LANGUAGE: python
CODE:
```
from fastapi import FastAPI

app = FastAPI()
```

--------------------------------

TITLE: GET /users/
DESCRIPTION: An example endpoint to read users, demonstrating the use of APIRouter with tags.

SOURCE: https://fastapi.tiangolo.com/pt/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /users/

### Description
This endpoint retrieves a list of users.

### Method
GET

### Endpoint
/users/

### Parameters
#### Query Parameters
* None

#### Request Body
* None

### Request Example
```json
{
  "example": "No request body needed for this GET request."
}
```

### Response
#### Success Response (200)
- **username** (str) - The username of the user.

#### Response Example
```json
{
  "example": "[\n  {\"username\": \"Rick\"}, \n  {\"username\": \"Morty\"}\n]"
}
```
```

--------------------------------

TITLE: FastAPI: Basic Setup and Path Parameters
DESCRIPTION: Demonstrates the basic setup of a FastAPI application and how to define path parameters for API endpoints. This is fundamental for creating dynamic API routes.

SOURCE: https://fastapi.tiangolo.com/az/reference/status

LANGUAGE: Python
CODE:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

--------------------------------

TITLE: GET /status/ - Get System Status
DESCRIPTION: Checks the status of the system.

SOURCE: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes

LANGUAGE: APIDOC
CODE:
```
## GET /status/

### Description
Provides a simple status check for the API. This endpoint requires a valid access token, but does not enforce specific scopes.

### Method
GET

### Endpoint
/status/

### Parameters
#### Request Header
- **Authorization** (str) - Required - Bearer token for authentication. Example: `Bearer YOUR_ACCESS_TOKEN`.

### Response
#### Success Response (200)
- **status** (str) - Indicates the system status, typically 'ok'.

#### Response Example
```json
{
  "status": "ok"
}
```

#### Error Response (401)
- **detail** (str) - 'Could not validate credentials' if the token is missing, invalid, or expired.
```

--------------------------------

TITLE: FastAPI GET Operation
DESCRIPTION: This section details the parameters and functionality of the `get` decorator for defining HTTP GET requests in FastAPI.

SOURCE: https://fastapi.tiangolo.com/es/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /path

### Description
Adds a path operation using an HTTP GET operation.

### Method
GET

### Endpoint
/path

### Parameters
#### Path Parameters
- **path** (str) - Required - The path for the GET request.

#### Query Parameters
- **response_model** (any) - Optional - The response model to use for serialization.
- **status_code** (int) - Optional - The status code to return for the response.
- **tags** (list[str]) - Optional - A list of tags to group operations.
- **dependencies** (list[Depends]) - Optional - A list of dependencies to execute before the endpoint.
- **summary** (str) - Optional - A short summary for the operation.
- **description** (str) - Optional - A detailed description for the operation.
- **response_description** (str) - Optional - Description for the response. Defaults to 'Successful Response'.
- **responses** (dict) - Optional - Dictionary of responses for different status codes.
- **deprecated** (bool) - Optional - Whether the operation is deprecated.
- **operation_id** (str) - Optional - Unique identifier for the operation.
- **response_model_include** (set | list | None) - Optional - Fields to include in the response model.
- **response_model_exclude** (set | list | None) - Optional - Fields to exclude from the response model.
- **response_model_by_alias** (bool) - Optional - Whether to use alias for response model fields. Defaults to True.
- **response_model_exclude_unset** (bool) - Optional - Whether to exclude fields that were not set. Defaults to False.
- **response_model_exclude_defaults** (bool) - Optional - Whether to exclude fields with default values. Defaults to False.
- **response_model_exclude_none** (bool) - Optional - Whether to exclude fields with None values. Defaults to False.
- **include_in_schema** (bool) - Optional - Whether to include the operation in the OpenAPI schema. Defaults to True.
- **response_class** (any) - Optional - The response class to use. Defaults to JSONResponse.
- **name** (str) - Optional - The name of the operation.
- **callbacks** (list[APIWebSocketRoute | WebSocketRoute]) - Optional - A list of callbacks for the operation.
- **openapi_extra** (dict) - Optional - Extra data to include in the OpenAPI schema.
- **generate_unique_id_function** (Callable) - Optional - Function to generate unique IDs for operations. Defaults to generate_unique_id.

### Request Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Response
#### Success Response (200)
- **item_id** (int) - The ID of the item.
- **q** (str | None) - An optional query parameter.

#### Response Example
```json
{
  "item_id": 1,
  "q": "somequery"
}
```
```

--------------------------------

TITLE: GET /path
DESCRIPTION: Defines a GET path operation with various configuration options.

SOURCE: https://fastapi.tiangolo.com/az/reference/apirouter

LANGUAGE: APIDOC
CODE:
```
## GET /path

### Description
Defines a GET path operation with various configuration options.

### Method
GET

### Endpoint
/path

### Parameters
#### Path Parameters
- **path** (str) - Required - The URL path to be used for this *path operation*.

#### Query Parameters
- **response_model** (Any) - Optional - The type to use for the response. Used for documentation, serialization, filtering, and validation.
- **status_code** (Optional[int]) - Optional - The default status code to be used for the response.
- **tags** (Optional[List[Union[str, Enum]]]) - Optional - A list of tags to be applied to the *path operation*.
- **dependencies** (Optional[Sequence[params.Depends]]) - Optional - A list of dependencies to be applied to the *path operation*.
- **summary** (Optional[str]) - Optional - A summary for the *path operation*.
- **description** (Optional[str]) - Optional - A description for the *path operation*. Can contain Markdown.
- **response_description** (str) - Required - The description for the default response.
- **responses** (Optional[Dict[Union[int, str], Dict[str, Any]]]) - Optional - Additional responses that could be returned by this *path operation*.

### Request Example
```json
{
  "example": "request body"
}
```

### Response
#### Success Response (200)
- **example** (str) - Description of the example field.
```

--------------------------------

TITLE: FastAPI Initialization and Dependencies
DESCRIPTION: Sets up the FastAPI application instance and defines global constants and data models used throughout the authentication system. Includes imports for necessary libraries.

SOURCE: https://fastapi.tiangolo.com/em/tutorial/security/oauth2-jwt

LANGUAGE: python
CODE:
```
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
```

--------------------------------

TITLE: FastAPI CLI Development Mode Example
DESCRIPTION: Demonstrates how to install and run FastAPI in development mode using the new `fastapi dev` command. It shows the typical output, including server addresses and API documentation links. This feature simplifies the development workflow.

SOURCE: https://fastapi.tiangolo.com/it/release-notes

LANGUAGE: bash
CODE:
```
$ pip install --upgrade fastapi

$ fastapi dev main.py


 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


```

--------------------------------

TITLE: Define FastAPI GET Path Operation
DESCRIPTION: Demonstrates how to define a GET path operation using the APIRouter's `get` decorator. It includes parameters for response models, status codes, tags, and custom OpenAPI generation functions. The example shows a simple route that returns a list of items.

SOURCE: https://fastapi.tiangolo.com/de/reference/apirouter

LANGUAGE: python
CODE:
```
from fastapi import APIRouter, FastAPI
from typing import Type, Optional, List, Dict, Any, Callable
from fastapi.responses import Response, JSONResponse
from fastapi.routing import APIRoute, BaseRoute
from fastapi.utils import Default

# Assume generate_unique_id is defined elsewhere or imported
def generate_unique_id(route: APIRoute) -> str:
    # Dummy implementation for demonstration
    return route.name

# Assume Doc is a type annotation helper, possibly from pydantic
class Doc:
    def __init__(self, description: str):
        self.description = description

class APIRouter:
    def api_route(
        self,
        path: str,
        *,  # Force keyword arguments so they are explicit
        response_model=Default(None),
        status_code=None,
        tags=None,
        dependencies=None,
        summary=None,
        description=None,
        response_description="Successful Response",
        responses=None,
        deprecated=None,
        methods=["GET"],
        operation_id=None,
        response_model_include=None,
        response_model_exclude=None,
        response_model_by_alias=True,
        response_model_exclude_unset=False,
        response_model_exclude_defaults=False,
        response_model_exclude_none=False,
        include_in_schema=True,
        response_class=Default(JSONResponse),
        name=None,
        callbacks=None,
        openapi_extra=None,
        generate_unique_id_function=Default(generate_unique_id),
    ) -> Callable:
        # In a real scenario, this method would register the route with the router.
        # For documentation purposes, we just return a callable that accepts the decorated function.
        def decorator(func: Callable) -> Callable:
            # Here you would typically store route information associated with 'func'
            # For example: self.routes.append({'path': path, 'methods': methods, ...})
            return func
        return decorator

    def get(
        self,
        path: str,
        *,  # Force keyword arguments so they are explicit
        response_model=Default(None),
        status_code=None,
        tags=None,
        dependencies=None,
        summary=None,
        description=None,
        response_description="Successful Response",
        responses=None,
        deprecated=None,
        operation_id=None,
        response_model_include=None,
        response_model_exclude=None,
        response_model_by_alias=True,
        response_model_exclude_unset=False,
        response_model_exclude_defaults=False,
        response_model_exclude_none=False,
        include_in_schema=True,
        response_class=Default(JSONResponse),
        name=None,
        callbacks=None,
        openapi_extra=None,
        generate_unique_id_function=Default(generate_unique_id),
    ) -> Callable:
        """
        Add a *path operation* using an HTTP GET operation.

        ## Example

        ```python
        from fastapi import APIRouter, FastAPI

        app = FastAPI()
        router = APIRouter()

        @router.get("/items/")
        def read_items():
            return [{"name": "Empanada"}, {"name": "Arepa"}]

        app.include_router(router)
        ```
        """
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=["GET"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

    def put(
        self,
        path: str,
        *,  # Force keyword arguments so they are explicit
        response_model=Default(None),
        status_code=None,
        tags=None,
        dependencies=None,
        summary=None,
        description=None,
        response_description="Successful Response",
        responses=None,
        deprecated=None,
        operation_id=None,
        response_model_include=None,
        response_model_exclude=None,
        response_model_by_alias=True,
        response_model_exclude_unset=False,
        response_model_exclude_defaults=False,
        response_model_exclude_none=False,
        include_in_schema=True,
        response_class=Default(JSONResponse),
        name=None,
        callbacks=None,
        openapi_extra=None,
        generate_unique_id_function=Default(generate_unique_id),
    ) -> Callable:
        """
        Add a _path operation_ using an HTTP PUT operation.
        """
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags,
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses,
            deprecated=deprecated,
            methods=["PUT"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
            callbacks=callbacks,
            openapi_extra=openapi_extra,
            generate_unique_id_function=generate_unique_id_function,
        )

```
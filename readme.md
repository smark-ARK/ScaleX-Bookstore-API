# ScaleX Bookstore API

## Description

ScaleX Bookstore API is a RESTful API built using FastAPI that provides endpoints to manage a collection of books. The API allows users to view all available books, add new books, and delete existing books. Books are stored in CSV files (`regularUser.csv` and `adminUser.csv`) located in the `db` folder.

## Setup Instructions

### .env
Please make sure you add .env file in the root directory
```
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
REFRESH_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88esmark
ALGORITHM=HS256
ACCESS_EXPIRE_MINUTES=30
REFRESH_EXPIRE_MINUTES=1440
```
### 1. Set Up Python Virtual Environment

Before running the application, it's recommended to set up a Python virtual environment to isolate dependencies. You can do this by running the following commands in your terminal:

```bash
# On Unix/Linux
python3 -m venv venv

# On Windows
python -m venv venv
```

This will create a virtual environment named `venv` in your project directory.

### 2. Activate the Virtual Environment

Activate the virtual environment by running the appropriate command based on your operating system:

```bash
# On Unix/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

To run the FastAPI application, use Uvicorn with the following command:

```bash
uvicorn app.main:app --reload
```

This command will start the server, and the `--reload` flag will enable auto-reloading so that the server restarts automatically when changes are detected in the code.


### Using Docker

Alternatively, you can run the application using Docker. Docker setup is already included in the project. Follow the steps below:

1. Make sure Docker is installed on your system.

2. Build the Docker image and start the container using the following command:

```bash
docker-compose up --build
```
## Endpoints

### /home (GET)

- **Description:** Returns a list of all available books.
- **Authentication:** Not required.
- **Response:** A JSON array containing book objects.
- **Example:** `GET /home`

### /addbook (POST)

- **Description:** Adds a new book to the collection.
- **Authentication:** Requires admin privileges.
- **Parameters:** 
  - `name` (string): The name of the book.
  - `author` (string): The author of the book.
  - `publication_year` (integer): The publication year of the book.
- **Response:** A success message.
- **Example:** 
  ```bash
  POST /addbook
  {
      "name": "New Book",
      "author": "New Author",
      "publication_year": 2022
  }
  ```

### /deletebook (DELETE)

- **Description:** Deletes a book from the collection.
- **Authentication:** Requires admin privileges.
- **Parameters:** 
  - `name` (string): The name of the book to delete.
- **Response:** A success message.
- **Example:** `DELETE /deletebook?name=New Book`

## Users

The application has the following hardcoded users:

- **User:** 
  - Username: sampleuser
  - Password: samplepass
  - Type: user

- **Admin:** 
  - Username: sampleadmin
  - Password: samplepass
  - Type: admin

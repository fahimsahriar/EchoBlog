# Django Project

This Django-based project is a CRUD web application designed for Blogging.

## Prerequisites

To run this project, you need the following installed on your machine:

- Python 3.x (latest version recommended)
- pip (Python package installer)
- Git (to clone the repository)

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/fahimsahriar/EchoBlog.git

```
### 2. Navigate into the project directory:

``` bash
cd EchoBlog
```

### 3. Set up a virtual environment (optional but recommended):

Create a virtual environment to isolate project dependencies:

``` bash
python -m venv env
```

### 4. Activate the virtual environment:

- on On Windows:
    ``` bash
    .\env\Scripts\activate
    ```
- on On MacOS/Linus:
    ``` bash
    source env/bin/activate
    ```

### 5. Install dependencies:
Install all the required Python packages using pip:
``` bash
pip install -r requirements.txt
```

## Database Setup

This project uses SQLite3 as the default database. To set up the database, follow these steps:

### 1. Apply migrations:
Run the following command to create the SQLite database and apply migrations:
``` bash 
python manage.py migrate

```
### 2. Apply Fixtures:
Run the following comman add some sample data

``` bash 
python manage.py loaddata MasterCountries
python manage.py loaddata MasterDepartments
```

## Running the Server

Once the dependencies are installed and the database is set up, you can start the development server:

``` bash
python manage.py runserver

```

## Troubleshooting

- **Missing Dependencies**: If you encounter missing dependencies, ensure you have run:

    ```bash
    pip install -r requirements.txt
    ```

- **Database Issues**: If you face database errors, ensure that SQLite3 is installed (it's included by default in Python) and that migrations have been applied correctly:

    ```bash
    python manage.py migrate
    ```

- **Environment Variables**: Ensure any required environment variables (e.g., secret keys, API credentials) are set in a `.env` file or your system's environment variables.

    Example `.env` file:

    ```plaintext
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3
    ```


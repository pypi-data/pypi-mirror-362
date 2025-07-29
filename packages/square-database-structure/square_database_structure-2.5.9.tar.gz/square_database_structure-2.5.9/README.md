# square_database_structure (WIP)

## about

square_database_structure is a Python module that provides a structured and modular way to define database schemas and
tables using SQLAlchemy. It is designed to work with **PostgreSQL** databases, which natively support a
database-schema-table hierarchy. This structure allows for clear separation between schemas within a single database,
making it easier to manage large and complex database systems.

This module abstracts the database structure from the rest of the application logic, making schema definitions reusable
and easy to maintain across multiple projects.

### goals

- Centralize Database Schema Definitions: Serve as a single source of truth for defining database structures across
  multiple projects.
- Modular Design: Allow databases and schemas to be independently defined and easily extended.
- PostgreSQL Compatibility: Utilize PostgreSQL's native support for database-schema-table hierarchy, allowing for
  separation of concerns and scalability.
- Replaceability: The module should be easy to substitute with another implementation if necessary, while still
  following the same mechanisms for schema and data definition.
- Explicit Structure: Ensure a clear, standardized structure that is easy to follow, making the design more explicit for
  users.

## installation

```shell
pip install square_database_structure
```

## usage

This module organizes database schemas in a standardized folder structure where each top-level folder represents a
database, and subfolders within it represent schemas. All mandatory components, such as `__init__.py` and tables.py,
data.py, stored_procedures_and_functions need to follow this structure.

### Folder Structure

Here’s how you should organize your project when using this module:

```
square_database_structure/
├───main.py                                       # Global definition file (mandatory)
├───create_database.py                            # Global database creation file (mandatory)
└───database1/                                    # Each folder corresponds to a separate database
    ├───__init__.py                               # Contains the global name for the database (mandatory)
    └───schema1/                                  # Each subfolder corresponds to a schema within the database
        ├───__init__.py                           # Contains the global name for the schema (mandatory)
        ├───data.py                               # Contains the data for insertion for the schema (mandatory)
        ├───enums.py                              # Defines Enums to be used in the schema (optional)
        ├───tables.py                             # Defines tables of the schema (mandatory)
        └───stored_procedures_and_functions/      # Contains stored procedures and functions for the schema (mandatory)
            ├───__init__.py                       # Contains logic to discover sql files (mandatory)
            └───function.sql                      # function or stored procedure sql file (optional)
```

- Top-level folders: Represent individual databases (e.g., database1).
- Subfolders: Represent schemas within each database (e.g., public, schema1).
- Mandatory files:
    - `__init__.py` (both at the database and schema level).
    - tables.py within each schema.
    - data.py within each schema.
    - stored_procedures_and_functions package within each schema.

### Defining Database and Schema Names in `__init__.py`

Each database and schema folder must contain an `__init__.py` file where the database and schema names are defined
as
global variables.

#### Example for Database:

```python
# database1/__init__.py

global_string_database_name = "database1"  # Mandatory: Database name
```

#### Example for Schema:

```python
# database1/schema1/__init__.py

global_string_schema_name = "schema1"  # Mandatory: Schema name
```

### Defining Tables in tables.py

Each schema folder must contain a tables.py file where:

- You must declare a Base object tied to the schema.
- You can define table classes, extending the Base object.

#### Example tables.py:

```python
# database1/schema1/tables.py

from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from database1.schema1 import global_string_schema_name

# 1. Mandatory: Declare Base with MetaData pointing to the schema

Base = declarative_base(metadata=MetaData(schema=global_string_schema_name))


# 2. Optional: Define table classes by extending Base

class App(Base):
    __tablename__ = 'app'


id = Column(Integer, primary_key=True)
app_name = Column(String, nullable=False)
```

### Defining data in data.py

- You must declare a data_to_insert list to store optional data that may be inserted into the schema's tables.

```python
from database1.schema1.tables import App

# 1. Mandatory: Initialize a list for optional data insertion
data_to_insert = []
# Optional: Append data to be inserted into the table
data_to_insert.append(App(app_name="example_app"))
```

### Defining function or stored procedure in stored_procedures_and_functions package

- paste this logic in the `__init__.py` of this package to discover all sql files.

```python
from pathlib import Path

directory = Path(__file__).parent
stored_procedures_and_functions = []

for file_path in directory.iterdir():
    if file_path.is_file() and file_path.suffix == ".sql":
        with file_path.open("r") as file:
            content = file.read()
            stored_procedures_and_functions.append(content)
```

- You can keep raw sql files each containing ideally 1 stored procedure or function.
- The name of the file should ideally correspond to the function / procedure name.
- This raw sql should be compatible with postgres database.

```sql
CREATE OR REPLACE FUNCTION add_user(
    p_username VARCHAR,
    p_email VARCHAR
) RETURNS TEXT AS $$
BEGIN
    -- Insert a new user into the users table
    INSERT INTO users (username, email)
    VALUES (p_username, p_email);

    -- Return a success message
    RETURN 'User added successfully!';
END;
$$ LANGUAGE plpgsql;

```

### Centralized Definitions in main.py

The main.py file is mandatory and contains a global list that maps databases to schemas and their corresponding table
definitions. This list is manually created by the user (for now).

#### Example main.py:

```python
# main.py

from database1.schema1 import global_string_schema_name as schema1_name
from database1.schema1.tables import Base as Schema1Base
from database1.schema1.data import data_to_insert as schema1_data
from database1.schema1.stored_procedures_and_functions import (
    stored_procedures_and_functions as schema1_stored_procedures_and_functions)
from database1 import global_string_database_name as database1_name

# Global list that maps databases and schemas

global_list_create = [
    {
        "database": database1_name,  # Mandatory: Database name
        "schemas": [
            {
                "schema": schema1_name,  # Mandatory: Schema name
                "base": Schema1Base,  # Mandatory: Base for this schema
                "data_to_insert": schema1_data,  # Mandatory: Data to insert (even if empty)
                "stored_procedures_and_functions": schema1_stored_procedures_and_functions,
                # Mandatory: stored procedures and functions (even if empty)
            },
        ],
    }
]
```

This file centralizes the definition of each database and schema, including the associated Base and data_to_insert for
table definitions.

### Creating Tables

Once you have defined your databases, schemas, and tables, you can create them in your PostgreSQL database by using the
`create_database_and_tables` function.

```python
from square_database_structure import create_database_and_tables

# Define the database connection details
db_username = "your_username"
db_password = "your_password"
db_ip = "localhost"
db_port = 5432

# Call the function to create the database and tables
create_database_and_tables(db_username, db_password, db_ip, db_port)
```

## env

- python>=3.12.0

## note

this module is planned to deviate a bit from the SemVer system for version numbers Major.x and x.Minor.x increments will
denote changes in application logic, while x.x.Patch increments will denote changes in database data or structure.

## changelog

### v2.5.9

- square
    - public
        - update TestEnumEnum.

### v2.5.8

- square
    - public
        - add more datatypes / columns in test table.
        - in test table convert test_text to nullable.

### v2.5.7

- square
    - authentication
        - make user_verification_code_expires_at nullable in UserVerificationCode table.

### v2.5.6

- square
    - authentication
        - add user_profile_phone_number_country_code in UserProfile table.
        - update unique constraint for phone number to account for user_profile_phone_number_country_code.

### v2.5.5

- square
    - email
        - fix schema name import.

### v2.5.4

- square
    - authentication
        - add UserVerificationCode.
        - add user_profile_email_verified in UserProfile table.
        - add VerificationCodeTypeEnum.
        - add AuthProviderEnum.
        - add UserAuthProvider.
        - move username from UserProfile to User.
    - email
        - new schema.
        - add EmailLog table.
        - add EmailTypeEnum.
        - add EmailStatusEnum.

### v2.5.3

- square
    - public
        - make test_text unique.

### v2.5.2

- square
    - authentication
        - remove user_status enum and column from User.
        - add RecoveryMethodEnum.
        - add UserRecoveryMethod table.

### v2.5.1

- square
    - file_storage
        - remove file_is_deleted and file_date_deleted from File table.

### v2.5.0

- testing
    - remove conftest file and all fixtures.
    - remove test_create_database_and_tables.
    - modify pytest workflow.
    - rename test file.

### v2.4.0

- testing
    - add fixture_create_database_and_tables for cleanup.

### v2.3.1

- square
    - authentication
        - remove user_credential_username from UserCredential table.
        - add UserProfile table.

### v2.3.0

- remove hardcoded testing database creds from pytest.

### v2.2.0

- add test_create_database_and_tables.

### v2.1.0

- add testing framework.

### v2.0.0

- replace force_recreate_tables optional param to drop_if_exists.

### v1.4.0

- add force_recreate_tables optional param to create_database_and_tables.

### v1.3.4

- remove app raspi_home inside square->public->app.
- remove app_id column from square->greeting->greeting.

### v1.3.3

- add new app raspi_home inside square->public->app.
- add new schema square->greeting with 1 table Greeting.

### v1.3.2

- update to versioning plan.
- add test app in square->public->app.

### v1.3.1

- update license in setup.py.

### v1.3.0

- add support for stored procedures and functions.

### v1.2.0

- move data to separate file for each schema.
- add enums file for each schema.

### v1.1.0

- add database, schema and table creation logic (from square database) (removed logs).

### v1.0.3

- change structure of square->authentication->UserApp and square->authentication->UserSession (due to complications with
  Composite Key).
- change default data in square->public->app.

### v1.0.2

- replace file_purpose with app_id in file_storage.

### v1.0.1

- add main.py file to have explicit mapping and ordering for schemas to be created.
- move database and schema names to `__init__.py`.
- add app table in public, change user, remove profile and add user app and remove enums.

### v1.0.0

- initial commit.

## Feedback is appreciated. Thank you!

# python-package-template

To create local package and remote package layers (not to create GraphQL and REST-API layers)

# TODO

Support new automated fields such as<br>

## Geo fields

${{ profile.main_city_name }}

## Birthday

${{ person.day_to_birthday }}

# Used by

Dialog Workflow<br>
Messages<br>

# directory structure

Root directory should have only .github/, ,gitignore, README.md and the project directory (i.e.
location_local_python_package same as repo) - This will allow is to easily switch to mono repo<br>
/location_local<br>
/location_local/get_country_name<br>
/location_local/get_country_name/src<br>
/location_local/get_country_name/src/get_country_name.py<br>
/location_local/get_country_name/tests<br>
/location_local/get_country_name/tests/get_country_name_test.py<br>

# database Python scripts in /db folder

Please place <table-name>.py in /db<br>
No need for seperate file for _ml table<br>
Please delete the example file if not needed<br>

# Create the files to create the database schema, tables, view and populate metadata and Test-Data

/db/<table-name>.py - CREATE SCHEMA ... CREATE TABLE ... CREATE VIEW ... including _ml_table<br>
/db/<table-name>_insert.py to create metadata and Test-Data records

# Update the setup.py (i.e.name, version)

# Please create test directory inside the directory of the project i.e. /<project-name>/tests

# Update the serverless.yml in the root directory

provider:
stage: play1

Update the endpoints in serverless.yml

# Working with VS Code

Please make sure you push to the repo launch.json fie that enables to run and debug the code<br>

# Unit-Test

We prefer using pytest and not unittest package<br>

Please create pytest.init in the project-directory and not in the root directory

```
[pytest]
markers =
    test: custom mark for tests
```

# When you took care of all the TODOs in the repo, using our infrastructure classes (i.e. Logger, Database, Url, Importer ...) your Feature Branch GitHub Actions Workflow is Green without warnings, all tests are running in GHA, code is documented, README.md is clean and self explained, test coverage is above 90% and all your lines are covered with Unit-Tests, you can filter and analyse your records in Logz.io, pull dev to your Feature Branch and only then create Pull Request to dev

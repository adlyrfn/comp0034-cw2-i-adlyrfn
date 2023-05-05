# COMP0034 Coursework 2

## Set-up

You will need to a Python environment e.g create and activate a venv.

Install the packages from requirements.txt using `pip install -r requirements.txt`

To run the code pass through the following command via terminal `flask --app 'cycling_app:create_app()' --debug run`

To run the tests pass through ` python -m pytest -vv tests/tests_cycling_app/ -W ignore::DeprecationWarning`

### The routes

The following routes were designed for the API.

| HTTP method | URL | Body | Response | Where the data is |
|:---- |:---- |:---- |:---- | :---- |
| GET | api/noc | None | Returns a list of NOC region codes with region name and notes | `noc_regions.csv` |
| GET | api/noc/{code} | None | Returns the region name and notes for a given code | `noc_regions.csv` |
| PATCH | api/noc/{code} | Changed fields for the NOC record| Return all the details of the updated NOC record|`noc_regions.csv` | `noc_regions.csv` |
| POST | api/noc | Region code, region name and (optional) notes | Status code 201 if new NOC code was saved. | `noc_regions.csv` |
| DELETE | api/noc/{code} | None | Removes an NOC code and if successful returns  202 (Accepted) | `noc_regions.csv` |
| GET | api/event | None | Returns a list of events with all details | `paralympics.csv` |
| GET | api/event/{event_id} | None | Returns all the details for a given event |`paralympics.csv` |
| POST | api/event | Event details| Status code 201 if new event was saved. |`paralympics.csv` |
| PATCH | api/event/{event_id} | Event details to be updated (specific fields to be passed) | Return all the details of the updated event|`paralympics.csv` |

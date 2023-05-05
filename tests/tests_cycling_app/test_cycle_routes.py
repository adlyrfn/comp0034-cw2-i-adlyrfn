from cycling_app.models import Cycling
from cycling_app import db

def test_get_all_cyclings(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/cyclings'
    THEN the status code should be 200, the Location 'Millbank (south of Thorney Street)' should be in the response data and the content type "application/json"
    """
    response = test_client.get("/cyclings")
    assert response.status_code == 200
    assert b"Millbank (south of Thorney Street)" in response.data
    assert response.content_type == "application/json"

def test_add_cycling(test_client):
    """
    GIVEN a Cycling model
    WHEN the HTTP POST request is made to /cyclings
    THEN a new cycling should be inserted in the database so there is 1 more row; and the response returned with the new cycling in JSON format
    """

    cycling = Cycling(
        Survey_wave = "New_survey wave",
        Location = "New_location",
        Survey_date = "New_survey_date",
        Weather = "New_weather",
        Time = "New_time",
        Period = "New_period",
        Direction = "New_direction",
        Number_of_private_cycles = "New_number_of_private_cycles",
        Number_of_cycle_hire_bikes = "New_number_of_cycle_hire_bikes",
        Total_cycles = "New_total_cycles",
        Year = "New_year",
        cycling_id = "New_cycling_id",
    )

    cycling_json = {
        "Survey_wave" : "New_survey wave",
        "Location" : "New_location",
        "Survey_date" : "New_survey_date",
        "Weather" : "New_weather",
        "Time" : "New_time",
        "Period" : "New_period",
        "Direction" : "New_direction",
        "Number_of_private_cycles" : 10,
        "Number_of_cycle_hire_bikes" : 10,
        "Total_cycles" : 20,
        "Year" : 2023,
        "cycling_id" : 999999,
    }

    # Check if the cycling data exists, it does then delete it
    exists = db.session.execute(
        db.select(Cycling).filter_by(Survey_wave=cycling.Survey_wave)
    ).scalar()
    if exists:
        db.session.execute(db.delete(Cycling).where(Cycling.Survey_wave == cycling.Survey_wave))
        db.session.commit()

    # Count() is not well explained in the documentation, try
    # https://github.com/sqlalchemy/sqlalchemy/issues/5908
    # Count the number of cycling data before adding a new one
    num_cyclings_in_db = db.session.scalar(
        db.select(db.func.count()).select_from(Cycling)
    )
    # Add a new cycling data
    response = test_client.post("/cyclings", json=cycling_json)
    # Count the number of cycling data  after the new cycling data is added
    num_cyclings_in_db_after = db.session.scalar(
        db.select(db.func.count()).select_from(Cycling)
    )
    data = response.json
    assert response.status_code == 201
    assert "New_survey wave" in data["Survey_wave"]
    assert (num_cyclings_in_db_after - num_cyclings_in_db) == 1


def test_get_specific_region(test_client):
    """
    GIVEN a running Flask app
    WHEN the "/cyclings/<location>/<survey_date_formatted>/<time>/<direction>" route is requested with the
    Millbank (south of Thorney Street)/24 1 2014 12:00:00 AM/0600 - 0615/Northbound code
    THEN the response should contain the cycling_id 1
    """
    # The expected result is defined 
    expected_result = {
        "Survey_wave" : "2014 Q1 (January-March)",
        "Location" : "Millbank (south of Thorney Street)",
        "Survey_date" : "24/1/2014 0:00",
        "Weather" : "Dry",
        "Time" : "0600 - 0615",
        "Period" : "Early Morning (06:00-07:00)",
        "Direction" : "Northbound",
        "Number_of_private_cycles" : 0,
        "Number_of_cycle_hire_bikes" : 0,
        "Total_cycles" : 0,
        "Year" : 2014,
        "cycling_id" : 1,
    }
    
    # A GET request is made to the API endpoint with parameters stated
    response = test_client.get("/cyclings/Millbank (south of Thorney Street)/24 1 2014 12:00:00 AM/0600 - 0615/Northbound")

    # Check response is of status code is 200
    assert response.status_code == 200

    # Check response of body has expected result
    assert response.json == expected_result

def test_delete_region(test_client):
    """
    GIVEN a cyclings json AND the cyclings is in the database
    WHEN the DELETE "/cyclings/<location>/<survey_date_formatted>/<time>/<direction>" route is called
    THEN check the fields are defined correctly
    """
    # A new cycling record is created in the databse
    cycling_new = Cycling(
        Survey_wave = "Test_survey_wave",
        Location = "Test_new_location",
        Survey_date = "24/1/2014  12:00:00 AM",
        Weather = "Test_weather",
        Time = "0600 - 0615",
        Period = "Early Morning (06:00-07:00)",
        Direction = "Westbound",
        Number_of_private_cycles = 123,
        Number_of_cycle_hire_bikes = 123,
        Total_cycles = 246,
        Year = 2014,
        cycling_id = 999999,
    )
    db.session.add(cycling_new)
    db.session.commit()

    # The DELETE route for cycling_new is called
    response = test_client.delete(f"/cyclings/Test_new_location/24 1 2014 12:00:00 AM/0600 - 0615/Westbound")

    # Check response if successful (code status 200)
    assert response.status_code == 200

    # Check if new cycling data has been deleted
    deleted_cycling_new = Cycling.query.filter_by(
        Location = "Test_new_location",
        Survey_date = "24 1 2014 12:00:00 AM",
        Time = "0600 - 0615",
        Direction = "Westbound",        
    ).first()
    assert deleted_cycling_new is None
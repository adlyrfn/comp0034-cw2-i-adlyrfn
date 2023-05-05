from cycling_app.models import Cycling
from cycling_app import db

def test_get_all_cyclings(test_client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/cyclings'
    THEN the status code should be 200, the Location 'Millbank (south of Thorney Street)' should be in the response data and the content type "application/json"
    """
    response = test_client.get("/api/cyclings")
    assert response.status_code == 200
    assert b"Millbank (south of Thorney Street)" in response.data
    assert response.content_type == "application/json"

def test_add_cycling(test_client):
    """
    GIVEN a Cycling model
    WHEN the HTTP POST request is made to /cyclings
    THEN a new cycling should be inserted in the database so there is 1 more row; and the response returned with the new region in JSON format
    """
    cycling = Cycling(
        Survey_wave="New_survey_wave",
        Location="New_location",
        Survey_date="New_survey_date",
        Weather="New_weather",
        Time="New_time",
        Period="New_period",
        Direction="New_direction",
        Number_of_private_cycles=123,
        Number_of_cycle_hire_bikes=123,
        Total_cycles=246,
        Year=2023,
        cycling_id=9999,
    )

    cycling_json = {
        "Survey_wave": "New_survey_wave",
        "Survey_wave":"New_survey_wave",
        "Location":"New_location",
        "Survey_date":"New_survey_date",
        "Weather":"New_weather",
        "Time":"New_time",
        "Period":"New_period",
        "Direction":"New_direction",
        "Number_of_private_cycles":123,
        "Number_of_cycle_hire_bikes":123,
        "Total_cycles":246,
        "Year":2023,
        "cycling_id":9999,
    }

    # Check if the cycling data exists, if it does then delete it
    exists = db.session.execute(
        db.select(Cycling).filter_by(cycling_id=cycling.cycling_id)
    ).scalar()
    if exists:
        db.session.execute(db.delete(Cycling).where(Cycling.cycling_id == cycling.cycling_id))
        db.session.commit()

    # Count the number of regions before adding a new one
    num_regions_in_db = db.session.scalar(
        db.select(db.func.count()).select_from(Cycling)
    )
    # Add a new region
    response = test_client.post("/api/cyclings", json=cycling_json)
    # Count the number of regions after the new region is added
    num_regions_in_db_after = db.session.scalar(
        db.select(db.func.count()).select_from(Cycling)
    )
    data = response.json
    assert response.status_code == 201
    assert "New_survey_wave" in data["Survey_wave"]
    assert (num_regions_in_db_after - num_regions_in_db) == 1

def test_get_specific_region(test_client):
    """
    GIVEN a running Flask app
    WHEN the "/api/cyclings/<location>/<survey_date>/<time>/<direction>" route is requested with the 
    /Millbank (south of Thorney Street)/24 1 2014 12:00:00 AM/0600 - 0615/Northbound code
    THEN the response should contain the Weather Dry
    """
    response = test_client.get("/api/cyclings/Millbank (south of Thorney Street)/24 1 2014 12:00:00 AM/0600 - 0615/Northbound")
    data =response.json
    assert data["cycling_id"] == 1
    assert response.status_code == 200

def test_delete_region(test_client):
    """
    GIVEN a cycling data json AND the cycling data is in the database
    WHEN the DELETE "/api/cyclings/<location>/<survey_date>/<time>/<direction>" route is called
    THEN check the fields are defined correctly
    """
    # A new cycling is created
    cycling = Cycling(
        Survey_wave="2023 Q1 (January-March)",
        Location="Malaysia",
        Survey_date="24 1 2023 12:00:00 AM",
        Weather="Dry",
        Time="0600 - 0615",
        Period="Early Morning (06:00-07:00)",
        Direction="Northbound",
        Number_of_private_cycles=321,
        Number_of_cycle_hire_bikes=321,
        Total_cycles=642,
        Year=2023,
        cycling_id=1234,
    )
    db.session.add(cycling)
    db.session.commit()

    # Check whether the data is in the database
    assert db.session.query(Cycling).filter_by(cycling_id=1234).first() is not None

    # A DELETE request is passed through to the API to delete the data
    response = test_client.delete("/api/cyclings/Malaysia/24 1 2023 12:00:00 AM/0600 - 0615/Northbound")

    # Check if resoonse is 200
    assert response.status_code == 200

    # Check cycling data has been deleted from database
    assert db.session.query(Cycling).filter_by(cycling_id=1234).first() is None
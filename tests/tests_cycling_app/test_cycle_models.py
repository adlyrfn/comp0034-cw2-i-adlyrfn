from cycling_app.models import Cycling


def test_create_new_cycling():
    """
    GIVEN json for a cycling data
    WHEN a new Cycling object is created
    THEN check the fields are defined correctly
    """
    r = Cycling(
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
    assert r.Survey_wave == "New_survey_wave"
    assert r.Location == "New_location"
    assert r.Survey_date == "New_survey_date"
    assert r.Weather == "New_weather"
    assert r.Time == "New_time"
    assert r.Period == "New_period"
    assert r.Direction == "New_direction"
    assert r.Number_of_private_cycles == 123
    assert r.Number_of_cycle_hire_bikes == 123
    assert r.Total_cycles == 246
    assert r.Year == 2023
    assert r.cycling_id == 9999

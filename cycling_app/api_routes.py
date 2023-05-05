from cycling_app.schemas import CyclingSchema
from cycling_app import db
from cycling_app.models import Cycling
from flask import (
    render_template,
    current_app as app,
    request,
    make_response,
    jsonify,
    abort,
    Blueprint,
)

# Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ------
# Schemas
# ------

cyclings_schema = CyclingSchema(many=True)
cycling_schema = CyclingSchema()

# ------
# Routes
# ------

@api_bp.get("/cyclings")
def cyclings():
    """Returns a list of all cycling data and their details in JSON format."""
    # Select all the locations using Flask SQLAlchemy
    all_locations = db.session.execute(db.select(Cycling)).scalars()
    # Obatin the data using Marshmallow schema (returns JSON)
    result = cyclings_schema.dump(all_locations)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    # Return the data requested
    return response

@api_bp.get("/cyclings/<location>/<survey_date>/<time>/<direction>")
def cyclings_loc_date_time_direction(location, survey_date, time, direction):
    """Returns the details for a given cycling data location, survey date, time and direction."""
    region = db.session.execute(
        db.select(Cycling).filter_by(
        Location=location,
        Survey_date=survey_date,
        Time=time,
        Direction=direction)
    ).scalar_one_or_none()
    if region:
        result = cycling_schema.dump(region)
        response = make_response(result, 200)
        response.headers["Content-Type"] = "application/json"
    else:
        message = jsonify(
            {
                "status": 404,
                "error": "Not found",
                "message": "Invalid resource URI",
            }
        )
        response = make_response(message, 404)
    return response

@api_bp.post("/cyclings")
def cyclings_add():
    """Adds a new cycling record to the dataset."""
    Survey_wave = request.json.get("Survey_wave", "")
    Location = request.json.get("Location", "")
    Survey_date = request.json.get("Survey_date", "")
    Weather = request.json.get("Weather", "")
    Time = request.json.get("Time", "")
    Period = request.json.get("Period", "")
    Direction = request.json.get("Direction", "")
    Number_of_private_cycles = request.json.get("Number_of_private_cycles", "")
    Number_of_cycle_hire_bikes = request.json.get("Number_of_cycle_hire_bikes", "")
    Total_cycles = request.json.get("Total_cycles", "")
    Year = request.json.get("Year", "")
    cycling_id = request.json.get("cycling_id", "")
    cycling = Cycling(Survey_wave=Survey_wave, Location=Location, Survey_date=Survey_date,
                    Weather=Weather, Time=Time, Period=Period, Direction=Direction,
                    Number_of_private_cycles=Number_of_private_cycles,
                    Number_of_cycle_hire_bikes=Number_of_cycle_hire_bikes,
                    Total_cycles=Total_cycles, Year=Year, cycling_id=cycling_id,)
    db.session.add(cycling)
    db.session.commit()
    result = cycling_schema.jsonify(cycling)
    response = make_response(result, 201)
    response.headers["Content-type"] = "application/json"
    return response

@api_bp.patch("/cyclings/<location>/<survey_date>/<time>/<direction>")
def cyclings_update(location, survey_date, time, direction):
    """Updates changed fields for the cycling data record

    TODO: Handle 404 error"""
    # Find the current cycling data in the database
    existing_region = db.session.execute(
        db.select(Cycling).filter_by(
        Location=location,
        Survey_date=survey_date,
        Time=time,
        Direction=direction
        )
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    region_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    cycling_schema.load(region_json, instance=existing_region, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(Cycling).filter_by(
        Location=location,
        Survey_date=survey_date,
        Time=time,
        Direction=direction
        )
    ).scalar_one_or_none()
    result = cycling_schema.jsonify(updated_region)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@api_bp.delete("/cyclings/<location>/<survey_date>/<time>/<direction>")
def cyclings_delete(location, survey_date, time, direction):
    """Removes a cycling record from the dataset.

    TODO: handle 404 error"""
    cycling = db.session.execute(
        db.select(Cycling).filter_by(
        Location=location,
        Survey_date=survey_date,
        Time=time,
        Direction=direction
        )
    ).scalar_one_or_none()
    db.session.delete(cycling)
    db.session.commit()
    # This example returns a custom HTTP response using flask make_response
    # https://flask.palletsprojects.com/en/2.2.x/api/?highlight=make_response#flask.make_response
    text = jsonify({"Successfully deleted": cycling.Location + cycling.Survey_date + cycling.Time + cycling.Direction})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response

def get_cyclings():
    """A function to get all cyclings from database as objects which will be converted to JSON"""
    all_cyclings = db.session.execute(db.select(Cycling)).scalars()
    cycling_json = cyclings_schema.dump(all_cyclings)
    return cycling_json

def get_cycling(cycling_id):
    """A function to get a single cycling as a json structure
    
    TODO: handle 404 error"""
    cycling = db.session.execute(
        db.select(Cycling).filter_by(cycling_id=cycling_id)
    ).scalar_one_or_none()
    result = cycling_schema.dump(cycling)
    return result

from cycling_app.models import Cycling
from cycling_app import db, ma

class CyclingSchema(ma.SQLAlchemySchema):
    """Marshmallow schema defining the attributes to create a new cycling"""

    class Meta:
        model = Cycling
        include_fk = True
        load_instance =True
        sqla_session = db.session

    Survey_wave = ma.auto_field()
    Location = ma.auto_field()
    Survey_date = ma.auto_field()
    Weather = ma.auto_field()
    Time = ma.auto_field()
    Period = ma.auto_field()
    Direction = ma.auto_field()
    Number_of_private_cycles = ma.auto_field()
    Number_of_cycle_hire_bikes = ma.auto_field()
    Total_cycles = ma.auto_field()
    Year = ma.auto_field()
    cycling_id = ma.auto_field()
from cycling_app import db

class Cycling(db.Model):
    """Prepared central london cycling"""

    __tablename__= "cycling"
    Survey_wave = db.Column(db.Text, nullable=False)
    Location = db.Column(db.Text, nullable=False)
    Survey_date = db.Column(db.Text, nullable=False)
    Weather = db.Column(db.Text, nullable=False)
    Time = db.Column(db.Text, nullable=False)
    Period = db.Column(db.Text, nullable=False)
    Direction = db.Column(db.Text, nullable=False)
    Number_of_private_cycles = db.Column(db.Integer, nullable=False)
    Number_of_cycle_hire_bikes = db.Column(db.Integer, nullable=False)
    Total_cycles = db.Column(db.Integer, nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    cycling_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        """
        Attributes of the event is return as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.Survey_wave},{self.Location},{self.Survey_date}, \
            {self.Weather},{self.Time},{self.Period},{self.Direction}, \
                {self.Number_of_private_cycles},{self.Number_of_cycle_hire_bikes}, \
                    {self.Total_cycles},{self.Year},{self.cycling_id}>"
    
    # Add this line to the mapper configuration
    __mapper_args__ = {"confirm_deleted_rows": False}
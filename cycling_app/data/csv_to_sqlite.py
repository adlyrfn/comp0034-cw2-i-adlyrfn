from pathlib import Path 
import pandas as pd
from sqlalchemy import create_engine, types, inspect
from sqlalchemy import create_engine, inspect
# from cycling_app.models import Cycling

# Define the database file name and location
db_file = Path(__file__).parent.joinpath("cycling.db")

# Create a connection to file as a SQLite database which creates file if it does not exist
engine = create_engine("sqlite:///" + str(db_file), echo=False )
inspector = inspect(engine)

# The prepared central london data is read to a pandas dataframe
cycling_file = Path(__file__).parent.joinpath("prepared_central_london_(area).csv")
cycling = pd.read_csv(cycling_file)

# The data read is written in a sqlite database
dtype_cycling = {
    "Survey_wave": types.TEXT(),
    "Location": types.TEXT(),
    "Survey_date": types.TEXT(),
    "Weather": types.TEXT(),
    "Time": types.TEXT(),
    "Period": types.TEXT(),
    "Direction": types.TEXT(),
    "Number_of_private_cycles": types.INTEGER(),
    "Number_of_cycle_hire_bikes": types.INTEGER(),
    "Total_cycles": types.INTEGER(),
    "Year": types.INTEGER(),
    "cycling_id": types.INTEGER(),
}

cycling.to_sql(
    "cycling", engine, if_exists="append", index=False, dtype=dtype_cycling
)

# columns = inspector.get_columns('cycling')
# for column in columns:
#     print(column['name'])
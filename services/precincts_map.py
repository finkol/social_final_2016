import csv

from flask import make_response
import StringIO

from services.soda_api import get_data
from sodapy import Socrata

client = Socrata("data.cityofnewyork.us", "Z9djfh6hUgBAIHC7gpZRscVBj")

offenses_dict = dict(RAPE=0, GRAND_LARCENY=1, ROBBERY=2, MURDER_NON_NEGL_MANSLAUGHTE=3, NA=4, FELONY_ASSAULT=5,
                     BURGLARY=6, GRAND_LARCENY_OF_MOTOR_VEHICLE=7)

def get_precincts_coordinates(year):
    offenses = get_data(content_type="csv", select="offense, location_1", where="occurrence_year =" + year)

    keys = ["lat", "lon", "offense_no"]
    si = StringIO.StringIO()
    dict_writer = csv.DictWriter(si, keys)
    dict_writer.writeheader()
    for offense in offenses[1:]:
        points = offense[0].replace("POINT (", "")
        points = points.replace(")", "").split()
        temp_dict = dict(offense_no=offenses_dict[offense[1].replace(".", "").replace("& ", "").replace("-", "_").replace(" ","_")], lat=points[0], lon=points[1])
        dict_writer.writerow(temp_dict)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=" + year + ".csv"
    output.headers["Content-type"] = "text/csv"

    return output


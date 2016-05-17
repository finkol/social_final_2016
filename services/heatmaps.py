import calendar
import csv

from flask import make_response
import StringIO
import re

from services.soda_api import get_data
from sodapy import Socrata

def get_time_heatmap():
    data = get_data(content_type="csv", select="day_of_week, occurrence_hour, count(objectid)", group="day_of_week, occurrence_hour")

    keys = ["day", "hour", "value"]
    si = StringIO.StringIO()
    dict_writer = csv.DictWriter(si, keys)
    dict_writer.writeheader()
    dow = dict(zip('Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split(),range(7)))
    for line in data[1:]:
        print line
        if line[1] in dow and line[2] != "NA":
            temp_dict = dict(
                day=dow[line[1]], hour=line[2], value=line[0])
            dict_writer.writerow(temp_dict)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=heatmap.csv"
    output.headers["Content-type"] = "text/csv"

    return output

def get_month_heatmap():
    data = get_data(content_type="csv", select="occurrence_month, occurrence_day, count(objectid)", group="occurrence_month, occurrence_day")
    keys = ["month", "day", "value"]
    si = StringIO.StringIO()
    dict_writer = csv.DictWriter(si, keys)
    dict_writer.writeheader()
    months = dict(zip('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(), range(12)))
    print months
    for line in data[1:]:
        print line
        if line[2] in months and line[1] != "NA":
            temp_dict = dict(
                month=months[line[2]], day=line[1], value=line[0])
            dict_writer.writerow(temp_dict)
            print temp_dict
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=heatmap_months.csv"
    output.headers["Content-type"] = "text/csv"
    print months
    return output
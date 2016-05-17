import os

from flask import Flask, jsonify, request, make_response, render_template

from services.base_calculations import offense_by_borough_compared_to_other_boroughs
from services.decision_tree import predict_crime
from services.precincts_map import get_precincts_coordinates, offenses_dict
from services.soda_api import get_data
from services.heatmaps import get_time_heatmap, get_month_heatmap

app = Flask(__name__)


@app.route('/get_test_data')
def GET_test_data():
    return jsonify(all_data=get_data(select="offense, count(offense)", group="offense"))


@app.route('/get_felonies_by_offense_type')
def GET_felonies_by_offense_type():
    return jsonify(data=get_data(select="offense, count(offense)", group="offense"))


@app.route('/get_offense_by_borough_compared_to_other_boroughs')
def GET_offense_by_borough_compared_to_other_boroughs():
    return jsonify(data=offense_by_borough_compared_to_other_boroughs())

@app.route('/get_offenses_precincts')
def GET_offenses_precincts():
    year = request.args['year']
    return get_precincts_coordinates(year)

@app.route('/get_offenses_dict')
def GET_offenses_dict():
    return jsonify(data=list(offenses_dict))

@app.route('/get_time_heatmap')
def GET_time_heatmap():
    return get_time_heatmap()

@app.route('/get_month_heatmap')
def GET_month_heatmap():
    return get_month_heatmap()

@app.route('/predict_crime')
def GET_predict_crime():
    precinct = request.args['precinct']
    return jsonify(most_likely_offense=predict_crime(precinct))

@app.route('/')
def GET_page():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('index.html'), 200, headers)

@app.route('/machine_learning')
def GET_machine_learning_page():
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('machine_learning.html'), 200, headers)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 2400))
    app.run(host='0.0.0.0', port=port, debug=True)

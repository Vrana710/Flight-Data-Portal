from flask import Flask, request, jsonify, render_template
from data import FlightData
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Initialize FlightData
db_uri = 'sqlite:///data/flights.sqlite3'
data_manager = FlightData(db_uri)

@app.route('/', methods=['GET'])
def home():
    """
    This function is the route handler for 
    the root URL ("/") of the web application.
    It returns the rendered HTML template "Flight_Data_Portal.html".

    Parameters:
    None

    Returns:
    str: The rendered HTML content of the "Flight_Data_Portal.html" template.
    """
    return render_template("Flight_Data_Portal.html")

@app.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    results = data_manager.get_flight_by_id(flight_id)
    return jsonify(results)

@app.route('/flights/date', methods=['GET'])
def get_flights_by_date():
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_flights_by_date(day, month, year)
    return jsonify(results)

@app.route('/delayed/airline/<string:airline_name>', methods=['GET'])
def get_delayed_flights_by_airline(airline_name):
    results = data_manager.get_delayed_flights_by_airline(airline_name)
    return jsonify(results)

@app.route('/delayed/airport/<string:airport_code>', methods=['GET'])
def get_delayed_flights_by_airport(airport_code):
    results = data_manager.get_delayed_flights_by_airport(airport_code)
    return jsonify(results)

@app.route('/delayed/airlines', methods=['GET'])
def get_all_delayed_flights_grouped_by_airline():
    results = data_manager.get_all_delayed_flights_grouped_by_airline()
    return jsonify(results)

@app.route('/delayed/hour', methods=['GET'])
def get_delayed_flights_per_hour():
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_delayed_flights_per_hour(day, month, year)
    return jsonify(results)

@app.route('/heatmap', methods=['GET'])
def get_flight_delays_heatmap():
    results = data_manager.get_flight_delays_heatmap()
    return jsonify(results.to_dict(orient='records'))

@app.route('/average/routes', methods=['GET'])
def get_delayed_flights_average_per_route():
    results = data_manager.get_delayed_flights_average_per_route()
    return jsonify(results)

@app.route('/route-map', methods=['GET'])
def get_delayed_flights_per_route_map():
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_delayed_flights_per_route_map(day, month, year)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
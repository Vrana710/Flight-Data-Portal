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
    This function is the route handler for the root URL ("/") of the web application.
    It returns the rendered HTML template "Flight_Data_Portal.html".

    Parameters:
    None

    Returns:
    str: The rendered HTML content of the "Flight_Data_Portal.html" template.
    """
    return render_template("Flight_Data_Portal.html")

@app.route('/flight/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    """
    Retrieves flight data by its unique identifier from the database.

    Parameters:
    flight_id (int): The unique identifier of the flight to retrieve.

    Returns:
    flask.Response: A JSON response containing the flight data.
    If the flight with the specified ID is not found, 
    an empty JSON object is returned.
    """
    results = data_manager.get_flight_by_id(flight_id)
    return jsonify(results)

@app.route('/flights/date', methods=['GET'])
def get_flights_by_date():
    """
    Retrieves flight data based on the specified date.

    Parameters:
    day (str): The day of the month for which to retrieve flight data.
    month (str): The month for which to retrieve flight data.
    year (str): The year for which to retrieve flight data.

    Returns:
    flask.Response: A JSON response containing 
    the flight data for the specified date.
    If the required parameters are missing, 
    an error message is returned with a 400 status code.
    The JSON response is in the following format:
    [
        {
            "flight_id": unique_flight_identifier,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "airline_name": airline_name,
            "airport_code": airport_code,
            ...
        },
        ...
    ]
    """
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_flights_by_date(day, month, year)
    return jsonify(results)


@app.route('/delayed/airline/<string:airline_name>', methods=['GET'])
def get_delayed_flights_by_airline(airline_name):
    """
    Retrieves delayed flight data for a specific airline from the database.

    Parameters:
    airline_name (str): The name of the airline for 
    which to retrieve delayed flight data.

    Returns:
    flask.Response: A JSON response containing 
    the delayed flight data for the specified airline.
    The JSON response is in the following format:
    [
        {
            "flight_id": unique_flight_identifier,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "airline_name": airline_name,
            "airport_code": airport_code,
            ...
        },
        ...
    ]
    If the airline with the specified name is not found, 
    an empty JSON object is returned.
    """
    results = data_manager.get_delayed_flights_by_airline(airline_name)
    return jsonify(results)


@app.route('/delayed/airport/<string:airport_code>', methods=['GET'])
def get_delayed_flights_by_airport(airport_code):
    """
    Retrieves delayed flight data for a specific airport from the database.

    Parameters:
    airport_code (str): The code of the airport 
    for which to retrieve delayed flight data.

    Returns:
    flask.Response: A JSON response containing 
    the delayed flight data for the specified airport.
    The JSON response is in the following format:
    [
        {
            "flight_id": unique_flight_identifier,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "airline_name": airline_name,
            "airport_code": airport_code,
            ...
        },
        ...
    ]
    If the airport with the specified code is not found, 
    an empty JSON object is returned.
    """
    results = data_manager.get_delayed_flights_by_airport(airport_code)
    return jsonify(results)


@app.route('/delayed/airlines', methods=['GET'])
def get_all_delayed_flights_grouped_by_airline():
    """
    Retrieves all delayed flight data grouped 
    by airline from the database.

    Parameters:
    None

    Returns:
    flask.Response: A JSON response containing 
    the delayed flight data grouped by airline.
    The JSON response is in the following format:
    {
        "airline1": [
            {
                "flight_id": unique_flight_identifier,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "airline_name": airline_name,
                "airport_code": airport_code,
                ...
            },
            ...
        ],
        "airline2": [
            {
                "flight_id": unique_flight_identifier,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "airline_name": airline_name,
                "airport_code": airport_code,
                ...
            },
            ...
        ],
        ...
    }
    If no delayed flights are found, 
    an empty JSON object is returned.
    """
    results = data_manager.get_all_delayed_flights_grouped_by_airline()
    return jsonify(results)

@app.route('/delayed/hour', methods=['GET'])
def get_delayed_flights_per_hour():
    """
    Retrieves the number of delayed flights per hour for a specific date.

    Parameters:
    day (str): The day of the month for which to retrieve delayed flight data.
    month (str): The month for which to retrieve delayed flight data.
    year (str): The year for which to retrieve delayed flight data.

    Returns:
    flask.Response: A JSON response containing the number of 
    delayed flights per hour for the specified date.
    If the required parameters are missing, an error 
    message is returned with a 400 status code.
    The JSON response is in the following format:
    [
        {
            "hour": hour_of_day,
            "delayed_flights": number_of_delayed_flights
        },
        ...
    ]
    The 'delayed_flights' field represents the number of delayed flights 
    that occurred during the specified hour.
    """
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_delayed_flights_per_hour(day, month, year)
    return jsonify(results)


@app.route('/heatmap', methods=['GET'])
def get_flight_delays_heatmap():
    """
    Retrieves flight delay data from the database and 
    returns it in a format suitable for a heatmap visualization.

    Parameters:
    None

    Returns:
    flask.Response: A JSON response containing flight delay 
    data in the following format:
    [
        {
            "day": day_of_month,
            "month": month,
            "year": year,
            "airport_code": airport_code,
            "delay_time": average_delay_time
        },
        ...
    ]
    The JSON response is a list of dictionaries, where each 
    dictionary represents a day-airport combination.
    The 'delay_time' field represents the average delay time 
    for flights departing from the specified airport on the given day.
    """
    results = data_manager.get_flight_delays_heatmap()
    return jsonify(results.to_dict(orient='records'))

@app.route('/average/routes', methods=['GET'])
def get_delayed_flights_average_per_route():
    """
    This function retrieves the average number of delayed flights per route 
    from the flight data database.

    Parameters:
    None

    Returns:
    flask.Response: A JSON response containing 
    the average number of delayed flights per route.
    The JSON response is in the following format:
    {
        "route1": average_delay_time1,
        "route2": average_delay_time2,
        ...
    }
    """
    results = data_manager.get_delayed_flights_average_per_route()
    return jsonify(results)

@app.route('/route-map', methods=['GET'])
def get_delayed_flights_per_route_map():
    """
    This function retrieves delayed flight data for a specific date 
    and returns it in a format suitable for a route map.

    Parameters:
    day (str): The day of the month for which to retrieve delayed flight data.
    month (str): The month for which to retrieve delayed flight data.
    year (str): The year for which to retrieve delayed flight data.

    Returns:
    flask.Response: A JSON response containing the delayed 
    flight data for the specified date. If the required parameters are missing,
    an error message is returned with a 400 status code.
    """
    day = request.args.get('day')
    month = request.args.get('month')
    year = request.args.get('year')

    if not (day and month and year):
        return jsonify({'error': 'Missing parameters'}), 400

    results = data_manager.get_delayed_flights_per_route_map(day, month, year)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
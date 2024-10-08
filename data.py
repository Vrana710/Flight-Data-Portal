"""
This module provides functionality for retrieving and analyzing flight data
from a SQL database.
"""

import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class FlightData:
    """
    Class for handling flight data operations with a database.
    """
    def __init__(self, db_uri):
        """
        Initialize the FlightData object with a database URI.

        :param db_uri: Database URI.
        """
        logging.basicConfig(level=logging.INFO)
        self._engine = create_engine(db_uri)


    def _execute_query(self, query, params=None):
        """
        Execute a SQL query with optional parameters and return the
        results as a list of dictionaries.
        :param query: SQL query to execute.
        :param params: Parameters for the SQL query.
        :return: List of dictionaries representing the query result.
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except SQLAlchemyError as ex:
            logging.error("SQLAlchemy Error: %s", ex)
            return []


    def get_flight_by_id(self, flight_id):
        """
        Retrieve flight details by flight ID.
        :param flight_id: ID of the flight.
        :return: List of dictionaries containing flight details.
        """
        params = {'id': flight_id}
        query = """
        SELECT flights.*, airlines.airline, flights.ID AS FLIGHT_ID, 
               COALESCE(NULLIF(flights.DEPARTURE_DELAY,''), 0) AS DELAY 
        FROM flights 
        JOIN airlines ON flights.airline = airlines.id 
        WHERE flights.ID = :id
        """
        return self._execute_query(query, params)


    def get_flights_by_date(self, day, month, year):
        """
        Retrieve flights for a specific date.
        :param day: Day of the flight.
        :param month: Month of the flight.
        :param year: Year of the flight.
        :return: List of dictionaries containing flight details.
        """
        params = {'day': day, 'month': month, 'year': year}
        query = """
        SELECT flights.*, airlines.airline, flights.ID AS FLIGHT_ID,
               COALESCE(NULLIF(flights.DEPARTURE_DELAY,''), 0) AS DELAY  
        FROM flights 
        JOIN airlines ON flights.airline = airlines.id 
        WHERE flights.DAY = :day 
              AND flights.MONTH = :month 
              AND flights.YEAR = :year
        """
        return self._execute_query(query, params)


    def get_delayed_flights_by_airline(self, airline_name):
        """
        Retrieve delayed flights for a specific airline.
        :param airline_name: Name of the airline.
        :return: List of dictionaries containing delayed flights.
        """
        params = {'airline_name': airline_name}
        query = """
        SELECT flights.*, airlines.airline, flights.ID AS FLIGHT_ID,
               COALESCE(NULLIF(flights.DEPARTURE_DELAY,''), 0) AS DELAY 
        FROM flights 
        JOIN airlines ON flights.airline = airlines.id 
        WHERE airlines.airline = :airline_name 
              AND COALESCE(NULLIF(flights.DEPARTURE_DELAY, ''), 0) > 20 
              AND flights.DEPARTURE_DELAY IS NOT NULL
        """
        return self._execute_query(query, params)


    def get_all_delayed_flights_grouped_by_airline(self):
        """
        Retrieve all delayed flights grouped by airline.
        :return: List of dictionaries containing delayed flights by airline.
        """
        query = """
        SELECT airlines.airline, 
               COUNT(*) AS delay_count
        FROM flights
        JOIN airlines ON flights.airline = airlines.id
        WHERE COALESCE(NULLIF(flights.DEPARTURE_DELAY, ''), 0) > 20 
              GROUP BY airlines.airline
        """
        return self._execute_query(query)


    def get_delayed_flights_by_airport(self, airport_code):
        """
        Retrieve delayed flights for a specific airport.
        :param airport_code: Code of the airport.
        :return: List of dictionaries containing delayed flights.
        """
        params = {'airport_code': airport_code}
        query = """
        SELECT flights.*, airlines.airline, flights.ID AS FLIGHT_ID, 
               COALESCE(NULLIF(flights.DEPARTURE_DELAY,''), 0) AS DELAY 
        FROM flights 
        JOIN airlines ON flights.airline = airlines.id 
        WHERE flights.ORIGIN_AIRPORT = :airport_code 
              AND COALESCE(NULLIF(flights.DEPARTURE_DELAY, ''), 0) > 20 
              AND flights.DEPARTURE_DELAY IS NOT NULL
        """
        return self._execute_query(query, params)


    def get_delayed_flights_per_hour(self, day, month, year):
        """
        Retrieve delayed flights grouped by hour for a specific date.
        :param day: Day of the flights.
        :param month: Month of the flights.
        :param year: Year of the flights.
        :return: List of dictionaries containing delayed flights per hour.
        """
        params = {'day': day, 'month': month, 'year': year}
        query = """
        WITH all_hours AS (
            SELECT '00' AS hour UNION ALL SELECT '01' UNION ALL SELECT '02'
            UNION ALL SELECT '03' UNION ALL SELECT '04' UNION ALL SELECT '05'
            UNION ALL SELECT '06' UNION ALL SELECT '07' UNION ALL SELECT '08'
            UNION ALL SELECT '09' UNION ALL SELECT '10' UNION ALL SELECT '11'
            UNION ALL SELECT '12' UNION ALL SELECT '13' UNION ALL SELECT '14'
            UNION ALL SELECT '15' UNION ALL SELECT '16' UNION ALL SELECT '17'
            UNION ALL SELECT '18' UNION ALL SELECT '19' UNION ALL SELECT '20'
            UNION ALL SELECT '21' UNION ALL SELECT '22' UNION ALL SELECT '23'
        ),

        hourly_stats AS (
            SELECT 
                -- Extract the hour from the departure time (assuming it's in HHMM format)
                substr('00' || DEPARTURE_TIME, -4, 2) AS hour,
                COUNT(*) AS total_count,
                SUM(CASE WHEN COALESCE(NULLIF(DEPARTURE_DELAY, ''), 0) > 20 THEN 1 ELSE 0 END) AS delayed_count
            FROM flights
            WHERE YEAR = 2015 AND MONTH = 1 AND DAY = 1
            GROUP BY hour
        )

        SELECT h.hour,
            COALESCE(s.delayed_count, 0) AS delayed_count,
            COALESCE(s.total_count, 0) AS total_count
        FROM all_hours h
        LEFT JOIN hourly_stats s ON h.hour = s.hour
        ORDER BY h.hour;
        """
        return self._execute_query(query, params)


    def get_flight_delays_heatmap(self):
        """
        Retrieve a heatmap of flight delays between airports.
        :return: DataFrame with origin, destination, and percentage of
                delayed flights.
        """
        query = """
        SELECT f.ORIGIN_AIRPORT AS origin_airport,
               f.DESTINATION_AIRPORT AS destination_airport,
               COUNT(*) AS total_flights,
               SUM(CASE WHEN COALESCE(NULLIF(f.DEPARTURE_DELAY, ''), 0) > 20
                        THEN 1 ELSE 0 END) AS delayed_flights
        FROM flights f
        WHERE f.CANCELLED = 0 AND f.DIVERTED = 0
        GROUP BY f.ORIGIN_AIRPORT, f.DESTINATION_AIRPORT
        """
        results = self._execute_query(query)
        new_data_frame = pd.DataFrame(results)
        new_data_frame['percentage'] = (
            (new_data_frame['delayed_flights'] / new_data_frame['total_flights']) * 100
        )
        return new_data_frame[['origin_airport', 'destination_airport', 'percentage']]

    def get_delayed_flights_average_per_route(self):
        """
        Retrieve average percentage of delayed flights per route.
        :return: List of dictionaries containing average delay percentages.
        """
        query = """
        WITH flight_data AS (
            SELECT f.ORIGIN_AIRPORT,
                   f.DESTINATION_AIRPORT,
                   COUNT(*) AS total_count,
                   SUM(CASE WHEN COALESCE(NULLIF(f.DEPARTURE_DELAY, ''), 0) > 20 
                            THEN 1 ELSE 0 END) AS delay_count,
                   (SUM(CASE WHEN f.DEPARTURE_DELAY >= 20 
                             THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage,
                   ao.LATITUDE AS origin_latitude,
                   ao.LONGITUDE AS origin_longitude,
                   ad.LATITUDE AS destination_latitude,
                   ad.LONGITUDE AS destination_longitude
            FROM flights f
            JOIN airports ao ON f.ORIGIN_AIRPORT = ao.IATA_CODE
            JOIN airports ad ON f.DESTINATION_AIRPORT = ad.IATA_CODE
            GROUP BY f.ORIGIN_AIRPORT, f.DESTINATION_AIRPORT
        ),
        average_percentage AS (
            SELECT ORIGIN_AIRPORT,
                   DESTINATION_AIRPORT,
                   AVG(percentage) AS avg_percentage,
                   AVG(origin_latitude) AS origin_latitude,
                   AVG(origin_longitude) AS origin_longitude,
                   AVG(destination_latitude) AS destination_latitude,
                   AVG(destination_longitude) AS destination_longitude
            FROM flight_data
            GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
        )
        SELECT origin_latitude,
               origin_longitude,
               destination_latitude,
               destination_longitude,
               avg_percentage
        FROM average_percentage
        """
        return self._execute_query(query)


    def get_delayed_flights_per_route_map(self, day, month, year):
        """
        Retrieve delayed flights per route with percentage of
        delays for a specific date.
        :param day: Day of the flights.
        :param month: Month of the flights.
        :param year: Year of the flights.
        :return: List of dictionaries containing percentage of
        delayed flights per route.
        """
        params = {'day': day, 'month': month, 'year': year}
        query = """
        SELECT ORIGIN_AIRPORT AS origin_airport,
               DESTINATION_AIRPORT AS destination_airport,
               (SUM(CASE WHEN COALESCE(NULLIF(DEPARTURE_DELAY, ''), 0) > 20
                        THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS percentage
        FROM flights
        GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
        """
        return self._execute_query(query, params)


    def get_airport_coordinates(self):
        """
        Retrieve coordinates for all airports.
        :return: Dictionary with airport IATA codes as keys and
                tuples of (latitude, longitude) as values.
        """
        query = """
        SELECT IATA_CODE, LATITUDE, LONGITUDE 
        FROM airports
        """
        results = self._execute_query(query)
        coordinates = {}
        for row in results:
            iata_code = row['IATA_CODE']
            latitude = row['LATITUDE']
            longitude = row['LONGITUDE']
            if latitude and longitude:
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)
                    coordinates[iata_code] = (latitude, longitude)
                except ValueError:
                    logging.warning(
                        "Invalid coordinate values for %s: %s, %s",
                        iata_code, latitude, longitude
                    )
            else:
                logging.warning("Missing coordinate values for %s", iata_code)
        return coordinates


    def __del__(self):
        """Dispose of the SQLAlchemy engine when the object is deleted."""
        self._engine.dispose()

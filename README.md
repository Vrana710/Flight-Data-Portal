# Flight Data Portal

## Overview

The Flight Data Portal is a web application designed to query and visualize flight data. It provides various functionalities for retrieving and displaying flight information, including details by flight ID, flights by date, and delayed flights based on different criteria. The application uses Flask for the backend and a combination of HTML, CSS, and JavaScript for the frontend.

## Project Structure

- `api.py`: Flask backend API for handling flight data requests.
- `data.py`: Contains the `FlightData` class for interacting with the database.
- `main.py`: Command-line interface for interacting with flight data.
- `visualization.py`: Contains functions for visualizing flight data.
- `Flight_Data_Portal.html`: Main HTML file for the frontend user interface.
- `JS/script.js`: JavaScript file for handling frontend logic and API interactions.
- `css/style.css`: CSS file for styling the frontend.

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- SQLite (for the database)
- Pandas
- Matplotlib
- Seaborn
- Folium

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Vrana710/Flight-Data-Portal.git
   cd Flight-Data-Portal
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```bash
   pip3 install flask flask-cors sqlalchemy pandas matplotlib seaborn folium

   OR

   pip3 install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure the `data/flights.sqlite3` database file is present or set up the database as needed.

5. **Run the Flask server:**

   ```bash
   python3 api.py
   ```

6. **Open `Flight_Data_Portal.html` in a web browser to use the application.**


## Screenshots

Here are some screenshots of the application:

### Flight_Portal
![Flight_Portal](/static/images/Flight_Portal.png)

###  Visualize percentage of delayed flights by route
![ Visualize percentage of delayed flights by route](/static/images/flights_by_route.png)

### Visualize delayed flights by airline
![Visualize delayed flights by airline](/static/images/flights_by_airline.png)

### Visualize percentage of delayed flights per hour of the day
![Visualize percentage of delayed flights per hour of the day](/static/images/flights_per_hour.png)

### Visualize percentage of delayed flights per route on a map
![Visualize percentage of delayed flights per route on a map](/static/images/flights_by_route_map.png)


## Usage

### Command-Line Interface (`main.py`)

The `main.py` script provides a command-line interface to interact with flight data. 

#### Available Commands

1. **Show Flight by ID**
   - Prompts for a flight ID and displays the flight details.

2. **Show Flights by Date**
   - Prompts for a date in `DD/MM/YYYY` format and displays flights for that date.

3. **Delayed Flights by Airline**
   - Prompts for an airline name and displays delayed flights for that airline.

4. **Delayed Flights by Origin Airport**
   - Prompts for an origin airport IATA code and displays delayed flights for that airport.

5. **Visualize Delayed Flights by Airline**
   - Generates a visualization of delayed flights grouped by airline.

6. **Visualize Percentage of Delayed Flights per Hour of the Day**
   - Generates a visualization of the percentage of delayed flights per hour for a specified date.

7. **Visualize Percentage of Delayed Flights by Route**
   - Generates a heatmap of the percentage of delayed flights between airports.

8. **Visualize Percentage of Delayed Flights per Route on a Map**
   - Generates a map showing the percentage of delayed flights for each route.

9. **Exit**
   - Exits the program.

#### How to Use

1. Run the script:

   ```bash
   python3 main.py
   ```

2. Follow the on-screen menu to select an option and enter the required inputs.

### Visualization (`visualization.py`)

The `visualization.py` script provides various functions to generate visualizations of flight data. 

#### Functions

1. **Visualize Delayed Flights per Airline**
   - Creates a bar chart showing the number of delayed flights for each airline.

2. **Plot Delayed Flights per Hour**
   - Creates a bar chart showing the percentage of delayed flights per hour of the day for a given date.

3. **Plot Delayed Flights Heatmap**
   - Creates a heatmap showing the percentage of delayed flights for each route.

4. **Plot Delayed Flights Map**
   - Creates an interactive map showing the percentage of delayed flights between airports, using Folium.


### Backend API (`api.py`)

The Flask API provides endpoints to fetch flight data. 
The available endpoints are:
use this `http://127.0.0.1:5000`

- `GET /flight/<int:flight_id>`: Retrieve flight details by ID.
- `GET /flights/date`: Retrieve flights by date.
- `GET /delayed/airline/<string:airline_name>`: Retrieve delayed flights by airline.
- `GET /delayed/airport/<string:airport_code>`: Retrieve delayed flights by airport.
- `GET /delayed/airlines`: Retrieve all delayed flights grouped by airline.
- `GET /delayed/hour`: Retrieve delayed flights per hour.
- `GET /heatmap`: Retrieve flight delays heatmap.
- `GET /average/routes`: Retrieve average delays per route.
- `GET /route-map`: Retrieve delayed flights per route map.

### `data.py` - FlightData Class

The `FlightData` class provides methods for querying flight data from the database. Key methods include:

- `get_flight_by_id(flight_id)`: Retrieve flight details by ID.
- `get_flights_by_date(day, month, year)`: Retrieve flights for a specific date.
- `get_delayed_flights_by_airline(airline_name)`: Retrieve delayed flights for a specific airline.
- `get_delayed_flights_by_airport(airport_code)`: Retrieve delayed flights for a specific airport.
- `get_delayed_flights_per_hour(day, month, year)`: Retrieve delayed flights grouped by hour for a specific date.
- `get_flight_delays_heatmap()`: Retrieve a heatmap of flight delays between airports.
- `get_delayed_flights_average_per_route()`: Retrieve average delay percentages per route.
- `get_delayed_flights_per_route_map(day, month, year)`: Retrieve delayed flights per route with percentage of delays for a specific date.
- `get_airport_coordinates()`: Retrieve coordinates for all airports.

## Contribution

Feel free to contribute by creating issues, submitting pull requests, or improving the documentation. For more details, refer to the contributing guidelines in the repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions, please reach out to [ranavarsha710@gmail.com](mailto:ranavarsha710@gmail.com).
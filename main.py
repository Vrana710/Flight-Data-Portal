import visualization
import data
from datetime import datetime

SQLITE_URI = 'sqlite:///data/flights.sqlite3'
IATA_LENGTH = 3

def delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name and runs the query
    using the data object method 'get_delayed_flights_by_airline'.
    Displays the results.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code and
    validates the input. Runs the query using 'get_delayed_flights_by_airport'.
    Displays the results.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    while True:
        airport_input = input("Enter origin airport IATA code: ")
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            results = data_manager.get_delayed_flights_by_airport(airport_input)
            print_results(results)
            break
        else:
            print(f"Invalid IATA code. It should be {IATA_LENGTH} letters long.")


def flight_by_id(data_manager):
    """
    Asks the user for a flight ID, validates input, and retrieves
    flight details using 'get_flight_by_id'. Displays the results.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    while True:
        try:
            id_input = int(input("Enter flight ID: "))
            results = data_manager.get_flight_by_id(id_input)
            print_results(results)
            break
        except ValueError:
            print("Invalid input. Please enter a numeric flight ID.")


def flights_by_date(data_manager):
    """
    Asks the user for a date in DD/MM/YYYY format and retrieves
    flights on that date using 'get_flights_by_date'. Displays results.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    while True:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
            day, month, year = date.day, date.month, date.year

            results = data_manager.get_flights_by_date(day, month, year)

            if results:
                print_results(results)
            else:
                print("No results found for the given date.")
            break

        except ValueError:
            print("Invalid date format. Please enter date in DD/MM/YYYY format.")


def print_results(results):
    """
    Prints the flight results. Each result should contain the columns:
    FLIGHT_ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.

    :param results: List of flight results to print.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        try:
            delay_str = result.get('DELAY', '')
            delay = int(delay_str) if delay_str else 0
            origin = result.get('ORIGIN_AIRPORT', 'Unknown')
            dest = result.get('DESTINATION_AIRPORT', 'Unknown')
            airline = result.get('AIRLINE', 'Unknown')
            flight_id = result.get('FLIGHT_ID', 'Unknown')

            if delay >= 0:
                print(f"{flight_id}. {origin} -> {dest} by {airline}", 
                      f"Delay: {delay} Minutes")
            else:
                print(f"{flight_id}. {origin} -> {dest} by {airline}")

        except (ValueError, KeyError) as e:
            print(f"Error showing results: {e}")


def show_menu_and_get_input():
    """
    Displays the menu and prompts the user to select an option.

    :return: The function corresponding to the selected menu option.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    while True:
        try:
            choice = int(input("Select an option: "))
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

FUNCTIONS = {
    1: (flight_by_id, "Show flight by ID"),
    2: (flights_by_date, "Show flights by date"),
    3: (delayed_flights_by_airline, "Delayed flights by airline"),
    4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
    5: (visualization.visualize_delayed_flights_per_airline, 
        "Visualize delayed flights by airline"),
    6: (visualization.plot_delayed_flights_per_hour, 
        "Visualize percentage of delayed flights per hour of the day"),
    7: (visualization.plot_delayed_flights_heatmap, 
        "Visualize percentage of delayed flights by route"),
    8: (visualization.plot_delayed_flights_map, 
        "Visualize percentage of delayed flights per route on a map"),
    9: (quit, "Exit")
}


def main():
    """
    Main function to run the menu-driven program.
    """
    data_manager = data.FlightData(SQLITE_URI)

    while True:
        choice_func = show_menu_and_get_input()
        if choice_func == quit:
            print("Exiting program.")
            break
        if choice_func == visualization.plot_delayed_flights_per_hour:
            while True:
                try:
                    date_input = input("Enter date in DD/MM/YYYY format: ")
                    date = datetime.strptime(date_input, '%d/%m/%Y')
                    choice_func(data_manager, date)
                    break
                except ValueError:
                    print("Invalid date format. Please use DD/MM/YYYY.")
        elif choice_func == visualization.plot_delayed_flights_map:
            while True:
                try:
                    date_input = input("Enter date in DD/MM/YYYY format: ")
                    date = datetime.strptime(date_input, '%d/%m/%Y')
                    day, month, year = date.day, date.month, date.year
                    choice_func(data_manager, day, month, year)
                    #choice_func(data_manager, date)
                    break
                except ValueError:
                    print("Invalid date format. Please use DD/MM/YYYY.")            
        else:
            choice_func(data_manager)


if __name__ == "__main__":
    main()

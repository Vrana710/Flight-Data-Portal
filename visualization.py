import folium
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from folium import plugins
from datetime import datetime
from data import FlightData


def visualize_delayed_flights_per_airline(data_manager):
    """
    Visualize the number of delayed flights per airline.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    results = data_manager.get_all_delayed_flights_grouped_by_airline()

    if not results:
        print("No results found.")
        return

    airlines = [result['AIRLINE'] for result in results]
    delay_counts = [int(result['delay_count']) for result in results]  # Ensure delay_count is an integer

    plt.figure(figsize=(10, 6))
    plt.bar(airlines, delay_counts)  # delay_counts now a list of integers
    plt.xlabel('Airline')
    plt.ylabel('Number of Delayed Flights')
    plt.title('Number of Delayed Flights per Airline')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def plot_delayed_flights_per_hour(data_manager, date):
    """
    Plot the percentage of delayed flights per hour of the day for a specific date.

    :param data_manager: Instance of FlightData to fetch flight data.
    :param date: Date for which to plot the data (datetime object).
    """
    day, month, year = date.day, date.month, date.year
    results = data_manager.get_delayed_flights_per_hour(day, month, year)

    # Extract hour, delayed counts, and total counts, ensure hours are integers
    hours = [int(result['hour']) for result in results]  
    delayed_counts = [int(result['delayed_count']) for result in results]
    total_counts = [int(result['total_count']) for result in results]

    # Define all hours of the day (from 00 to 23) as integers for plotting
    all_hours = list(range(24))

    # Calculate percentage of delayed flights for each hour
    percentages = []
    for hour in all_hours:
        if hour in hours:
            idx = hours.index(hour)
            delayed_count = delayed_counts[idx]
            total_count = total_counts[idx]
            percentage = (delayed_count / total_count * 100) if total_count > 0 else 0
        else:
            percentage = 0
        percentages.append(percentage)

    # Plot the results using numeric hours
    plt.figure(figsize=(12, 6))

    # Set color based on percentage
    colors = sns.color_palette("YlGnBu", as_cmap=True)(plt.Normalize(0, 100)(percentages))
    
    plt.bar(all_hours, percentages, color=colors)

    # Set integer hours for the x-ticks, but display formatted strings
    plt.xticks(ticks=all_hours, labels=[f"{hour:02d}" for hour in all_hours], rotation=45)

    plt.xlabel('Hour of the Day')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title(f'Percentage of Delayed Flights per Hour on {date.strftime("%d/%m/%Y")}')
    plt.ylim(0, 100)  # Limit y-axis to 0-100%
    plt.tight_layout()
    plt.show()


def plot_delayed_flights_heatmap(data_manager):
    """
    Plot a heatmap showing the percentage of delayed flights for each route.

    :param data_manager: Instance of FlightData to fetch flight data.
    """
    data = data_manager.get_flight_delays_heatmap()

    pivot_table = data.pivot(index="origin_airport", columns="destination_airport", values="percentage")

    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot_table, cmap="coolwarm", fmt=".1f", linewidths=.5, cbar=True, annot=False)
    plt.title("Percentage of Delayed Flights (Heatmap of Routes)")
    plt.xlabel("Destination Airport")
    plt.ylabel("Origin Airport")
    plt.show()


def get_color_for_percentage(percentage):
    """
    Return a color based on the percentage of delay.

    :param percentage: Delay percentage.
    :return: Color code as a string.
    """
    if percentage < 20:
        return '#00FF00'  # Green for less delay
    elif percentage < 40:
        return '#FFFF00'  # Yellow for moderate delay
    elif percentage < 60:
        return '#FFA500'  # Orange for significant delay
    else:
        return '#FF0000'  # Red for severe delay


def plot_delayed_flights_map(data_manager, day, month, year):
    flights = data_manager.get_delayed_flights_per_route_map(day, month, year)

    if not flights:
        print("No flight data available.")
        return

    df = pd.DataFrame(flights)

    if 'origin_airport' not in df.columns or 'destination_airport' not in df.columns or 'percentage' not in df.columns:
        print("Required columns are missing in the data.")
        return

    airport_locations = data_manager.get_airport_coordinates()
    if not airport_locations:
        print("No airport coordinates data available.")
        return

    map_center = [37.0902, -95.7129]  # Center of the US
    map = folium.Map(location=map_center, zoom_start=4)

    for airport, coords in airport_locations.items():
        if coords and all(isinstance(coord, (int, float)) for coord in coords):
            folium.Marker(
                location=[coords[0], coords[1]],
                popup=airport
            ).add_to(map)
        else:
            print(f"Invalid coordinates for airport {airport}: {coords}")

    for _, row in df.iterrows():
        origin = row['origin_airport']
        destination = row['destination_airport']
        percentage = float(row['percentage'])  # Ensure percentage is a float

        origin_coords = airport_locations.get(origin)
        dest_coords = airport_locations.get(destination)
        if (origin_coords and dest_coords and 
            all(isinstance(coord, (int, float)) for coord in origin_coords) and 
            all(isinstance(coord, (int, float)) for coord in dest_coords)):
            folium.PolyLine(
                locations=[origin_coords, dest_coords],
                color=get_color_for_percentage(percentage),
                weight=percentage / 10 + 1
            ).add_to(map)
        else:
            print(f"Invalid coordinates for route {origin} -> {destination}: {origin_coords}, {dest_coords}")

    map_file = 'delayed_flights_map.html'
    map.save(map_file)
    print(f"Map has been saved to {map_file}.")


def main():
    """
    Main function to run the visualizations.
    """
    db_uri = 'sqlite:///data/flights.sqlite3'
    data_manager = FlightData(db_uri)

    # Example user input for the date
    user_input_date = input("Enter date in DD/MM/YYYY format: ")
    try:
        date = datetime.strptime(user_input_date, '%d/%m/%Y')
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return

    visualize_delayed_flights_per_airline(data_manager)
    plot_delayed_flights_per_hour(data_manager, date)
    plot_delayed_flights_heatmap(data_manager)
    plot_delayed_flights_map(data_manager)


if __name__ == "__main__":
    main()

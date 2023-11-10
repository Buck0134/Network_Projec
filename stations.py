import networkx as nx
import pandas as pd

class Station:
    def __init__(self, name):
        self.name = name
        self.outgoing_edges = 0
        self.incoming_edges = 0
        self.connected_stations = set()
        self.net_flow = 0
        self.latitude = 0
        self.longitude = 0
        
    def __str__(self):
        return (f"Station: {self.name}\n"
                f"Outgoing Edges: {self.outgoing_edges}\n"
                f"Incoming Edges: {self.incoming_edges}\n"
                f"Connected Stations: {len(self.connected_stations)}\n"
                f"Net Flow: {self.net_flow}"
                f"latitude: {self.latitude}\n"
                f"longitude: {self.longitude}\n")

def create_station_array(edge_data):
    G = nx.from_pandas_edgelist(edge_data, 'start_station_name', 'end_station_name', create_using=nx.DiGraph())
    
    # Create a dictionary to store Station objects by name
    stations = {}
    
    # Helper function to handle or update station information
    def handle_station(station_name, lat, lng, is_start_station):
        if station_name not in stations:
            station = Station(station_name)
            station.latitude = lat
            station.longitude = lng
            stations[station_name] = station
        else:
            station = stations[station_name]
        
        if is_start_station:
            station.outgoing_edges += 1
        else:
            station.incoming_edges += 1
    
    # Iterate over each edge data and update or create stations
    for _, row in edge_data.iterrows():
        handle_station(row['start_station_name'], row['start_lat'], row['start_lng'], True)
        handle_station(row['end_station_name'], row['end_lat'], row['end_lng'], False)
    
    # Now that we have updated edge counts, we can calculate other properties for each station
    for station in stations.values():
        station.connected_stations = set(G.neighbors(station.name))
        station.net_flow = station.outgoing_edges - station.incoming_edges

    # Convert the dictionary values (Station objects) to a list and sort by outgoing edges
    sorted_stations = sorted(stations.values(), key=lambda x: x.outgoing_edges, reverse=True)

    return sorted_stations


import folium

def create_map(stations, attribute, title):
    """
    Creates a map visualization with marker sizes based on a given attribute of stations.
    
    Parameters:
    - stations: List of Station objects
    - attribute: Attribute of Station (e.g., 'outgoing_edges', 'incoming_edges', 'net_flow')
    - title: Title of the map
    """
    # Find min and max of the attribute
    min_val = min([getattr(station, attribute) for station in stations])
    max_val = max([getattr(station, attribute) for station in stations])

    # Create base map
    m = folium.Map(location=[data['start_lat'].mean(), data['start_lng'].mean()], zoom_start=13)

    # Loop through stations and add them to the map
    for station in stations:
        value = getattr(station, attribute)
        
        # Normalize the attribute value to fall in the range [10, 50] for marker sizes
        normalized_size = 10 + 40 * (value - min_val) / (max_val - min_val)

        folium.CircleMarker(
            location=(station.latitude, station.longitude), # lat, lng
            radius=normalized_size,
            fill=True,
            fill_color='blue',
            color='blue',
            fill_opacity=0.6,
            tooltip=f"{station.name}: {value}"
        ).add_to(m)
    
    m.save(f"./Graphs/{title}.html")

# Usage:



# Usage
# Read the processed data
data = pd.read_csv('Processed_Data.csv')
sorted_stations_list = create_station_array(data)

create_map(sorted_stations_list, 'outgoing_edges', 'Outgoing Edges Map')
create_map(sorted_stations_list, 'incoming_edges', 'Incoming Edges Map')
create_map(sorted_stations_list, 'net_flow', 'Net Flow Map')

for station in sorted_stations_list:
    print(station)
    print("----------------------------")

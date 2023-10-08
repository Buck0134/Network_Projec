import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# reading the csv data
data = pd.read_csv('Data/JC-202201-citibike-tripdata.csv')

# for index, row in data.iterrows():
#     if index < 10:
#         print(row)

# flitering only wanted data

# Display the attributes
table_attributes = list(data.columns)
mandatory_attributes = ['start_station_name', 'start_station_id', 'end_station_name', 'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng']

# Ensure mandatory attributes are present
for attribute in mandatory_attributes:
    if attribute not in table_attributes:
        raise ValueError(f"Mandatory attribute '{attribute}' not found in data.")

for index, attribute in enumerate(table_attributes):
    if attribute in mandatory_attributes:
        print(f"{index}. {attribute} (Mandatory)")
    else:
        print(f"{index}. {attribute}")

print("\nPlease select the corresponding attributes by entering their listed numbers, separated by commas.")
print("Mandatory attributes will be included regardless of your selection.")
print("Enter 100 to only use the mandatory attributes.")
print("Enter 101 for default selection (all attributes).")

# Get input from the user
selection = input("Your selection: ")

# Process the input
if selection == "100":
    selected_attributes = mandatory_attributes
elif selection == "101":
    selected_attributes = table_attributes
else:
    indices = [int(idx.strip()) for idx in selection.split(",") if idx.strip().isdigit()]
    selected_attributes = [table_attributes[idx] for idx in indices if 0 <= idx < len(table_attributes)]
    # Adding mandatory attributes
    for attribute in mandatory_attributes:
        if attribute not in selected_attributes:
            selected_attributes.append(attribute)

print("\nYou've selected:")
for attribute in selected_attributes:
    print(attribute)

print("Processing Data ....")

# Filter the DataFrame
filtered_data = data[selected_attributes]

# Handle 'member_casual' and 'rideable_type' options
if 'member_casual' in selected_attributes:
    unique_members = filtered_data['member_casual'].unique()
    print("Available membership types:")
    for index, member in enumerate(unique_members):
        print(f"{index}. {member}")
    selected_members = input("Select membership types by index (comma-separated): ").split(',')
    selected_members = [unique_members[int(index)] for index in selected_members]
    filtered_data = filtered_data[filtered_data['member_casual'].isin(selected_members)]

if 'rideable_type' in selected_attributes:
    unique_rideables = filtered_data['rideable_type'].unique()
    print("Available rideable types:")
    for index, rideable in enumerate(unique_rideables):
        print(f"{index}. {rideable}")
    selected_rideables = input("Select rideable types by index (comma-separated): ").split(',')
    selected_rideables = [unique_rideables[int(index)] for index in selected_rideables]
    filtered_data = filtered_data[filtered_data['rideable_type'].isin(selected_rideables)]



# process locational data
start_position_dict = {row['start_station_name']: (row['start_lng'], row['start_lat']) for _, row in filtered_data.iterrows()}
end_position_dict = {row['end_station_name']: (row['end_lng'], row['end_lat']) for _, row in filtered_data.iterrows()}
position_dict = {**start_position_dict, **end_position_dict}


# make sure data are all vaild
data_filterd_cleaned = filtered_data.dropna()
data_filterd_cleaned.to_csv('Processed_Data.csv', index=False)
print("Data saved on Processed_Data.csv")

print("Drawing Data Graph ....")

import folium

# Create a base map centered around the mean latitude and longitude of your data
m = folium.Map(location=[data_filterd_cleaned['start_lat'].mean(), data['start_lng'].mean()], zoom_start=13)

# Add markers for each start station
for _, row in data_filterd_cleaned.iterrows():
    folium.Marker(
        [row['start_lat'], row['start_lng']], 
        tooltip=row['start_station_name'],
        # icon=folium.Icon(color='blue', icon='cloud')  # blue marker for start stations
    ).add_to(m)

    folium.Marker(
        [row['end_lat'], row['end_lng']], 
        tooltip=row['end_station_name'],
        # icon=folium.Icon(color='red')  # red marker for end stations
    ).add_to(m)

    # Add a line connecting start and end stations
    folium.PolyLine([(row['start_lat'], row['start_lng']), 
                     (row['end_lat'], row['end_lng'])], 
                     color="blue", weight=2.5, opacity=1).add_to(m)

m.save('stations_map.html')


# G = nx.from_pandas_edgelist(filtered_data, 'start_station_name', 'end_station_name', create_using=nx.DiGraph())

# # Embeding geo data into gexf# Embedding the start station geo-coordinates
# for _, row in data.iterrows():
#     G.nodes[row['start_station_name']]['latitude'] = row['start_lat']
#     G.nodes[row['start_station_name']]['longitude'] = row['start_lng']
    
#     # Similarly for end station
#     G.nodes[row['end_station_name']]['latitude'] = row['end_lat']
#     G.nodes[row['end_station_name']]['longitude'] = row['end_lng']

# nx.write_gexf(G, "output_graph_with_geo_data.gexf")

# Masaking graph
# Geological graph

# plt.figure(figsize=(20, 20))

# nx.draw(G, pos=position_dict, node_size=50, node_color='blue', edge_color='gray', with_labels=True, font_size=6)

# plt.title('CitiBike Stations Geospatial Layout')
# plt.show()



# normal graph
# Save to .gexf format (for Gephi)
# nx.write_gexf(G, "output_graph.gexf")

# Visualize the graph
# plt.figure(figsize=(12, 12)) 
# pos = nx.spring_layout(G) 
# nx.draw_networkx_nodes(G, pos)
# nx.draw_networkx_edges(G, pos)
# nx.draw_networkx_labels(G, pos, font_size=8)
# plt.title('Network Visualization')
# plt.show()




from ipyleaflet import Map, Marker
import ipywidgets as widgets
from IPython.display import HTML, display

# Define latitude and longitude coordinates for cities
coordinates = [(30.4766, 76.5905), (34.0522, -118.2437), (51.5074, -0.1278), (-33.8688, 151.2093)]
cities = ['Rajpura', 'Los Angeles', 'London', 'Sydney']

# Create a map centered around the first city
mymap = Map(center=coordinates[0], zoom=5)

# Add markers for each city
for coord, city in zip(coordinates, cities):
    marker = Marker(location=coord, title=city)
    mymap.add_layer(marker)

# Convert the map to HTML code
html_code = display(mymap, display_id='map')

# Save the HTML code to a variable or use it as needed
html_string = html_code.data

# Print or use the HTML string as needed
print(html_string)
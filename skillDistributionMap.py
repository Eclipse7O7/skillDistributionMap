import pandas as pd

import folium

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter

 
# Define colours for skills
# Colour options:
# {'blue', 'lightblue', 'white', 'darkblue', 'darkgreen', 'darkpurple', 'gray', 'orange',
#  'beige', 'lightred', 'green', 'red', 'purple', 'pink', 'lightgray', 'black', 'darkred',
#  'cadetblue', 'lightgreen'}
skill_colours = {
   'Welder': 'red',
   'CNC Machinist': 'blue',
   'General Operative': 'orange',
   'Leadership': 'purple',
   'Laser Cut & Punch': 'yellow',
   'Press-Brake': 'green'
}




# Load CSV file

#df = pd.read_csv("Skills Distribution.csv")
df = pd.read_csv("workData.csv")
x = df.iterrows()

# Set up geocoder to turn postcodes into lat/long

geolocator = Nominatim(user_agent="norfolk_skill_map")

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Create a map centered on Norfolk, UK

m = folium.Map(location=[52.63, 1.29], zoom_start=9)

# Creatuing a layer controller in top right of map

layerControl = folium.LayerControl(position='topright', collapsed=True)

# Creating a toggleable layer for Lotus Locations

fg = folium.FeatureGroup(name="Group Lotus Locations", show=True)
hethelMarker = folium.Marker(location=(52.5607858,1.1772759), popup="Lotus Hethel", icon=folium.Icon(color='red', icon='none'))
hethelMarker.add_to(fg)
lasMarker = folium.Marker(location=(52.6664829,1.2789882), popup="LAS", icon=folium.Icon(color='green', icon='none'))
lasMarker.add_to(fg)
fg.add_to(m)

# Creating a toggleable layer for each skill type

fg2 = folium.FeatureGroup(name="Skills: Welder", show=True)
fg3 = folium.FeatureGroup(name="Skills: CNC Machinist", show=True)
fg4 = folium.FeatureGroup(name="Skills: General Operative", show=True)
fg5 = folium.FeatureGroup(name="Skills: Leadership", show=True)
fg6 = folium.FeatureGroup(name="Skills: Laser Cut & Punch", show=True)
fg7 = folium.FeatureGroup(name="Skills: Press-Brake", show=True)


for i in x:
   id = str(i[1][0])
   skill = str(i[1][1]).removeprefix(" ").removesuffix(" ")
   postcode = str(i[1][2]).removeprefix(" ").removesuffix(" ")
   
   try:
      if not pd.isna(postcode):
         location = geocode(postcode + ", UK")
         print("long and lat:",location.latitude, location.longitude)
         print(location)
         if location:
               
            # "Circle" Marker icon
            marker = folium.Circle(radius=800, fill_color=skill_colours.get(skill), fill_opacity=0.4, color=skill_colours.get(skill), weight=1, location=[float(location.latitude), float(location.longitude)])
            #marker.add_child(folium.Popup(f"{postcode}"))
            extendedPostcodeList = geocode(postcode).address.split(",")
            shorterExtendedPostcode = str(extendedPostcodeList[0] + " " + extendedPostcodeList[1]) if extendedPostcodeList else postcode
            marker.add_child(folium.Popup(f"{shorterExtendedPostcode}"))
            # Adding the marker to the appropriate group based on skill
            if skill == 'Welder':
               marker.add_to(fg2)
            elif skill == 'CNC Machinist':
               marker.add_to(fg3)
            elif skill == 'General Operative':
               marker.add_to(fg4)
            elif skill == 'Leadership':
               marker.add_to(fg5)
            elif skill == 'Laser Cut & Punch':
               marker.add_to(fg6)
            elif skill == 'Press-Brake':
               marker.add_to(fg7)
            else:
               marker.add_to(m)
            
         else:
               print(f"Could not geocode postcode: {postcode}")

   except Exception as e:
      print(f"Error geocoding postcode {postcode}: {e}")

# Adding all groups to the map

fg2.add_to(m)
fg3.add_to(m)
fg4.add_to(m)
fg5.add_to(m)
fg6.add_to(m)
fg7.add_to(m)

# Adding the layer control to the map

layerControl.add_to(m)

# Save the map to an HTML file

m.save("skillHeatMap.html")

# Open automatically in default browser

import webbrowser
webbrowser.open("skillHeatMap.html")


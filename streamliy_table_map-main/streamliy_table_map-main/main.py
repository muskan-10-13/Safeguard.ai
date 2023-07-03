import streamlit as st
import requests
import json
import pydeck as pdk

def create_map(points):
    layers = []
    for point in points:
        latitude = float(point['latitude'])
        longitude = float(point['longitude'])
        marker_layer = pdk.Layer(
            'ScatterplotLayer',
            data=[{'position': [longitude, latitude]}],
            get_position='position',
            get_radius=1000,
            get_fill_color=[255, 0, 0,0.44*255],
            radius_min_pixels=1,
            radius_max_pixels=10,
        )
        layers.append(marker_layer)

    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=2)
    map = pdk.Deck(layers=layers, initial_view_state=view_state)

    return map.to_html()

def main():
    st.title('Map Example')

    response = requests.get('http://ec2-43-204-130-153.ap-south-1.compute.amazonaws.com:5000/data/all')
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        st.error('Failed to fetch data')
        return None

    if data:
        map_html = create_map(data)
        st.components.v1.html(map_html, height=600)

if __name__ == '__main__':
    main()

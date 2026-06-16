import streamlit as st
import cohere
from dotenv import load_dotenv
import os
import json
import openrouteservice

load_dotenv()
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
ors = openrouteservice.Client(key=os.getenv("ORS_API_KEY"))

def get_coordinates(place):
    result = ors.pelias_search(text=place)
    coords = result['features'][0]['geometry']['coordinates']
    return coords

def get_route_info(origin_coords, dest_coords):
    route = ors.directions(
        coordinates=[origin_coords, dest_coords],
        profile='driving-car',
        format='json'
    )
    summary = route['routes'][0]['summary']
    miles = round(summary['distance'] / 1609.34)
    hours = round(summary['duration'] / 3600, 1)
    return miles, hours

st.title("Road Trip OS")

name = st.text_input("What's your name?")
origin = st.text_input("Where are you starting from?")
destination = st.text_input("Where are you going?")
days = st.number_input("How many days?", min_value=1, max_value=30)
mode = st.selectbox("How are you getting there?", ["Driving", "Flying", "Train", "Bus"])

if name and origin and destination:
    if st.button("Plan My Trip"):
        with st.spinner("Planning your trip..."):
            origin_coords = get_coordinates(origin)
            dest_coords = get_coordinates(destination)
            miles, hours = get_route_info(origin_coords, dest_coords)

            prompt = (
                f"You are a travel planning API. Return ONLY valid JSON, no explanation, no extra text.\n\n"
                f"Plan a {days} day trip for {name} from {origin} to {destination} by {mode}.\n"
                f"The total driving distance is {miles} miles and approximately {hours} hours of driving.\n"
                f"Use these real numbers when planning drive times for each day.\n\n"
                f"Return this exact structure:\n"
                f'{{"days": [{{"day": 1, "from": "city", "to": "city", "drive_hours": 4, "stops": ["stop1", "stop2"], "eat": "restaurant recommendation", "sleep": "hotel or campsite", "est_cost": 150}}], "total_miles": {miles}, "total_cost": 800}}'
            )
            response = co.chat(
                model="command-r-plus-08-2024",
                messages=[{"role": "user", "content": prompt}]
            )

            try:
                data = json.loads(response.message.content[0].text)
                st.subheader("Your Itinerary")
                for day in data["days"]:
                    st.markdown(f"### Day {day['day']}: {day['from']} → {day['to']}")
                    st.write(f"🚗 Drive time: {day['drive_hours']} hours")
                    st.write(f"📍 Stops: {', '.join(day['stops'])}")
                    st.write(f"🍔 Eat: {day['eat']}")
                    st.write(f"🛏️ Sleep: {day['sleep']}")
                    st.write(f"💵 Est. cost: ${day['est_cost']}")
                    st.divider()
                st.success(f"Total trip: {data['total_miles']} miles — ${data['total_cost']} estimated")
            except Exception as e:
                st.error(f"Error: {e}")
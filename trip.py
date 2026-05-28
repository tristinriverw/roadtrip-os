import streamlit as st
import cohere
from dotenv import load_dotenv
import os
import json

load_dotenv()
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

st.title("Road Trip OS")

name = st.text_input("What's your name?")
origin = st.text_input("Where are you starting from?")
destination = st.text_input("Where are you going?")
days = st.number_input("How many days?", min_value=1, max_value=30)
mode = st.selectbox("How are you getting there?", ["Driving", "Flying", "Train", "Bus"])

if name and origin and destination:
    if st.button("Plan My Trip"):
        with st.spinner("Planning your trip..."):
            prompt = f"""
You are a travel planning API. Return ONLY valid JSON, no explanation, no extra text.

Plan a {days} day trip for {name} from {origin} to {destination} by {mode}.

Return this exact structure:
{{
  "days": [
    {{
      "day": 1,
      "from": "city",
      "to": "city",
      "drive_hours": 4,
      "stops": ["stop1", "stop2"],
      "eat": "restaurant recommendation",
      "sleep": "hotel or campsite",
      "est_cost": 150
    }}
  ],
  "total_miles": 1200,
  "total_cost": 800
}}
"""
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
            except:
                st.error("AI returned unexpected format, try again")
import streamlit as st

st.title("Roadtrip OS")
st.write("A simple adventure trip planner prototype.")

start = st.text_input("Starting location", "Quad Cities, IL")
destination = st.text_input("Destination", "Yellowstone National Park")
days = st.number_input("Trip length in days", min_value=1, max_value=30, value=7)
miles = st.number_input("Estimated total miles", min_value=1, value=2200)
mpg = st.number_input("Vehicle MPG", min_value=1, value=25)
gas_price = st.number_input("Gas price per gallon", min_value=1.0, value=3.50)
budget = st.number_input("Total budget", min_value=0, value=1000)

camping = st.checkbox("Mostly camping?", value=True)

if st.button("Generate Plan"):
    gallons_needed = miles / mpg
    fuel_cost = gallons_needed * gas_price
    daily_budget = budget / days
    miles_per_day = miles / days

    st.subheader("Trip Summary")
    st.write(f"Trip: {start} → {destination}")
    st.write(f"Estimated fuel cost: ${fuel_cost:.2f}")
    st.write(f"Average miles per day: {miles_per_day:.0f}")
    st.write(f"Daily budget: ${daily_budget:.2f}")

    st.subheader("Basic Plan")
    if camping:
        st.write("Prioritize campsites, dispersed camping, showers, food storage, and weather checks.")
    else:
        st.write("Prioritize hotels, parking, food stops, and daily driving comfort.")

    st.subheader("Starter Packing List")
    st.write("- Tent / sleeping setup")
    st.write("- Cooler and food")
    st.write("- Water jug")
    st.write("- Power bank")
    st.write("- Basic tools")
    st.write("- Clothes for weather changes")

st.subheader("Day-by-Day Rough Itinerary")

for day in range(1, days + 1):
    st.write(f"**Day {day}**")
    st.write(f"- Drive about {miles_per_day:.0f} miles")
    st.write("- Find food, fuel, and a rest stop")
    if camping:
        st.write("- Look for a campsite or dispersed camping area")
    else:
        st.write("- Look for a hotel/motel near the route")
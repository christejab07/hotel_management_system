import requests
import pandas as pd

try:
    # Send a GET request
    get_rooms = requests.get("http://127.0.0.1:8000/api/rooms/")
    get_rooms.raise_for_status()
    rooms = get_rooms.json()
    print(rooms)
    get_reservations = requests.get("http://127.0.0.1:8000/api/reservations/")
    get_reservations.raise_for_status()
    reservations = get_reservations.json()
    print(reservations)

    rdf = pd.DataFrame(rooms)
    cdf = pd.DataFrame(reservations)

    inner_merged_df = pd.merge(rdf, cdf, on="id", how="inner")
    print(inner_merged_df.head())

except requests.exceptions.RequestException as e:
    print(f"Error: fetchng data {e}")

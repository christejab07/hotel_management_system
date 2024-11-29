import pandas as pd
import random
import requests


# Step 1: Generate dataset
def generate_dataset(rows=20):
    data = {
        "room_number": [f"Room-{num}" for num in random.sample(range(1, 1000), rows)],
        "room_type": [
            random.choice(["Single", "Double", "Suite", "Deluxe"]) for _ in range(rows)
        ],
        "price": [round(random.uniform(50, 500), 2) for _ in range(rows)],
        "capacity": [random.randint(1, 4) for _ in range(rows)],
        "is_available": True,
    }
    return pd.DataFrame(data)


def post_data_to_api(df):
    # Define the FastAPI endpoint for posting data
    api_url = "http://127.0.0.1:8000/api/rooms/"

    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        # Convert the row to a dictionary
        room_data = row.to_dict()

        # Post the data to the FastAPI `/rooms/` endpoint
        try:
            response = requests.post(api_url, json=room_data)
            response.raise_for_status()  # Raise an error for unsuccessful requests
            print(f"Successfully uploaded room: {room_data['room_number']}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to upload room: {room_data['room_number']}\nError: {e}")
            continue  # Skip to the next iteration if there is an error


# Step 2: Describe the dataset
def describe_dataset(df):
    return df.describe(include="all")


# Step 3: Find and replace null values
def handle_null_values(df):
    # Simulate some null values for demonstration purposes
    df.loc[random.sample(range(len(df)), 10), "price"] = (
        None  # Add 30 null values in "price"
    )

    print("\nMissing Values Before Handling:")
    print(df.isnull().sum())

    # Replace null values with appropriate defaults
    df["price"].fillna(
        df["price"].mean(), inplace=True
    )  # Replace null prices with the mean

    print("\nMissing Values After Handling:")
    print(df.isnull().sum())
    return df


# Step 4: Perform basic data processing
def process_data(df):

    # Filter rows with `is_available == True`
    available_rooms = df[df["is_available"] == True]

    return df, available_rooms


# Step 5: Create new features
def create_features(df):
    # Feature 1: Price per person (price divided by capacity)
    df["price_per_person"] = df["price"] / df["capacity"]

    # Feature 2: Room category based on price
    df["price_category"] = pd.cut(
        df["price"], bins=[0, 100, 300, 500], labels=["Budget", "Mid-range", "Luxury"]
    )

    # Feature 3: Mark expensive rooms (price > $400)
    df["is_expensive"] = df["price"] > 400

    return df


# Main execution
if __name__ == "__main__":
    # Generate dataset
    print("Generating dataset...")
    df = generate_dataset()

    # Describe dataset
    print("\nDataset Description:")
    print(describe_dataset(df))

    # Post the data to the running FastAPI project
    print("\nPosting data to FastAPI...")
    post_data_to_api(df)
    print("\nData upload completed!")

    # Handle null values
    print("\nHandling Null Values...")
    df = handle_null_values(df)

    # Perform basic data processing
    print("\nProcessing Data...")
    df, available_rooms = process_data(df)
    print(f"\nAvailable Rooms: {len(available_rooms)}")

    # Create new features
    print("\nCreating New Features...")
    df = create_features(df)

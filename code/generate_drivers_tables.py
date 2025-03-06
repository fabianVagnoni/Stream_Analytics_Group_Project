from faker import Faker
import pandas as pd
from datetime import datetime
import random

NO_OF_DRIVERS = 100

car_companies = [
    "Toyota", "Honda", "Ford", "Chevrolet", "Tesla", 
    "BMW", "Mercedes-Benz", "Volkswagen", "Hyundai", "Nissan",
    "Audi", "Kia", "Subaru", "Mazda", "Jeep"
]

vehicle_types = ["Sedan", "SUV", "Hatchback", "Truck", "Coupe"]

email_domains = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"
]

fake = Faker('es_ES')

static = pd.DataFrame(columns=[
    'driver_id',
    'first_name',
    'last_name',
    'phone_number',
    'email',
    'license_number',
    'vehicle',
    'account_creation_date'
])


for _ in range(NO_OF_DRIVERS):

    first_name = fake.first_name()
    last_name = fake.last_name()

    # Generate individual data points
    driver_data = {
        "driver_id": f"D{random.randint(10000, 99999)}",  # e.g., "D12345"
        "first_name": first_name,  # First name only
        "last_name": last_name,  # Last name
        "phone_number": fake.phone_number(),  # e.g., "(123) 456-7890"
        "email": f"{last_name.lower()}{random.randint(1, 999)}@{random.choice(email_domains)}",  # e.g., "smith42@gmail.com"
        "license_number": fake.bothify(text="??######", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),  # e.g., "AB123456"
        "vehicle": f"{random.choice(car_companies)} {random.choice(vehicle_types)} {random.randint(2015, 2023)}",  # e.g., "Toyota Sedan 2019"
        "account_creation_date": fake.date_between(start_date="-5y", end_date="-1y")  # Date in last 5 years
    }
    
    # Append the data as a new row to the DataFrame
    static = pd.concat([static, pd.DataFrame([driver_data])], ignore_index=True)


static.to_csv("./data/driver_static.csv", index=False)


dynamic = pd.DataFrame(columns=[
    'driver_id', 
    'rating', 
    'no_of_rides', 
    'cancellation_rate', 
    'money_earned', 
    'time_driven'
])

# Use the same driver_ids from static
driver_ids = static['driver_id'].tolist()

for driver_id in driver_ids:
    # Generate dynamic data points
    no_of_rides = random.randint(50, 2500)  # Wide range for driver activity
    dynamic_data = {
        "driver_id": driver_id,
        "rating": round(random.uniform(4.0, 5.0) if random.random() < 0.9 else random.uniform(3.0, 4.0), 2),  # 90% chance of 4.0-5.0, 10% chance of 3.0-4.0
        "no_of_rides": no_of_rides,
        "cancellation_rate": round(random.uniform(0.0, 0.2) if random.random() < 0.95 else random.uniform(0.2, 0.5), 3),  # 95% chance of 0-20%, 5% chance of 20-50%
        "money_earned": round(no_of_rides * random.uniform(7, 40), 2),  # $10-$40 per ride
        "time_driven": round(no_of_rides * random.uniform(0.25, 1.0), 2)  # 15-60 minutes per ride
    }
    
    # Append to dynamic DataFrame
    dynamic = pd.concat([dynamic, pd.DataFrame([dynamic_data])], ignore_index=True)

# Save dynamic data
dynamic.to_csv("./data/driver_dynamic.csv", index=False)

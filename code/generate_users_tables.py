from faker import Faker
import pandas as pd
from datetime import datetime
import random

# Constants
NO_OF_USERS = 1000

email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com"]
spanish_cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga", "Zaragoza"]

fake = Faker('es_ES')

# --- Static DataFrame ---
user_static = pd.DataFrame(columns=[
    'user_id', 'first_name', 'last_name', 'email', 'phone_number', 
    'signup_date', 'city'
])

for _ in range(NO_OF_USERS):
    first_name = fake.first_name()
    last_name = fake.last_name()

    user_data = {
        "user_id": f"U{random.randint(10000, 99999)}",
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{last_name.lower()}{random.randint(1, 999)}@{random.choice(email_domains)}",
        "phone_number": fake.phone_number(),  # Spanish format, e.g., "+34612345678"
        "signup_date": fake.date_between(start_date="-5y", end_date="now"),
        "city": random.choice(spanish_cities)
    }
    
    user_static = pd.concat([user_static, pd.DataFrame([user_data])], ignore_index=True)

# Save static data
user_static.to_csv("./data/user_static.csv", index=False)

# --- Dynamic DataFrame ---
user_dynamic = pd.DataFrame(columns=[
    'user_id', 'rides_taken', 'money_spent', 'avg_rating_given', 
    'cancellation_rate', 'last_ride_date'
])

# Use the same user_ids from static
user_ids = user_static['user_id'].tolist()

for user_id in user_ids:
    rides_taken = random.randint(0, 1000)  # Wide range for user activity
    dynamic_data = {
        "user_id": user_id,
        "rides_taken": rides_taken,
        "money_spent": round(rides_taken * random.uniform(10, 50), 2),  # $10-$50 per ride
        "avg_rating_given": round(random.uniform(4.0, 5.0) if random.random() < 0.85 else random.uniform(2.5, 4.0), 2),  # 85% chance of 4.0-5.0
        "cancellation_rate": round(random.uniform(0.0, 0.2) if random.random() < 0.9 else random.uniform(0.2, 0.5), 3),  # 90% chance of 0-20%
        "last_ride_date": fake.date_between(start_date="-1y", end_date="today")  # Recent activity
    }
    
    user_dynamic = pd.concat([user_dynamic, pd.DataFrame([dynamic_data])], ignore_index=True)

# Save dynamic data
user_dynamic.to_csv("./data/user_dynamic.csv", index=False)

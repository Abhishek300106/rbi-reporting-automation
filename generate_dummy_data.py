import pandas as pd
import random
from faker import Faker
import os

fake = Faker("en_IN")

# Create input folder
os.makedirs("input", exist_ok=True)

# ---------------- COMMON DATA ----------------

country_currency = {
    "USA": "USD",
    "GBR": "GBP",
    "FRA": "EUR",
    "AUS": "AUD",
    "CAN": "CAD",
    "SGP": "SGD",
    "JPN": "JPY"
}

purpose_codes = [
    "P001",
    "P002",
    "P101",
    "P202",
    "P303"
]

# Generate PAN
def generate_pan():
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
    numbers = ''.join(random.choices('0123456789', k=4))
    letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return letters + numbers + letter

# Generate Aadhaar
def generate_aadhaar():
    return ''.join(random.choices('0123456789', k=12))

# Create customer pool
customers = []

for _ in range(40):
    customers.append({
        "name": fake.name(),
        "pan": generate_pan(),
        "aadhaar": generate_aadhaar()
    })

# ---------------- DCARD FILE ----------------

dcard_data = []

for i in range(100):

    cust = random.choice(customers)

    country = random.choice(list(country_currency.keys()))

    # Intentionally create some blank currency codes
    if random.randint(1, 10) == 1:
        currency = ""
    else:
        currency = country_currency[country]

    amount = random.randint(100, 5000)

    dcard_data.append({
        "Record Number": i + 1,
        "PAN No": cust["pan"],
        "Name Remitter": cust["name"],
        "Aadhar": cust["aadhaar"],
        "Beneficiary Country Code": country,
        "Remittance Date": fake.date_this_year(),
        "Purpose Code": random.choice(purpose_codes),
        "Currency Code": currency,
        "Eq.USD": amount,
        "Remarks": random.choice([
            "Normal",
            "Education",
            "Travel",
            "Medical",
            ""
        ])
    })

dcard_df = pd.DataFrame(dcard_data)

dcard_df.to_excel("input/DCARD.xlsx", index=False)

# ---------------- LRS FILE ----------------

lrs_data = []

for i in range(100):

    cust = random.choice(customers)

    country = random.choice(list(country_currency.keys()))

    # Some blank currencies
    if random.randint(1, 12) == 1:
        currency = ""
    else:
        currency = country_currency[country]

    usd_amount = random.randint(500, 10000)

    lrs_data.append({
        "Zone": random.choice(["East", "West", "North", "South"]),
        "Region": fake.city(),
        "BrCode": random.randint(1000, 9999),
        "Branch": fake.city(),
        "Sol ID": random.randint(10000, 99999),
        "Customer ID": random.randint(100000, 999999),
        "Customer name": cust["name"],
        "NRE flag": random.choice(["Y", "N"]),
        "PAN Number": cust["pan"],
        "Aadhar NO": cust["aadhaar"],
        "Operative A/C": random.randint(1000000000, 9999999999),
        "Scheme": random.choice(["SB", "CA"]),
        "Bill No": f"BILL{i+1}",
        "Bill Date": fake.date_this_year(),
        "Crncy": currency,
        "Bill Amount": usd_amount * 80,
        "Bill Amount INR": usd_amount * 83,
        "Bill Amount USD": usd_amount,
        "Other party": fake.name(),
        "Other party country code": country,
        "Purpose": random.choice(purpose_codes),
        "Purpose code description": random.choice([
            "Education",
            "Travel",
            "Medical",
            "Gift"
        ])
    })

lrs_df = pd.DataFrame(lrs_data)

lrs_df.to_excel("input/LRS.xlsx", index=False)

# ---------------- UPI FILE ----------------

upi_data = []

for i in range(100):

    cust = random.choice(customers)

    country = random.choice(list(country_currency.keys()))

    # Blank currency simulation
    if random.randint(1, 15) == 1:
        currency = ""
    else:
        currency = country_currency[country]

    usd_amount = random.randint(10, 1000)

    upi_data.append({
        "pan remitter": cust["pan"],
        "name remitter": cust["name"],
        "beneficiary_country_code": country,
        "date_remittance": fake.date_this_year(),
        "purpose": random.choice(purpose_codes),
        "currency code": currency,
        "usd amount": usd_amount,
        "remarks": random.choice([
            "UPI Transfer",
            "Family Support",
            "Gift",
            ""
        ])
    })

upi_df = pd.DataFrame(upi_data)

upi_df.to_excel("input/UPI.xlsx", index=False)

print("DCARD, LRS and UPI dummy files generated successfully.")
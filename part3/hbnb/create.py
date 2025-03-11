import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/users/"

users = [
    {"first_name": "Vithuchan", "last_name": "One", "email": "vit@vit.com", "password": "Vit123456"},
    {"first_name": "Vithuchan", "last_name": "Two", "email": "vit2@vit.com", "password": "Vit123456"},
]

user_ids = []

for user in users:
    response = requests.post(BASE_URL, json=user)
    if response.status_code != 201:
        print(f"Error creating user: {response.text}")
        continue

    data = response.json()
    user_id = data.get("id")
    user_ids.append(user_id)
    print(f"Created user {user['first_name']} {user['last_name']} with ID: {user_id}")

# Ensure at least one user is created
if len(user_ids) == 0:
    print("No users created, stopping script.")
    exit()

user1 = user_ids[0] if len(user_ids) > 0 else None

BASE_URL2 = "http://127.0.0.1:5000/api/v1/auth/login"

token_data = {  # ✅ Fixed this from list to dictionary
    "email": "vit@vit.com",
    "password": "Vit123456"
}

response = requests.post(BASE_URL2, json=token_data)
if response.status_code != 200:  # Check if login is successful
    print(f"Error logging in: {response.text}")
    exit()

data = response.json()

# ✅ Check for correct token key
token_id = data.get("access_token") or data.get("token")

print(f"Token ID: {token_id}")

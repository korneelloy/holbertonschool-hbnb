import os

print("---------------- 👀 Checking task 0 ----------------")
# Define the expected directory structure
required_dirs = [
    "app",
    "app/api",
    "app/api/v1",
    "app/models",
    "app/services",
    "app/persistence"
]

# Check if all required directories and init files exist
missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
missing_init_files = [d for d in required_dirs if not os.path.isfile(os.path.join(d, "__init__.py"))]

if missing_dirs:
    print("❌ Missing directories:")
    for d in missing_dirs:
        print(f" - {d}")
else:
    print("✅ All required directories exist.")

if missing_init_files:
    print("❌ Missing __init__.py files in:")
    for d in missing_init_files:
        print(f" - {d}")
else:
	print("✅ All required __init__.py files exist.")
     
with open('app/__init__.py', 'r') as f:
	content = f.read()
	if "from flask import Flask" in content and "from flask_restx import Api" and "app = Flask(__name__)" in content:
		print("✅ app/__init__.py looks good.")
	else:
		print("❌ app/__init__.py is missing expected imports.")

inMemoryRepository_methods = [
      'add',
      'get',
      'get_all',
      'get_by_attribute',
      'update',
      'delete' ]

from app.persistence.repository import InMemoryRepository
from abc import ABC
missings_methods = [m for m in inMemoryRepository_methods if not hasattr(InMemoryRepository, m)]
if missings_methods:
	print("❌ InMemoryRepository is missing methods:")
	for m in missings_methods:
		print(f" - {m}")
else:
	print("✅ InMemoryRepository has all expected methods.")

if issubclass(InMemoryRepository, ABC):
	print("✅ InMemoryRepository is a subclass of ABC.")
else:
	print("❌ InMemoryRepository is not a subclass of object.")

from app.services.facade import HBnBFacade
facade = HBnBFacade()
missing_attributes = [a for a in ['user_repo', 'amenity_repo', 'place_repo', 'review_repo'] if not hasattr(facade, a)]
if missing_attributes:
	print("❌ HBnBFacade is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	wrong_attributes = [a for a in ['user_repo', 'amenity_repo', 'place_repo', 'review_repo'] if not isinstance(getattr(facade, a), InMemoryRepository)]
	if wrong_attributes:
		print("❌ HBnBFacade has wrong attributes:")
		for a in wrong_attributes:
			print(f" - {a}")
	else:
		print("✅ HBnBFacade has all expected attributes.")

with open("run.py", "r") as f:
	content = f.read()
	if "from app import create_app" in content and "app = create_app()" and "app.run(debug=True)" in content:
		print("✅ run.py looks good.")
	else:
		print("❌ run.py is missing expected imports.")

from config import Config, DevelopmentConfig
if DevelopmentConfig.DEBUG == True and Config.DEBUG == False and Config.SECRET_KEY:
	print("✅ config.py looks good")
else:
	print("❌ config.py is missing expected values.")

with open("requirements.txt", "r") as f:
	content = f.read()
	if "flask" in content and "flask-restx" in content:
		print("✅ requierements.txt looks good.")
	else:
		print("❌ requierements.txt is missing expected values.")

print("🫵 Check yourself if python3 run.py starts without any errors and access port 5000")
print("🫵 Check yourself if README exists and contains a brief overview of the project")
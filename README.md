# Fitness-Tracker-API
Using Fast API and Rest API architecture to create an application about Fitness Tracker
🏋️‍♂️ Secure Fitness Tracker API Backend

A high-performance, secure backend REST API architecture built using **FastAPI (Python 3.13)** and **PostgreSQL**. This system features complete isolation of environment configurations, asynchronous database operations, robust data validation via Pydantic, and a zero-trust OAuth2 authentication pipeline using modern native encryption.

 🚀 Key Architectural Features

-Asynchronous Execution Layer: Leverages Python's `async/await` paradigms via Uvicorn to process non-blocking database queries smoothly.
-Relational Data Persistence: Structured schemas managed via SQLAlchemy ORM, explicitly connecting endpoints to a persistent live ---------PostgreSQL environment (`fitness_db`).
-Native Bcrypt Migration: Built using standalone native `bcrypt` string matrices to guarantee full compatibility with Python 3.13 and avoid the common legacy wrapper `AttributeError` crashes.
-Stateful JWT Security: Secured via JSON Web Token (JWT) Bearer tokens to safely lock operational route validation checks.
- Interactive OpenAPI Documentation: Automated validation schemas exposed instantly via Swagger UI endpoint testing utilities.

📂 Project Directory Structure

fitness_tracker_api/
│
├── main.py          # Application entryway, routing definitions, and dependency hooks
├── auth.py          # Native bcrypt cryptographic operations and JWT token issuance
├── database.py      # Core SQLAlchemy engine instantiation and PostgreSQL sessions
├── models.py        # Declarative database mapping layouts for PostgreSQL tables
├── schemas.py       # Rigorous data payload format specifications (Pydantic validation)
├── .env             # High-security isolation parameters for credentials
└── README.md        # Technical execution documentation


🔧 Installation & Environment Setup
Follow these operational steps to deploy and run this repository locally on your machine.
git clone [https://github.com/YOUR_GITHUB_USERNAME/fitness-tracker-api.git](https://github.com/YOUR_GITHUB_USERNAME/fitness-tracker-api.git)
cd fitness-tracker-api


2. Configure Your Isolated Parameters (.env)
Create a file named .env inside your root directory and paste your connection strings and signing secret keys directly into it:
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fitness_db
SECRET_KEY=SUPER_SECRET_COMPLEX_KEY_HERE_123!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

3. Install Dependencies
Install the required packages, substituting legacy hashing contexts with stable native modules:
pip uninstall passlib
pip install fastapi uvicorn sqlalchemy psycopg2 bcrypt pyjwt python-dotenv


4. Boot Up the Application Server
Execute the Uvicorn application loop to bind your server instances to local ports:
uvicorn main:app --reload

🧪 Interactive API Integration Testing
Once the Uvicorn runtime reports an active server state, open your browser to interface with the OpenAPI test loop:

🔗 Interactive Documentation Gateway: http://127.0.0.1:8000/docs
The Lifecycle Testing Sequence:
Account Registration: Dispatch account payloads to POST /register. The system converts inputs to secure cryptographic texts and yields an explicit 201 Created code.

Authorization Exchange: Authenticate user parameters by clicking the green Authorize icon dialog box. Upon credential verification, the system hooks an authorization keycard block (bearer token) into your request tracking footprints.

Protected Submissions: Test backend input validation matrices by sending JSON profiles directly to POST /workouts/. Input formats violating schema criteria are safely checked and reported back via explicit 422 Unprocessable Content statuses to keep the relational persistence layer uncorrupted. Successful dispatches commit metrics down to the database automatically.

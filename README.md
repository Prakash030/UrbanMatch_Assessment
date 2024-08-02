# Marriage Matchmaking App

## Brief Description
The Marriage Matchmaking App is a simple backend application designed to help users find potential matches based on their profile information. The app allows users to create, read, update, and delete profiles with details such as name, age, gender, email, city, and interests.

The provided code includes:

### Basic Project Structure:

- **main.py** : The main application file with basic CRUD operations for user profiles.
- **models.py**: SQLAlchemy models defining the User schema.
- **database.py**: Database configuration and setup.
- **schemas.py**: Pydantic schemas for data validation and serialization.

### Functionality:

- Create User Endpoint: Create a new user profile.
- Read Users Endpoint: Retrieve a list of user profiles.
- Read User by ID Endpoint: Retrieve a user profile by ID.
- SQLite Database: The application uses SQLite as the database to store user profiles.

## Changes Made

### Database Schema
- **Interest Column Modification**: The `interests` column in the `user` table has been modified to store interests as a comma-separated string. This change was necessary due to the SQL database's limitation in supporting the Array datatype. The application continues to handle and process interests as lists/arrays in request and response payloads.

### Endpoints
- **User Endpoints**:
  - **Update User**: Endpoint to update user information based on `user_id`.
  - **Delete User**: Endpoint to delete a user from the database using `user_id`.
  - **Match Making**: Endpoint to find potential matches for a user based on the following criteria:
    - **Gender**: Only profiles of the opposite gender are considered.
    - **Age Range**: Matches are found within an age range of ±5 years from the user's age.
    - **Common Interests**: At least one common interest is required for a profile to be considered a match.

### Email Validation
- **Validation Using Pydantic**: Email addresses are validated using Pydantic's `EmailStr` to ensure they are in a valid format before storing or processing user data.

## Match Making Logic
- **Criteria for Matching**:
  1. **Opposite Gender**: Profiles must be of the opposite gender to the user.
  2. **Age Range**: The profile must fall within an age range of ±5 years from the user's age.
  3. **Common Interests**: The profile should share at least one common interest with the user.

### Prerequisites
- Python 3.7+
- FastAPI
- SQLAlchemy
- SQLite

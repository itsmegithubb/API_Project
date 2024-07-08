# Statistical Test Web Application

This project demonstrates a simple web application for performing statistical tests. It uses `FastAPI` for the API server, `Flask` for the client server, and basic HTML/CSS for the frontend.

## Technologies Used

- FastAPI
- Flask
- HTML
- CSS

## Project Structure

.
├── client-server
│ ├── app.py
│ └── templates
│ └── form.html
└── api-server
├── main.py
└── data
└── data.csv

markdown
Copy code

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

Ensure you have Python 3.6+ installed on your system.

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/itsmegithubb/API_Project.git
    cd statistical-test-webapp
    ```

2. **Create and activate a virtual environment:**

    On Windows:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

    On macOS/Linux:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the API server:**

    Navigate to the `api-server` directory and run the following command:

    ```sh
    cd api-server
    uvicorn main:app --reload
    ```

2. **Start the client server:**

    Open a new terminal, navigate to the `client-server` directory and run:

    ```sh
    cd client-server
    python app.py
    ```

3. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000` to access the client server.

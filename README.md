# Project Structure
```
menu_app/
│
├── templates/
│   └── upload.html
│
├── static/
│   └── uploads/
│
├── app.py
├── config.py
├── gsheet.py
├── ocr.py
├── .env
└── requirements.txt
```

# Steps to Run the Application
## Set up virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
## Create .env file:
Create a .env file in the root directory with your configuration values.

## Run the Flask application:
```
python app.py
```

## Access the web interface:
Open your browser and navigate to http://127.0.0.1:5000/ to upload an image and process it.

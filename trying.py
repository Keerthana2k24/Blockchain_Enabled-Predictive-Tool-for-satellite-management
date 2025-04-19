from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Mock dataset for satellite status (saved in a CSV file)
SATELLITE_DATA_FILE = 'satellite_data.csv'

# Load satellite data from CSV file
def load_satellite_data():
    # Load the dataset using pandas
    data = pd.read_csv(SATELLITE_DATA_FILE)
    return data

# Function to check satellite status and predict issues
def check_satellite_status(satellite_id):
    # Load the satellite data
    satellite_data = load_satellite_data()
    
    # Find the satellite by its ID (compare as string)
    satellite_info = satellite_data[satellite_data['satellite_id'] == satellite_id]
    
    # If the satellite is found in the dataset
    if not satellite_info.empty:
        satellite_info = satellite_info.iloc[0]
        
        # Initialize an empty list to store issues
        issues = []

        # Define conditions for the satellite being offline
        if satellite_info['battery_level'] < 20:
            issues.append('Battery Level Low')
        if satellite_info['signal_strength'] < 30:
            issues.append('Weak Signal Strength')
        if satellite_info['temperature'] > 75 or satellite_info['temperature'] < 10:
            issues.append('Temperature Out of Range')
        
        # Determine overall status based on the issues
        status = "offline" if issues else "online"
        
        # Return the status along with the satellite data and any issues
        return {
            "status": status,
            "info": satellite_info.to_dict(),
            "issues": issues
        }
    else:
        # If the satellite ID is not found
        return {
            "status": "not found",
            "message": f"Satellite with ID {satellite_id} not found."
        }

# Web page to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Web app route to handle satellite status request from form submission
@app.route('/satellite_status', methods=['POST'])
def satellite_status():
    satellite_id = request.form.get('satelliteId')
    
    if satellite_id:
        # Check the satellite status and issues
        satellite_status = check_satellite_status(satellite_id)
        
        # Render the result on the web page
        return render_template('result.html', status=satellite_status, satellite_id=satellite_id)
    else:
        return jsonify({"message": "Satellite ID not provided"}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

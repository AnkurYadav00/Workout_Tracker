import os
from datetime import datetime
import requests
import dotenv

dotenv.load_dotenv()

# TODO : Post request to nutritionix
APP_ID = os.getenv('APP_ID')
API_KEY = os.environ.get('API_KEY')
headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Content-Type': 'application/json'
}

# input
todaysWorkout = input('Enter today\'s workout goal completed: ')
content = {
    'query': todaysWorkout
}
response = requests.post(url='https://trackapi.nutritionix.com/v2/natural/exercise', headers=headers, json=content)
response.raise_for_status()

# workout stats response
workoutStats = response.json()['exercises']

# TODO : Post request to sheety (to update google-sheets)
AUTHENTICATION_KEY = os.environ.get('AUTHENTICATION_KEY')
USER_ID = os.environ.get('USER_ID')
header = {
    'Content-Type': 'application/json',
    'Authorization': AUTHENTICATION_KEY,
}
for stats in workoutStats:
    workouts = {
        'workout':
            {
                'date': str(datetime.now())[:10],
                'workouts': stats['name'],
                'duration': stats['duration_min'],
                'caloriesBurned': stats['nf_calories']
            }
    }

    # sheety requests
    sheet_response = requests.post(
        url=f"https://api.sheety.co/{USER_ID}/workoutsTracking/workouts",
        headers=header,
        json=workouts)
    sheet_response.raise_for_status()
    print(sheet_response.text)

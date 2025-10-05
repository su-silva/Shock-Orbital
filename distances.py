import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

api = "l7BmcPo9etREyMGq05KBuWrTKKDkJfoLlRWa14vY"
url = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api}'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    
    with open('approaches.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Approach_Date', 'Distance_km'])
        
        for neo in data['near_earth_objects'][:5]:
            for approach in neo['close_approach_data']:
                name = neo['name']
                date = approach['close_approach_date']
                distance = approach['miss_distance']['kilometers']
                writer.writerow([name, date, distance])
                
    print("CSV created : approaches.csv")
else:
    print("Error :", response.status_code)


look = pd.read_csv("approaches.csv")


look['Distance_km'] = pd.to_numeric(look['Distance_km'])


look['Approach_Date'] = pd.to_datetime(look['Approach_Date'])



plt.figure(figsize=(10,6))
sns.lineplot(x='Approach_Date', y='Distance_km', hue='Name', marker='o', data=look)
plt.ylabel("Distance to Earth (km)")
plt.title("Asteroid Close Approaches Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




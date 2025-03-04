import os
import requests
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()
# Access environment variables
api_key = os.getenv("TOMORROW_API_KEY")
# Literally my saving graces. All of this was dervied from code featured here https://www.geeksforgeeks.org/how-to-make-api-calls-using-python/ 
# https://docs.tomorrow.io/reference/realtime-weather This was also used a lot
# Requests documentation I pulled from https://pypi.org/project/requests/ 
# This calls the API via the url. This is specifically for the real time function
base_url = "https://api.tomorrow.io/v4/weather/realtime"
# This calls the API via the url. This is specifically for the forecast function
base_url2 = "https://api.tomorrow.io/v4/weather/forecast"
# Takes in a location defined by the user
def realtime_weather(location):
  # parameteres defined by the function. This keeps the API key safe in the env file and also accepts the location parameter. This specific real-time function accepts location names as well as longitude and latitude. For simplicity I decided to do a location name only.
  para = {"location": location, "apikey": api_key, "units": "imperial"}
  r = requests.get(base_url, params=para)
  # Status code 200 indicates a successful connection was made with the API and that the information was processed correctly
  if r.status_code == 200:
    # This returns the json response that the request requested
    data = r.json()
    # I asked chat GPT with help on format stuff https://chatgpt.com/share/67c65aa2-c308-8004-bf21-b69b18f3b716 
    values = data.get("data", {}).get("values", {})
    # saves the wind speed to a separate variable so I can convert to mph since it's in meters per second 
    wind_speed_ms = values.get("windSpeed")
    # Checks to see if the normal base wind speed is not null as it can be null if the wind isn't blowing. If it has a value then it performs the calculation. If it doesn't it sets the value to N/A
    if wind_speed_ms is not None:
      # I got this rounding function from here: https://www.w3schools.com/python/ref_func_round.asp 
      wind_speed_mph = round(wind_speed_ms * 2.23694, 0)
    else:
      wind_speed_mph = "N/A"
    # creates a dictionary with values to properly format the data. This also only prints the data that I want for my weather app
    WEATHER_CODE_MAP = {
    0: "Unknown",
    1000: "Clear, Sunny",
    1100: "Mostly Clear",
    1101: "Partly Cloudy",
    1102: "Mostly Cloudy",
    1001: "Cloudy",
    2000: "Fog",
    2100: "Light Fog",
    4000: "Drizzle",
    4001: "Rain",
    4200: "Light Rain",
    4201: "Heavy Rain",
    5000: "Snow",
    5001: "Flurries",
    5100: "Light Snow",
    5101: "Heavy Snow",
    6000: "Freezing Drizzle",
    6001: "Freezing Rain",
    6200: "Light Freezing Rain",
    6201: "Heavy Freezing Rain",
    7000: "Ice Pellets",
    7101: "Heavy Ice Pellets",
    7102: "Light Ice Pellets",
    8000: "Thunderstorm"
    }
    # Gets the weather code from the API
    weather_code_num = values.get("weatherCode", "N/A")
    # Maps the code with the text presented in the dictonary. Defaults to unknown
    weather_code_text = WEATHER_CODE_MAP.get(weather_code_num, "Unknown")
    # Gets specified values from the API so I can print them to the user
    weather_details = {
      "Temperature ": f"{values.get("temperature", "N/A")}°F",
      "Humidity ": f"{values.get("humidity", "N/A")}%",
      "Cloud Cover ": f"{values.get("cloudCover", "N/A")}%",
      "Dew Point ": f"{values.get("dewPoint", "N/A")}°F",
      "Precipitation Probability ": f"{values.get("precipitationProbability", "N/A")}%",
      "Wind Speed ": f"{wind_speed_mph} mph",
      "Wind Direction ": f"{values.get("windDirection", "N/A")}°",
      "UV Index": values.get("uvIndex"),
      "Weather Conditions": weather_code_text
    }
    # This just prints everything and makes sure the \n keyword is with each line (It basically automatically prints everything to a new line)
    formatted_output = "\n".join([f"{key}: {value}" for key, value in weather_details.items()])
    return formatted_output
  # If the program fails to find the location, it will return an error message to the user.
  else:
    return f"Error finding location."
# This function takes in a location and displays a 5 day weather forecast for that location
def forecast_weather(location):
    # the parameters include the location, my api key and the units I wanted it to be in. I chose imperial because we're in the US lol
    para = {"location": location, "apikey": api_key, "units": "imperial"}
    #this takes the 2nd url which maps to the forecast page
    r = requests.get(base_url2, params=para)
    #If the request is successful then the function will start
    if r.status_code == 200:
        data = r.json()
        # This ensures that the forecast is daily
        forecasts = data.get("timelines", {}).get("daily", [])  
        # This outputs the location that the user selected
        forecast_output = f"Weather Forecast for {location}:\n"
        # Because we are dealing with multiple forecasts, this loop is used to print every forecast in the list 
        for forecast in forecasts:
            # This gets the time and converts the dates to the proper format
            date = forecast.get("time", "N/A")[:10]  
            # this gets all the values specified in the json for this function
            values = forecast.get("values", {})
            # Like in the previous function, I converted wind speed from m/s to mph
            wind_speed_ms = values.get("windSpeedAvg")
            wind_speed_mph = round(wind_speed_ms * 2.23694, 0) if wind_speed_ms is not None else "N/A"
            # Like in the previous function, I created a dictionary to map the weather code to the words for easier readability 
            WEATHER_CODE_MAP = {
              0: "Unknown",
              1000: "Clear, Sunny",
              1100: "Mostly Clear",
              1101: "Partly Cloudy",
              1102: "Mostly Cloudy",
              1001: "Cloudy",
              2000: "Fog",
              2100: "Light Fog",
              4000: "Drizzle",
              4001: "Rain",
              4200: "Light Rain",
              4201: "Heavy Rain",
              5000: "Snow",
              5001: "Flurries",
              5100: "Light Snow",
              5101: "Heavy Snow",
              6000: "Freezing Drizzle",
              6001: "Freezing Rain",
              6200: "Light Freezing Rain",
              6201: "Heavy Freezing Rain",
              7000: "Ice Pellets",
              7101: "Heavy Ice Pellets",
              7102: "Light Ice Pellets",
              8000: "Thunderstorm"
              }
            # This gets the weather code for the specified day
            weather_code_num = values.get("weatherCodeMax", "N/A")
            # This maps the weather code to the text and stores it in a variable to print to the console
            weather_code_text = WEATHER_CODE_MAP.get(weather_code_num, "Unknown")
            # This is a list of all of the weather details that I want to display to the user. All names were found in the json of the API
            weather_details = {
                "Date": date,
                "Temperature High": f"{values.get('temperatureMax', 'N/A')}°F",
                "Temperature Low": f"{values.get('temperatureMin', 'N/A')}°F",
                "Humidity": f"{values.get('humidityAvg', 'N/A')}%",
                "Cloud Cover": f"{values.get('cloudCoverAvg', 'N/A')}%",
                "Dew Point": f"{values.get('dewPointAvg', 'N/A')}°F",
                "Precipitation Probability": f"{values.get('precipitationProbabilityAvg', 'N/A')}%",
                "Wind Speed": f"{wind_speed_mph} mph",
                "Wind Direction": f"{values.get('windDirectionAvg', 'N/A')}°",
                "UV Index": values.get("uvIndexAvg"),
                "Weather Conditions": weather_code_text
            }
            # This ensures that each forcast is outputted correctly and that each one is actually displayed
            forecast_output += "\n".join([f"{key}: {value}" for key, value in weather_details.items()]) + "\n\n"
        # Finally, the forecast output is returned to be displayed
        return forecast_output
    else:
        # If the program has issues getting the forecast data an error message will show 
        return "Error retrieving forecast data."
# This is the menu for the weather app. It allows the user to select if they want a 5 day forecast or if they want current weather conditions while the user has not requested to exit the program, the service continues
while True:
  # prints the menu options to a user
  print(f"\nWelcome to the Weather App. Please select from the following options: \n [1.] Current weather conditions\n [2.] 5 day forecast\n [3.] Exit")
  # Collects the choice data from a user
  choice = input("Enter the number of your choice: ")
  # uses the choice to call the correct function and print the data to the user
  if choice == "1":
        location = input("Enter the city for current weather conditions: ")
        print("\nFetching real-time weather...\n")
        print(realtime_weather(location))
  elif choice == "2":
        location = input("Enter the city for the weather forecast: ")
        print("\nFetching 5 day weather forecast...\n")
        print(forecast_weather(location))
  # If the user wants to exit the app, it exits and says a message
  elif choice == "3":
        print("Exiting the Weather App.")
        break
  # If the user enters something funky it tells the user that the input is invalid and to try again
  else:
        print("Invalid choice. Please enter 1, 2, or 3.")
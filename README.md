# Using-web-API-project
Project using Web API, I'm specifically using one for Tomorrow.io's web thing. It's for weather data. I wanted to make my own silly weather app. The user will input a location and the API will output the real-time weather for the application. 

## Issues
- Was absent from class when we went over this so I had to google how to do it. I was confused on how to use the web API service in general. I decided to use the http.client functions after doing some digging.
- I imported them into the file as requested. Also, I'm confused as fuck over github even though I've been using it for years lol (delete this later).
- Literally my saving grace: https://www.geeksforgeeks.org/how-to-make-api-calls-using-python/
- Also my saving grace: https://www.tomorrow.io/blog/build-your-own-weather-app-with-one-api-call/ By using this, I was able to interpret the functions and fields of the weather. 
- I was having trouble remembering how to call the API. I was able to figure it out with the above links.
- I wanted to format the weather data so the user can read and interpret the data. I started googling ways on how to do that. The console outputted a lot of weather nerd stuff that a basic person wouldn't be able to understand. (I ended up asking chat GPT for help. A link to the convo is located in the code.)
- It took me a while to figure out how to properly separate the url into a way for the program to read. I kept getting errors and my built in error message of, "Error cannot find location" even when the default value was typed in. I ended up looking through tomorrow.io and documentation and using the auto generation that vscode provides to figure it out.
- I wanted to convert meters per second into miles per hour because it's easier to read for me. I started with googling the conversion rate and then attempted to apply simple math to the program.
- I was able to do the conversion but it kept all the trailing decimal places. I googled how to round in python.
- I had trouble converting the weather code to the actual readable text.
- I had some issues with creating the forecast function. The variables were different from the real-time weather so it was difficult to figure out what values I was supposed to use. 

## Ideas
- I decided to split the URLs into two parts, one with the location and one with the API key for security reasons. This way the key will stay safe
- I also decided I was going to create a weather app that will display in the console based on multiple inputs from the user.
- I thought it was too basic so I wanted to add an option to do a forecast too
- I wanted to add a menu so the user could input city


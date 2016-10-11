# About
This is a project I made which showcases pulling data from the WxUnderground Current Conditions API, formatting that data, then pushing it to Geckoboard's API

# Flow of Operations
This script pulls data from two APIs; WxUnderground's Current Conditions API and my own personal Raspberry PI, equipped with a sense hat for measuring atmospheric conditions. It then formats that data to match the format required by Geckoboard's API. The script then pushes the data into Geckoboard's API.

# Language Choice
I chose to write this in Python, as that's the language I am most comfortable working with. I used the CherryPy package to host the API on my Raspberry PI, as it was rather simple to get off the ground and I've used it previously in other projects. I opted to make the API calls using the Requests package, as it's very simple to use once you've played around with it a bit.

# Issues Encountered
I encountered some issues translating the CURL POST command into "Python-ese", but a good bit of Googling helped me figure that out. I also ran into some issue understanding Geckoboard's API documentation ( https://developer.geckoboard.com/ ), as it was unclear about how variables were named; that slowed me down a bit, but I was able to figure it out.

# Finished Product
You can see the dashboard and the weather data I've collected at this link: https://cdchris12.geckoboard.com/dashboards/XP4D6A2AUIOICFCG

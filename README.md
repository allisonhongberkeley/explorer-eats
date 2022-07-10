### Food Explorer

#### About The Project:
In this project, I built a web application that allows users to explore new restaurants nearby and in locations of interest. The search functionality that I implemented specifically enables searching for restaurants based on location, cuisine type, and price and returns best-match results to the user.  

After filtering out merchants through searches, users can add places that they want to visit to a wishlist! From the wishlist, if the user decides that they enjoyed the food and/or experience, they can add merchants to their ‘favorites.’ 

#### User Authentication: 
The registration/login processes were built using bcrypt and MongoDB. When a user registers an account, their password is hashed with a salt and their login information is inserted into the backend database. When a user logs in, their username and hashed password is looked up and if a match is found, a successful login ensues. In the case of an error due to invalid credentials (wrong username/password, registering an account with a username that’s been taken), the app will flash an error message and re-route the user to the previous HTTP request. 

#### API Integration: 
The app pulls data from the Yelp Fusion API to return top results to the user. The search page takes in location, cuisine category, and a price range as HTML form inputs, and the inputs are parsed and re-formatted to match the query parameters specified by the Yelp Developers documentation. Finally, the app contacts the API endpoint to retrieve merchants that match the given specifications, and returns the information to the user on the frontend. 

#### User Interface: 
The UI is simple, clear, and aesthetic. Since the main functionality of the app is for users to find, save, and like restaurants, it is designed to be informative and easy to navigate. Attached below are example photos of the UI.


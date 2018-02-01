"""Goal: Create a program where users can input two locations and return a restaurant as equidistant as possible between them. This will be done by connecting
with the GoogleMaps Directions and Places API. Once a suitable establishment has been found, the program will return the establishment's name, address, phone number, and hours of operation."""


#!/usr/bin/env python3

import requests, json, pprint
#The requests and json modules allow me to access the JSON data from the Google APIs
#pprint allows me to return the data in a format that is easier to read


DIRECTIONS_API_KEY = 'AIzaSyDmLGPIUErCNSmM-FPFSUGS9LIPFv9cbRI' #GoogleMaps Directions API Key
PLACES_API_KEY = 'AIzaSyDR_0dNH_A30KWnjz3s7GG7PZw6Vo3WkDQ' #Google Places API Key
#I do not expect a lot of people to be accessing this program on GitHub currently, so I feel comfortable leaving in the API Keys and am not worried about going over the request limit.

print('Welcome to Middle Ground.\n\nThis project is still being developed, so please use the following guidelines: \n1. Make sure the addresses are spelled completely and correctly \n2. Restart the program if you have made an error while typing either address \n3. Since Middle Ground identifies restaurants within 500 meters of the midpoint,\n it is currently best suited for use when both addresses in the same city\n')

street_address_a = input('Please enter the street address only of Person A. \nDo not include city or state: ')
city_a = input('Enter the city of Person A: ')
state_a = input('Enter the state of Person A: ')
updated_address_a = str(street_address_a) + ' ' + str(city_a) + ' ' + str(state_a)
#print(updated_address_a) Commented this out but have been using this for troubleshooting while testing

street_address_b = input('\nPlease enter the street address only of Person B. \nDo not include city or state: ')
city_b = input('Enter the city of Person B: ')
state_b = input('Enter the state of Person B: ')
updated_address_b = str(street_address_b) + ' ' + str(city_b) + ' ' + str(state_b)
#print(updated_address_b) Also used for troubleshooting

#This is a good start, but is still pretty error prone. I need to add ways for the user to confirm the address is correct, with options to revise if there is a typo. I also need to confirm that the user's input is valid (e.g. not entering numbers or special characters instead of letters for city and state)

print('\nLet\'s find a restaurant at the midpoint of those locations!\nPlease wait... this may take a few moments.')

#We have gathered all the necessary information from the user, now we need to connect with the GoogleMaps API

api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(updated_address_a, DIRECTIONS_API_KEY))
api_response_dict = api_response.json()

if api_response_dict['status'] == 'OK':
    latitude_a = api_response_dict['results'][0]['geometry']['location']['lat']
    longitude_a = api_response_dict['results'][0]['geometry']['location']['lng']


api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(updated_address_b, DIRECTIONS_API_KEY))
api_response_dict = api_response.json()

if api_response_dict['status'] == 'OK':
    latitude_b = api_response_dict['results'][0]['geometry']['location']['lat']
    longitude_b = api_response_dict['results'][0]['geometry']['location']['lng']

#This code is a little repetitive and against the DRY principle. Look into making this a loop soon

#Now that the latitude and longitude of both addresses has been pulled from the GoogleMaps Directions API, I am going to average them together to find a midpoint

def find_average(input_a, input_b):
    return((input_a + input_b)/2)

average_latitude = find_average(latitude_a, latitude_b)
average_longitude = find_average(longitude_a, longitude_b)

list_places = requests.get('https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' + str(average_latitude) + ',' + str(average_longitude) + '&radius=500&type=restaurant&key=' + str(PLACES_API_KEY))

list_places_dict = list_places.json()
if list_places_dict['status'] == 'OK': #Checking to make sure there an establishment is found within 500 meters of the midpoint
    place_id = list_places_dict['results'][0]['place_id'] #This pulls the Place ID of the first result on the list of bars and restaurants within 500 meters of the middle point
    place_details = requests.get('https://maps.googleapis.com/maps/api/place/details/json?placeid=' + str(place_id) + '&key=' + str(PLACES_API_KEY))
    place_details = place_details.json()
    if place_details['status'] == 'OK':
        place_name = place_details['result']['name']
        place_address = place_details['result']['formatted_address']
        place_phone = place_details['result']['formatted_phone_number']
        place_hours = place_details['result']['opening_hours']['weekday_text']
        print('\nYou should meet at ' + place_name) #This is the name of the restaurant closest to the midpoint.
        print(place_address)
        print(place_phone)
        pprint.pprint(place_hours) #Using pprint module to print days and hours on separate lines
        print('\nEnd of program. Run Middle Ground again to put in a new address.')
else:
    print('\nI\'m sorry, I could not find a restaurant within 500 meters of the midpoint. \nPlease run Middle Ground again to put in a new address.')
#Add an option to put in a new address
      
"""Future improvements:
- Give users the choice to input restaurant, bar, cafe, museum, or any of the other supported "types" on the Google Places API
- Return a list of establishment choices, with options to rank by distance from midpoint or Yelp rating
- Make the acceptable radius of the midpoint establishment a percentage of the total distance between locations. Users traveling longer distances may be more willing to drive an extra few miles out of the way to visit a higher-rated establishment than users who plan on only walking a few city blocks to meet their friend."""




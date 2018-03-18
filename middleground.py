"""Goal: Create a program where users can input two locations and return a restaurant as equidistant as possible between them.
This will be done by connecting with the GoogleMaps Directions and Places API.
Once a suitable establishment has been found, the program will return the establishment's name, address, phone number, and hours of operation.
If a restaurant can not be found within 500 meters of the midpoint, Middle Ground will automatically expand the radius to 5000 meters."""


#!/usr/bin/env python3

import requests, json, pprint
#The requests and json modules allow me to access the JSON response from the Google APIs
#pprint allows me to return the data to the user in a format that is easier to read


DIRECTIONS_API_KEY = 'AIzaSyDmLGPIUErCNSmM-FPFSUGS9LIPFv9cbRI' #GoogleMaps Directions API Key
PLACES_API_KEY = 'AIzaSyDR_0dNH_A30KWnjz3s7GG7PZw6Vo3WkDQ' #Google Places API Key
#I do not expect a lot of people to be accessing this program on GitHub currently, so I feel comfortable leaving in the API Keys and am not worried about going over the request limit.

print('Welcome to Middle Ground.\n\nPlease use the following guidelines for the best results:')
print('\n1. Make sure the addresses are spelled completely and correctly.\nAddresses are not case-sensitive and standard postal abbreviations are acceptable.')
print('\n2. Restart the program if you have made an error while typing either address.')
print('\n3. Since Middle Ground aims to find restaurants within 500 meters of the midpoint, it is best suited for use in densely populated areas.\n')
print('*****************************************************\n\n')

restart = 1
#This code gives users the option to restart the program or exit when finished
while restart != "X" and restart != "x":
    
    street_address_a = input('Please enter the street address only of Person A. \nDo not include city or state: ')
    city_a = input('Enter the city of Person A: ')
    state_a = input('Enter the state of Person A: ')
    updated_address_a = str(street_address_a) + ' ' + str(city_a) + ' ' + str(state_a)

    street_address_b = input('\nPlease enter the street address only of Person B. \nDo not include city or state: ')
    city_b = input('Enter the city of Person B: ')
    state_b = input('Enter the state of Person B: ')
    updated_address_b = str(street_address_b) + ' ' + str(city_b) + ' ' + str(state_b)

    #Should add way for user to confirm the address is correct, with options to revise if there is a typo.
    #Should add exception handling to confirm that the user's input is valid (e.g. not entering numbers or special characters instead of letters for city and state)

    print('\nLet\'s find a restaurant at the midpoint of those locations!\nPlease wait... this may take a few moments.')

    #I have gathered all the necessary information from the user, now I need to connect with the GoogleMaps Directions API

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

    #Now that the latitude and longitude of both addresses has been pulled from the GoogleMaps Directions API, I am going to average them together to find a midpoint

    def find_average(input_a, input_b):
        return((input_a + input_b)/2)

    average_latitude = find_average(latitude_a, latitude_b)
    average_longitude = find_average(longitude_a, longitude_b)

    list_places = requests.get('https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' + str(average_latitude) + ',' + str(average_longitude) + '&radius=500&type=restaurant&key=' + str(PLACES_API_KEY))
    list_places_dict = list_places.json()

    if list_places_dict['status'] == 'OK':
        #Checking to make sure there an establishment is found within 500 meters of the midpoint
        place_id = list_places_dict['results'][0]['place_id']
        #This pulls the Place ID of the first result on the list of bars and restaurants within 500 meters of the middle point
        place_details = requests.get('https://maps.googleapis.com/maps/api/place/details/json?placeid=' + str(place_id) + '&key=' + str(PLACES_API_KEY))
        place_details = place_details.json()

        if  place_details['status'] == 'OK':
            place_name = place_details['result']['name']
            place_address = place_details['result']['formatted_address']
            place_phone = place_details['result']['formatted_phone_number']
            place_hours = place_details['result']['opening_hours']['weekday_text']
            print('\nYou should meet at ' + place_name)
            #This is the name of the restaurant closest to the midpoint.
            print(place_address)
            print(place_phone)
            pprint.pprint(place_hours)
            #Using pprint module to print days and hours on separate lines
            restart = input('\nPress ENTER to input new addresses or type X to exit.\n')

    else:
        print('\nI\'m sorry, I could not find a restaurant within 500 meters of the midpoint. \nI am now checking for a restaurant within 5000 meters.')
        #This addition allows for more flexibility in suburban areas or if both addresses are not located in the same city.
        list_places = requests.get('https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' + str(average_latitude) + ',' + str(average_longitude) + '&radius=5000&type=restaurant&key=' + str(PLACES_API_KEY))
        list_places_dict = list_places.json()

        if list_places_dict['status'] == 'OK':
            #Checking to make sure there an establishment is found within 5000 meters of the midpoint
            place_id = list_places_dict['results'][0]['place_id']
            #This pulls the Place ID of the first result on the list of bars and restaurants within 500 meters of the middle point
            place_details = requests.get('https://maps.googleapis.com/maps/api/place/details/json?placeid=' + str(place_id) + '&key=' + str(PLACES_API_KEY))
            place_details = place_details.json()

            if  place_details['status'] == 'OK':
                place_name = place_details['result']['name']
                place_address = place_details['result']['formatted_address']
                place_phone = place_details['result']['formatted_phone_number']
                place_hours = place_details['result']['opening_hours']['weekday_text']
                print('\nYou should meet at ' + place_name)
                #This is the name of the restaurant closest to the midpoint.
                print(place_address)
                print(place_phone)
                pprint.pprint(place_hours)
                #Using pprint module to print days and hours on separate lines
                restart = input('\nPress ENTER to input new addresses or type X to exit.\n')

        else:
            print('\nI\'m sorry, there does not appear to be a restaurant within 5000 meters of the midpoint. \nMiddle Ground is working on expanding functionality to less densely populated areas, so stay tuned for future updates!')
            restart = input('\nPress ENTER to input new addresses or type X to exit.\n')
                        
                      
"""FUTURE IMPROVEMENTS:

- Give users the choice to input restaurant, bar, cafe, museum, or any of the other supported "types" on the Google Places API

- Return a list of establishment choices, with options to rank by distance from midpoint or Yelp rating

- Make the acceptable radius of the midpoint establishment a percentage of the total distance between locations. Users traveling longer distances may be more willing to drive an extra few miles out of the way to visit a higher-rated establishment than users who plan on only walking a few city blocks to meet their friend.

- Take into consideration whether users will be driving, walking, public transportation as that can affect commuting time

- Explore whether I can connect Middle Ground with OpenTable to allow users to make a reservation

- Some results (McDonald's, Cozi, etc), while accurate, could be disappointing to users who are looking for a more elegant dining experience. Add a way for users to receive a second restaurant result if they are not happy with the first one. In some locations, chain restaurants may make up the bulk of available establishments, so I don't want to screen them out completely."""



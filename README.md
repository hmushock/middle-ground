<h1>Middle Ground</h1>

<h2>Synopsis</h2>

Middle Ground is a program that allows users to input two addresses and find a restaurant within 500 meters of the midpoint, simplifying the process of meeting up with friends who might not live in the same area of the city or in different towns. Middle Ground is currently fully functional for use in major urban areas such as Philadelphia, New York, and their suburbs. The program has recently been updated to automatically expand the acceptable radius to 5000 meters if there is not a dining establishment within 500 meters of the midpoint, allowing for greater flexibility when used in suburban areas or when traveling between different cities and towns.

Middle Ground uses Python 3 to connect with the GoogleMaps Directions API and Google Places API, returning the JSON response.

There are a few best practices to keep in mind while using Middle Ground. It is best suited for use in densely populated areas where it would be rare not to have a dining establishment within 500 (or 5000) meters of any address. Even if both addresses are in urban areas, long distances can affect the functionality of this program. For example, if you are traveling from Brooklyn to meet up with a friend from Los Angeles, Middle Ground might not be able to find a restaurant if the midpoint is in a very rural area of the midwest.

<h2>Motivation</h2>

As a resident of Philadelphia for nearly seven years, I have noticed a reoccurring problem with indecisiveness when meeting up with friends from other areas of the city. With parking spaces at a premium, slow public transportation, and often unreliable weather, I decided to develop a program to streamline this process. Middle Ground not only chooses a meeting place, but ensures that the distance is equitable to both parties and provides users with all necessary information about the establishment (address, phone number, and hours of operation).

<h2>Installation</h2>

Middle Ground uses Python 3. If you do not have Python 3 already installed on your computer, you can install the latest version from www.python.org.

The following libraries must also be installed in your Python interpreter before running Middle Ground. 

   - requests: https://pypi.python.org/pypi/requests/2.7.0

   - pprint: https://pypi.python.org/pypi/pprintpp

The above libraries can be installed using pip. If you do not have pip or are not sure, you can learn more here: https://pip.pypa.io/en/stable/installing/

Middle Ground also uses the json module. However, this is part of the standard Python library and does not need to be installed with pip.

<h2>API Documentation</h2>

Middle Ground uses the following Google APIs:

**GoogleMaps Directions API:** https://developers.google.com/maps/documentation/directions/

**Google Places API:** https://developers.google.com/places/

<h2>Contributors</h2>

* **Heather Mushock** - Initial work

<h2>License</h2>

This project is licensed under the MIT License - see the LICENSE.txt file for details.

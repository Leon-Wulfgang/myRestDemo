from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "Q1VFKMAC3WKRFTMZ3UX3EI2KOECON1S4K2NV1EE1Z3XNVJSG"
foursquare_client_secret = "VBYTUEY1EHRZTULHFOQFD3ZXX4AP5UEM4VOO23UEMOSHL3K3"


def findARestaurant(mealType, location):
    print mealType, location
    lat, lng = getGeocodeLocation(location)
    coordinateString = "%s,%s" % (lat, lng)
    print coordinateString

    # queryUrl = "https://api.foursquare.com/v2/venues/search"
    queryUrl = "https://api.foursquare.com/v2/venues/explore"
    queryLimit="1"
    queryVer = "20130815"
    queryString = "%s" \
                  "?client_id=%s" \
                  "&client_secret=%s" \
                  "&ll=%s" \
                  "&query=%s" \
                  "&limit=%s" \
                  "&venuePhotos=1" \
                  "&v=%s" \
                  % (queryUrl, foursquare_client_id, foursquare_client_secret, coordinateString, mealType, queryLimit, queryVer)
    h = httplib2.Http()
    response, content = h.request(queryString, 'GET')
    result = json.loads(content)

    name = result['response']['groups'][0]['items'][0]['venue']['name']
    address = ','.join(result['response']['groups'][0]['items'][0]['venue']['location']['formattedAddress'])
    image1 = result['response']['groups'][0]['items'][0]['venue']['photos']['groups'][0]['items'][0]['prefix']
    image2 = "width300"
    image3 = result['response']['groups'][0]['items'][0]['venue']['photos']['groups'][0]['items'][0]['suffix']
    image = "%s%s%s" % (image1, image2, image3)
    result = {
        'name': name,
        'address': address,
        'image': image
    }
    print result

    # write to file for json viewer
    with open('preview.json', 'ab+') as f:
        #f.write(str(result['response']['groups'][0]['items'][0]))
        f.write('\n')
        f.write('\n'.join([name, address, image]).encode('utf8'))
        f.write('\n')




# 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

# 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
# HINT: format for url will be something like
# https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

# 3. Grab the first restaurant
# 4. Get a  300x300 picture of the restaurant using the venue_id
#  (you can change this by altering the 300x300 value in the URL or replacing it
#  with 'original' to get the original picture
# 5. Grab the first image
# 6. If no image is available, insert default a image url
# 7. Return a dictionary containing the restaurant name, address, and image url
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")

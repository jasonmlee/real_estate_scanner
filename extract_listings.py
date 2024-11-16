import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

class Listings:

    def __init__(self, area):
        self.area = area

    def get_response(self):
        """
        Makes API Call from MLS API and returns the response as a json
        """

        LatMax = self.area['LatMax']
        LatMin = self.area['LatMin']
        LongMax = self.area['LongMax']
        LongMin = self.area['LongMin']

        url = "https://realty-in-ca1.p.rapidapi.com/properties/list-residential"

        querystring = {"LatitudeMax": LatMax,"LatitudeMin": LatMin,"LongitudeMax": LongMax,"LongitudeMin": LongMin,"CurrentPage":"1","RecordsPerPage":"100","SortOrder":"A","SortBy":"1","CultureId":"1","NumberOfDays":"0","BedRange":"0-0","BathRange":"0-0","RentMin":"0"}

        headers = {
            "x-rapidapi-key": "c0a8ab37d5msh2445478aa64c3cdp12cb17jsn29d89a3ba80f",
            "x-rapidapi-host": "realty-in-ca1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return data

    def get_listings(self):
        """
        Takes the response json and converts it into a dataframe
        """

        data = self.get_response()
        info = []

        for result in data['Results']:
                id = result.get('Id', 'N/A')
                PublicRemarks = result.get('PublicRemarks', 'N/A')
                Bathroom = result.get('Building',{}).get('BathroomTotal', 'N/A')
                Bedrooms = result.get('Building', {}).get('Bedrooms', 'N/A')
                Sqft_str = result.get('Building', {}).get('SizeInterior', 'N/A')

                if Sqft_str != 'N/A':
                    Sqft_str = Sqft_str.replace(' sqft', '')
                    Sqft = int(Sqft_str)
                else: 
                    Sqft = 0

                Price_str = result.get('Property', {}).get('Price', 'N/A')

                if Price_str != 'N/A':
                    Price_str = Price_str.replace('$', '').replace(',', '')
                    Price = int(Price_str)
                else:
                    Price = 'N/A'

                Type = result.get('Property', {}).get('Type', 'N/A')
                Address = result.get('Property', {}).get('Address', {}).get('AddressText', 'N/A')
                Longitude = result.get('Property', {}).get('Address', {}).get('Longitude', 'N/A')
                Latitude = result.get('Property', {}).get('Address', {}).get('Latitude', 'N/A')
                PostalCode = result.get('PostalCode', 'N/A')

                listing_dict = {"id": id,
                                "PublicRemarks": PublicRemarks,
                                "Bathroom": Bathroom,
                                "Bedrooms": Bedrooms,
                                "Sqft": Sqft,
                                "Price": Price,
                                "Type": Type,
                                "Address": Address,
                                "Longitude": Longitude,
                                "Latitude": Latitude,
                                "PostalCode": PostalCode,
                                }

                info.append(listing_dict)

        final_result = pd.DataFrame(info).sort_values('Price', ascending = False).reset_index()
        return final_result
    
TerraNova = {"LatMax": 49.1745,
             "LatMin": 49.1662,
			 "LongMax":-123.1749,
			 "LongMin":-123.1902}

PointGrey = {"LatMax": 49.2691,
             "LatMin": 49.2583,
			 "LongMax":-123.1840,
			 "LongMin":-123.2154}

MainSt = {"LatMax": 49.2567,
          "LatMin": 49.2563,
		  "LongMax":-123.0899,
		  "LongMin":-123.1151}

TN = Listings(TerraNova)
PG = Listings(PointGrey)
MainSt = Listings(MainSt)

#TerraNova_listings = TN.get_listings()
#TerraNova_listings.to_csv("TerraNova_listings.csv")

#PointGrey_listings = PG.get_listings()
#PointGrey_listings.to_csv("PointGrey_listings.csv")

#MainSt_listings = MainSt.get_listings()
MainSt_listings_r = MainSt.get_response()
print(MainSt_listings_r)
#MainSt_listings.to_csv("MainSt_listings.csv")
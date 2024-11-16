import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_property_details(PropertyId):
	"""
	Takes the ID of an individual property and retrieves property details from the MLS API
	"""
	
	url = "https://realty-in-ca1.p.rapidapi.com/properties/detail"

	querystring = {"ReferenceNumber":"30794904","PropertyID":PropertyId,"PreferedMeasurementUnit":"1","CultureId":"1"}

	headers = {
	    "x-rapidapi-key": "c0a8ab37d5msh2445478aa64c3cdp12cb17jsn29d89a3ba80f",
	    "x-rapidapi-host": "realty-in-ca1.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	property_details = response.json()

	Id = property_details.get('Id', 'N/A')
	MlsNumber = property_details.get('MlsNumber', 'N/A')
	PublicRemarks = property_details.get('PublicRemarks', 'N/A')
	Type = property_details.get('Building', {}).get('Type', 'N/A')
	Amenities = property_details.get('Building', {}).get('Amenities', 'N/A')
	ArchitecturalStyle = property_details.get('Building', {}).get('ArchitecturalStyle', 'N/A')
	ConstructedDate = property_details.get('Building', {}).get('ConstructedDate', 'N/A')
	HeatingType = property_details.get('Building', {}).get('HeatingType', 'N/A')
	BuiltIn = property_details.get('Building', {}).get('BuiltIn', 'N/A')
	Parking1 = property_details.get('Property', {}).get('Parking', {})[0].get('Name', 'N/A')
	Parking2 = property_details.get('Property', {}).get('ParkingSpaceTotal', 'N/A')
	OwnershipType = property_details.get('Property', {}).get('OwnershipType', 'N/A')
	MaintenanceFee = property_details.get('Property', {}).get('MaintenanceFee', 'N/A')
	TaxAmount = property_details.get('Property', {}).get('TaxAmount')
	PreviousClosePrice = property_details.get('History', {})[0].get('ClosePrice', 'N/A')
	PreviousSaleDate = property_details.get('History', {})[0].get('StatusEffectiveDate', 'N/A')
	Photos = property_details.get('Property', {}).get('Photo', [])

	property_details_dict = {
			 "Id": Id,
			 "MlsNumber": MlsNumber,
			 "PublicRemarks": PublicRemarks,
			 "Type": Type,
			 "Amenities": Amenities,
			 "ArchitecturalStyle": ArchitecturalStyle,
			 "ConstructedDate": ConstructedDate,
			 "HeatingType": HeatingType,
			 "BuiltIn": BuiltIn,
			 "Parking1": Parking1,
			 "Parking2": Parking2,
			 "OwnershipType": OwnershipType,
			 "MaintenanceFee": MaintenanceFee,
			 "TaxAmount": TaxAmount,
			 "PreviousClosePrice": PreviousClosePrice,
			 "PreviousSaleDate": PreviousSaleDate
	}

	for photo in Photos:
		sequence_id = photo.get('SequenceId')
		high_res_path = photo.get('HighResPath')
		if sequence_id and high_res_path:
			key = f"image_{sequence_id}"
			property_details_dict[key] = high_res_path

	return property_details_dict

def get_full_details(csv_path):
	"""
	Takes a path to a CSV of listings and uses its property ID to make a query to retrieve its property details. Returns a dataframe.
	"""

	listings_df = pd.read_csv(csv_path)
	property_details_list = []

	for index, row in listings_df.iterrows():
		PropertyId = row['id']
		try:
			property_details = get_property_details(PropertyId)
			property_details_list.append(property_details)
		except:
			pass

	property_details_df = pd.DataFrame(property_details_list)
	listings_df['id'] = listings_df['id'].astype(str)
	property_details_df['Id'] = property_details_df['Id'].astype(str)
	final_result = pd.merge(listings_df, property_details_df, left_on = 'id', right_on='Id', how= 'left')
	return final_result

#csv_path = "TerraNova_listings.csv"
csv_path = "PointGrey_listings.csv"
full_details_df = get_full_details(csv_path)

#full_details_df = full_details_df[columns]
#full_details_df.to_csv("TerraNova_full_details.csv")
full_details_df.to_csv("PointGrey_full_details.csv")

print("done!")
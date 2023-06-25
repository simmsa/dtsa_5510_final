import json

import pandas as pd

fname = "2023_03_04-12_38_22_unique_denver_area.json"

f = open(fname)
data = json.load(f)

res_list = []


for key in data.keys():
    row = data[key]
    try:
        id = row["zpid"]
    except:
        id = row["detailUrl"]
    print(f"Processing row {id}")
    res = pd.json_normalize(row, sep="_")

    # Add Lot square footage
    sqft = 0
    acres = 0
    try:
        home_info = row["hdpData"]["homeInfo"]
        if home_info["lotAreaUnit"] == "sqft":
            sqft = home_info["lotAreaValue"]
            acres = sqft / 43560
        elif home_info["lotAreaUnit"] == "acres":
            acres = home_info["lotAreaValue"]
            sqft = acres * 43560

    except KeyError:
        continue

    res["lot_sqft"] = sqft

    if res.empty != True:
        res_list.append(res)

df = pd.concat(res_list)

df.to_csv(fname.replace("json", "csv"))

# Example json entry below
# "buildingId": "39.697666--104.89756",
# "lotId": 1001781042,
# "price": "From $389,900",
# "latLong": {
# "latitude": 39.697666,
# "longitude": -104.89756
# "minBeds": 2,
# "minBaths": 2,
# "minArea": 1394,
# "imgSrc": "https://photos.zillowstatic.com/fp/136789e94e344fb3c8433b3dbda2a86d-p_e.jpg",
# "hasImage": true,
# "isFeaturedListing": false,
# "unitCount": 2,
# "isBuilding": true,
# "address": "7865 E Mississippi Ave, Denver, CO",
# "variableData": {},
# "badgeInfo": null,
# "statusType": "FOR_SALE",
# "statusText": "For Rent",
# "listingType": "",
# "isFavorite": false,
# "detailUrl": "/b/7865-e-mississippi-ave-denver-co-5Xmzw5/",
# "has3DModel": false,
# "info3String": "https://photos.zillowstatic.com/fp/8dd1dd7033ea7ca8cc1a403da3dafc72-zillow_web_inf_14.jpg",
# "info1String": "MLS ID #5474025",
# "brokerName": "RE/MAX Masters Millennium",
# "hasAdditionalAttributions": true,
# "canSaveBuilding": false
# "buildingId": "39.704426--104.879654",
# "lotId": 1004771500,
# "price": "From $160,000",
# "latLong": {
# "latitude": 39.704426,
# "longitude": -104.879654
# "minBeds": 1,
# "minBaths": 1,
# "minArea": 855,
# "imgSrc": "https://photos.zillowstatic.com/fp/07cfb357dd83fca00401830210ef524f-p_e.jpg",
# "hasImage": true,
# "isFeaturedListing": false,
# "unitCount": 25,
# "isBuilding": true,
# "address": "725 S Alton Way, Denver, CO",
# "variableData": {
# "type": "3D_HOME",
# "text": "3D Tour"
# "badgeInfo": null,
# "statusType": "FOR_SALE",
# "statusText": "For Rent",
# "listingType": "",
# "isFavorite": false,
# "detailUrl": "/b/725-s-alton-way-denver-co-5YJQQq/",
# "has3DModel": true,
# "info3String": "https://photos.zillowstatic.com/fp/8dd1dd7033ea7ca8cc1a403da3dafc72-zillow_web_inf_14.jpg",
# "info1String": "MLS ID #3047963",
# "brokerName": "Dream Denver",
# "hasAdditionalAttributions": true,
# "canSaveBuilding": false
# },
# {
# "buildingId": "39.70111--104.89064",
# "lotId": null,
# "price": "From $624,900",
# "latLong": {
# "latitude": 39.70111,
# "longitude": -104.89064
# },
# "minBeds": 2,
# "minBaths": 3,
# "minArea": 1253,
# "imgSrc": "https://photos.zillowstatic.com/fp/5eba720c1608ffc8238134d0252f928f-p_e.jpg",
# "hasImage": true,
# "plid": "29309887",
# "isFeaturedListing": false,
# "unitCount": 8,
# "isBuilding": true,
# "address": "888 S Valentia St, Denver, CO",
# "variableData": {},
# "badgeInfo": null,
# "statusType": "FOR_SALE",
# "statusText": "For Rent",
# "listingType": "NEW_CONSTRUCTION",
# "isFavorite": false,
# "detailUrl": "/community/prelude-at-tava-waters/29309887_plid/",
# "has3DModel": false,
# "hasAdditionalAttributions": false,
# "canSaveBuilding": false,
# "communityName": "Prelude at TAVA Waters",
# "style": "Gated",
# "isCdpResult": true
# },
# {
# "zpid": "13046235",
# "price": "$390,000",
# "priceLabel": "$390K",
# "beds": 2,
# "baths": 2,
# "area": 1240,
# "latLong": {
# "latitude": 39.694836,
# "longitude": -104.87669
# },
# "statusType": "FOR_SALE",
# "statusText": "Condo for sale",
# "isFavorite": false,
# "isUserClaimingOwner": false,
# "isUserConfirmedClaim": false,
# "imgSrc": "https://photos.zillowstatic.com/fp/8fd1148203efde0f0a7f6da300cbeefe-p_e.jpg",
# "hasImage": true,
# "visited": false,
# "listingType": "",
# "variableData": null,
# "hdpData": {
# "homeInfo": {
# "zpid": 13046235,
# "zipcode": "80247",
# "city": "Denver",
# "state": "CO",
# "latitude": 39.694836,
# "longitude": -104.87669,
# "price": 390000,
# "bathrooms": 2,
# "bedrooms": 2,
# "livingArea": 1240,
# "homeType": "CONDO",
# "homeStatus": "FOR_SALE",
# "daysOnZillow": -1,
# "isFeatured": false,
# "shouldHighlight": false,
# "zestimate": 349400,
# "rentZestimate": 1800,
# "listing_sub_type": {
# "is_FSBA": true
# },
# "isUnmappable": false,
# "isPreforeclosureAuction": false,
# "homeStatusForHDP": "FOR_SALE",
# "priceForHDP": 390000,
# "isNonOwnerOccupied": true,
# "isPremierBuilder": false,
# "isZillowOwned": false,
# "currency": "USD",
# "country": "USA",
# "taxAssessedValue": 256800,
# "unit": "Apt 23",
# "lotAreaValue": 435.6,
# "lotAreaUnit": "sqft"
# }
# },
# "detailUrl": "/homedetails/9646-E-Kansas-Cir-APT-23-Denver-CO-80247/13046235_zpid/",
# "pgapt": "ForSale",
# "sgapt": "For Sale by Agent",
# "has3DModel": false,
# "hasVideo": false,
# "isHomeRec": false,
# "address": "--",
# "info3String": "https://photos.zillowstatic.com/fp/8dd1dd7033ea7ca8cc1a403da3dafc72-zillow_web_inf_14.jpg",
# "info1String": "MLS ID #8010408",
# "brokerName": "Keller Williams Preferred Realty",
# "hasAdditionalAttributions": true,
# "isFeaturedListing": false,
# "availabilityDate": null

# Not sure what these entries are but they look like this:
# {
# "buildingId": "40.00125--104.7432",
# "lotId": null,
# "price": "From $461,990",
# "latLong": {
# "latitude": 40.00125,
# "longitude": -104.7432
# },
# "minBeds": 3,
# "minBaths": 2,
# "minArea": 1291,
# "imgSrc": "https://photos.zillowstatic.com/fp/d42eeba7d67e7f1d3aa520b5fb08898f-p_e.jpg",
# "hasImage": true,
# "isFeaturedListing": false,
# "unitCount": 9,
# "isBuilding": true,
# "address": "1111 Sunrise Dr, Brighton, CO",
# "variableData": {},
# "badgeInfo": null,
# "statusType": "FOR_SALE",
# "statusText": "For Rent",
# "listingType": "",
# "isFavorite": false,
# "detailUrl": "/b/Brighton-CO/40.00125,-104.7432_ll/",
# "has3DModel": false,
# "hasAdditionalAttributions": false,
# "canSaveBuilding": false
# },

import json
import random
import time
from urllib.parse import urlencode

import httpx

with open("zip_codes.json", "r") as fp:
    zip_codes = json.load(fp)


def calculate_zip_code_center(zip_code_dict):
    lat_center = (zip_code_dict["north"] + zip_code_dict["south"]) / 2
    lng_center = (zip_code_dict["east"] + zip_code_dict["west"]) / 2
    return ",".join([str(lat_center), str(lng_center)])


unique_zip_code_centers = {}

for zip_code in zip_codes.keys():
    center = calculate_zip_code_center(zip_codes[zip_code])
    if center not in unique_zip_code_centers:
        unique_zip_code_centers[center] = [zip_code]
    else:
        unique_zip_code_centers[center].append(zip_code)

unique_zip_codes = []

for key in unique_zip_code_centers.keys():
    zip_code_list = unique_zip_code_centers[key]
    unique_zip_codes.append(zip_code_list[0])

BASE_HEADERS = {
    "accept-language": "en-us",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
}

zillow_ids = {}


def get_zillow__search_results(search_term, map_bounds):
    url = "https://www.zillow.com/search/GetSearchPageState.htm?"
    parameters = {
        "searchQueryState": {
            "pagination": {},
            "usersSearchTerm": search_term,
            "mapBounds": map_bounds,
        },
        "wants": {"cat1": ["mapResults"]},
        "requestId": 2,
    }
    response = httpx.get(url + urlencode(parameters), headers=BASE_HEADERS)
    try:
        results = response.json()["cat1"]["searchResults"]["mapResults"]
        for result in results:
            if "zpid" in result.keys():
                this_id = result["zpid"]
                if this_id not in zillow_ids:
                    zillow_ids[this_id] = result

        print(f"{search_term} has {len(results)} results!")
        return results
    except json.JSONDecodeError:
        print(f"Could not decode result from: {search_term}")
        print(response.headers)
        print(response.text)
        exit()


all_results = []

random.shuffle(unique_zip_codes)

iteration = 1
for zip_code in unique_zip_codes:
    results = get_zillow__search_results(zip_code, zip_codes[zip_code])
    time.sleep(random.random() * 10)
    if results != None:
        all_results.extend(results)
    percent_complete = (iteration / len(unique_zip_codes)) * 100.0
    iteration += 1
    print(f"{percent_complete:.2f}% complete")

print(f"found {len(all_results)} property results")
print(f"found {len(zillow_ids.keys())} unique property results")
now_str = time.strftime("%Y_%m_%d-%H_%M_%S")

# with open(f"{now_str}_jeffco.json", "w") as f:
#     json.dump(all_results, f)
# with open(f"{now_str}_denver_zillow_ids.json", "w") as f:
#     json.dump(zillow_ids, f)

unique_results = {}

for key in zillow_ids.keys():
    unique_results[key] = zillow_ids[key]

with open(f"{now_str}_unique_denver_area.json", "w") as f:
    json.dump(unique_results, f)

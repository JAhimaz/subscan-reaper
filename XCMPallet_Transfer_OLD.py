import requests
import time
from datetime import datetime

# Polkadot
url = "https://polkadot.webapi.subscan.io/api/v2/scan/extrinsics"
extrinsic_url = "https://polkadot.webapi.subscan.io/api/scan/extrinsic"
chain = "Polkadot"
block_range = "14509978-14949703"
decimals = 10

# ==========================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

page_number = 0
number_of_pages = 0
extrinsic_indexes = []


def get_asset_amount(data):
    asset_version = list(data[2]["value"].keys())[0]
    asset_data = data[2]["value"][asset_version][0]
    if "ConcreteFungible" in asset_data:
        return asset_data["ConcreteFungible"]["amount"]
    elif "fun" in asset_data:
        return asset_data["fun"]["Fungible"]
    else:
        return None


def get_parachain(data):
    location_version = list(data[0]["value"].keys())[0]
    location_data = data[0]["value"][location_version]
    if location_version == "V0":
        return location_data["X1"]["Parachain"]
    elif location_version == "V1":
        return location_data["interior"]["X1"]["Parachain"]
    else:
        return None


# create an empty file to write the data to
with open("./XCM_Transfers/" + chain + "_XCM_transfer.txt", "w") as f:
    f.write("")
    f.close()

# if the file is not empty, clear it
with open("./XCM_Transfers/" + chain + "_XCM_transfer.txt", "r") as f:
    if f.read() != "":
        f.close()
        with open("./XCM_Transfers/" + chain + "_XCM_transfer.txt", "w") as f:
            f.write("")
            f.close()


# loop 15 times (Gets last 1500 transactions)

print("Getting XCM Transfer Data from " + chain + " Network...")

for i in range(15):
    response = requests.post(url, headers=headers, json={
        "row": 100,
        "page": page_number,
        "signed": "signed",
        "address": "",
        "module": "xcmpallet",
        "call": "reserve_transfer_assets",
        "success": True,
        "block_range": block_range
    })

    # Check if response is valid
    if response.status_code == 200:
        data = response.json()

        if data["data"]["extrinsics"] is None:
            break

        # Check if there are extrinsics
        if data["data"]["extrinsics"] is not None and len(data["data"]["extrinsics"]) > 0:
            # For each extrinsic
            for extrinsic in data["data"]["extrinsics"]:
                # Push the individual data as an object to the extrinsics array
                extrinsic_indexes.append({
                    "id": extrinsic["extrinsic_index"],
                })
    else:
        print("Error: " + str(response.status_code))

    # Increment the page number
    page_number += 1
    print("[Extrinsic_Index] Page: " + str(page_number))

    # This is to prevent the API from blocking us
    time.sleep(1)

# Get the data for each extrinsic
for extrinsic_index in extrinsic_indexes:
    extrinsic_response = requests.post(extrinsic_url, headers=headers, json={
        "extrinsic_index": str(extrinsic_index["id"]),
        "events_limit": 10,
        "only_extrinsic_event": True
    })
    if extrinsic_response.status_code == 200:
        extrinsic_data = extrinsic_response.json()

        version = next(iter(extrinsic_data["data"]["params"][2]["value"]))

        # open balances_transfer.txt and append the data to it in a csv format
        with open("./XCM_Transfers/" + chain + "_XCM_transfer.txt", "a") as f:
            f.write(str(extrinsic_index["id"]) +
                    ", " + str(extrinsic_data["data"]["account_id"]) +
                    ", " + str(extrinsic_data["data"]["extrinsic_hash"]) +
                    ", " + str(extrinsic_data["data"]["block_num"]) +
                    ", " + str(round(int(get_asset_amount(extrinsic_data["data"]["params"])) / (10 ** decimals), 5)) +
                    # ", " + str(round(int(extrinsic_data["data"]["params"][2]["value"][key][0]["ConcreteFungible"]["amount"]) / (10 ** decimals), 5)) +
                    ", " + str(get_parachain(extrinsic_data["data"]["params"])) +
                    ", " + datetime.fromtimestamp(int(extrinsic_data["data"]["block_timestamp"])).strftime('%Y-%m-%d %H:%M:%S') +
                    ", " + str(extrinsic_data["data"]["call_module"]) +
                    ", " + str(extrinsic_data["data"]["call_module_function"]) +
                    "\n")
            f.close()
    else:
        print("Error: " + str(extrinsic_response.status_code) +
              " " + str(extrinsic_index["id"]))
    # print how many extrinsics have been processed
    print("[Extrinsic_Data] " + str(extrinsic_indexes.index(extrinsic_index) + 1) +
          " of " + str(len(extrinsic_indexes)))

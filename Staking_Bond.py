import requests
import time
from datetime import datetime

# Select the network you want to scan

# Polkadot
# url = "https://polkadot.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://polkadot.webapi.subscan.io/api/scan/extrinsic"
# chain = "Polkadot"
# block_range = ""
# decimals = 10

# Kusama
# url = "https://kusama.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://kusama.webapi.subscan.io/api/scan/extrinsic"
# chain = "Kusama"
# block_range = "16911800-17343355"
# decimals = 12

# Aleph_Zero
url = "https://alephzero.webapi.subscan.io/api/v2/scan/extrinsics"
extrinsic_url = "https://alephzero.webapi.subscan.io/api/scan/extrinsic"
chain = "Aleph_Zero"
block_range = "41381050-44033150"
decimals = 9

# ==========================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

page_number = 0
number_of_pages = 0
extrinsic_indexes = []

# create an empty file to write the data to
with open("./Staking_Bond/" + chain + "_staking_bond.txt", "w") as f:
    f.write("")
    f.close()

# if the file is not empty, clear it
with open("./Staking_Bond/" + chain + "_staking_bond.txt", "r") as f:
    if f.read() != "":
        f.close()
        with open("./Staking_Bond/" + chain + "_staking_bond.txt", "w") as f:
            f.write("")
            f.close()


# loop 15 times (Gets last 1500 transactions)
for i in range(15):
    response = requests.post(url, headers=headers, json={
        "row": 100,
        "page": page_number,
        "signed": "signed",
        "module": "staking",
        "call": "bond",
        "no_params": True,
        "block_range": "16911800-17343355", "success": True
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

for extrinsic_index in extrinsic_indexes:
    extrinsic_response = requests.post(extrinsic_url, headers=headers, json={
        "extrinsic_index": str(extrinsic_index["id"]),
        "events_limit": 10,
        "only_extrinsic_event": True
    })
    if extrinsic_response.status_code == 200:
        extrinsic_data = extrinsic_response.json()

        # open balances_transfer.txt and append the data to it in a csv format
        with open("./Staking_Bond/" + chain + "_staking_bond.txt", "a") as f:
            f.write(str(extrinsic_index["id"]) +
                    ", " + str(extrinsic_data["data"]["account_id"]) +
                    ", " + str(extrinsic_data["data"]["extrinsic_hash"]) +
                    ", " + str(extrinsic_data["data"]["block_num"]) +
                    ", " + str(round(int(extrinsic_data["data"]["params"][1]["value"]) / (10 ** decimals), 5)) +
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

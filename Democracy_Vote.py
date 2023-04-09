import requests
import time
from datetime import datetime

# Select the network you want to scan

# Polkadot
url = "https://polkadot.webapi.subscan.io/api/v2/scan/extrinsics"
extrinsic_url = "https://polkadot.webapi.subscan.io/api/scan/extrinsic"
chain = "Polkadot"
block_range = "14524371-14964096"
decimals = 10

# Kusama
# url = "https://kusama.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://kusama.webapi.subscan.io/api/scan/extrinsic"
# chain = "Kusama"
# block_range = ""
# decimals = 12

# Acala
# url = "https://acala.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://acala.webapi.subscan.io/api/scan/extrinsic"
# chain = "Acala"
# block_range = "3083743-3292181"
# decimals = 12

# Karura
# url = "https://karura.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://karura.webapi.subscan.io/api/scan/extrinsic"
# chain = "Karura"
# block_range = "3841263-4053927"
# decimals = 12

# Moonriver
# url = "https://moonriver.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://moonriver.webapi.subscan.io/api/scan/extrinsic"
# chain = "Moonriver"
# block_range = "3758319-3968646"
# decimals = 18

# Moonbeam
# url = "https://moonbeam.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://moonbeam.webapi.subscan.io/api/scan/extrinsic"
# chain = "Moonbeam"
# block_range = "3083964-3287757"
# decimals = 18

# Aleph_Zero
# url = "https://alephzero.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://alephzero.webapi.subscan.io/api/scan/extrinsic"
# chain = "Aleph_Zero"
# block_range = "41381050-44033150"
# decimals = 9

# Parallel
# url = "https://parallel.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://parallel.webapi.subscan.io/api/scan/extrinsic"
# chain = "Parallel"
# block_range = "3026973-3239239"
# decimals = 12

# AStar
# url = "https://astar.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://astar.webapi.subscan.io/api/scan/extrinsic"
# chain = "AStar"
# block_range = "3079388-3291694"
# decimals = 18

# Bifrost
# url = "https://bifrost.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://bifrost.webapi.subscan.io/api/scan/extrinsic"
# chain = "Bifrost"
# block_range = "1877693-2088466"
# decimals = 12

# Centrifuge
# url = "https://centrifuge.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://centrifuge.webapi.subscan.io/api/scan/extrinsic"
# chain = "Centrifuge"
# block_range = "2463846-2678056"
# decimals = 18

# Phala
# url = "https://phala.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://phala.webapi.subscan.io/api/scan/extrinsic"
# chain = "Phala"
# block_range = "2044618-2260069"
# decimals = 12

# Basilisk
# url = "https://basilisk.webapi.subscan.io/api/v2/scan/extrinsics"
# extrinsic_url = "https://basilisk.webapi.subscan.io/api/scan/extrinsic"
# chain = "Basilisk"
# block_range = "2893350-3103249"
# decimals = 12

# Mangata X
# url =
# extrinsic_url =
# chain = "Mangata X"
# block_range = ""
# decimals = 12


# ==========================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

page_number = 0
number_of_pages = 0
extrinsic_indexes = []

# create an empty file to write the data to
with open("./Democracy_Vote/" + chain + "_democracy_vote.csv", "w") as f:
    f.write("")
    f.close()

# if the file is not empty, clear it
with open("./Democracy_Vote/" + chain + "_democracy_vote.csv", "r") as f:
    if f.read() != "":
        f.close()
        with open("./Democracy_Vote/" + chain + "_democracy_vote.csv", "w") as f:
            f.write("")
            f.close()


# loop 15 times (Gets last 1500 transactions)

print("Getting Balances Transfer Data from " + chain + " Network...")

for i in range(15):
    response = requests.post(url, headers=headers, json={
        "row": 100,
        "page": page_number,
        "signed": "signed",
        "address": "",
        "module": "democracy",
        "call": "vote",
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

for extrinsic_index in extrinsic_indexes:
    extrinsic_response = requests.post(extrinsic_url, headers=headers, json={
        "extrinsic_index": str(extrinsic_index["id"]),
        "events_limit": 10,
        "only_extrinsic_event": True
    })
    if extrinsic_response.status_code == 200:
        extrinsic_data = extrinsic_response.json()

        # open democracy_vote.csv and append the data to it in a csv format
        with open("./Democracy_Vote/" + chain + "_democracy_vote.csv", "a") as f:
            f.write(str(extrinsic_index["id"]) +
                    ", " + str(extrinsic_data["data"]["account_id"]) +
                    ", " + str(extrinsic_data["data"]["extrinsic_hash"]) +
                    ", " + str(extrinsic_data["data"]["block_num"]) +
                    ", " + "0" +
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

    # time.sleep(1)

import requests
import time
from datetime import datetime, date

blockchain = "Moonbeam"
# Acala
if (blockchain == "Acala"):
    url = "https://acala.webapi.subscan.io/api/v2/scan/transfers"
    chain = "Acala"
    block_ranges = ["3306444-3342109", "3285060-3306444",
                    "3263691-3285060", "3235236-3263691"]
    decimals = 12

# Karura
if (blockchain == "Karura"):
    url = "https://karura.webapi.subscan.io/api/v2/scan/transfers"
    chain = "Karura"
    block_ranges = ["4025368-4102682", "3997178-4025368"]
    decimals = 12

# Moonriver
if (blockchain == "Moonriver"):
    url = "https://moonriver.webapi.subscan.io/api/v2/scan/transfers"
    chain = "Moonriver"
    block_ranges = ["3988743-4016705",
                    "3967974-3988743", "3947316-3967974", "3933343-3947316", "3912338-3933343"]
    decimals = 18

# Moonbeam
# Come back to this later 😓😓😓
if (blockchain == "Moonbeam"):
    url = "https://moonbeam.webapi.subscan.io/api/v2/scan/transfers"
    chain = "Moonbeam"
    min_block = 3231630
    max_block = 3334044
    block_tick_rate = 100
    decimals = 18

# Aleph_Zero
if (blockchain == "Aleph_Zero"):
    url = "https://alephzero.webapi.subscan.io/api/v2/scan/transfers"
    chain = "Aleph_Zero"
    block_ranges = []
    min_block = 43353524
    max_block = 44628259
    block_tick_rate = 10000
    decimals = 9

# Parallel
if (blockchain == "Parallel"):
    url = "https://parallel.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://parallel.webapi.subscan.io/api/scan/extrinsic"
    chain = "Parallel"
    block_ranges = []
    decimals = 12

# AStar
if (blockchain == "AStar"):
    url = "https://astar.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://astar.webapi.subscan.io/api/scan/extrinsic"
    chain = "AStar"
    block_ranges = []
    decimals = 18

# Bifrost
if (blockchain == "Bifrost"):
    url = "https://bifrost.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://bifrost.webapi.subscan.io/api/scan/extrinsic"
    chain = "Bifrost"
    block_ranges = []
    decimals = 12

# Centrifuge
if (blockchain == "Centrifuge"):
    url = "https://centrifuge.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://centrifuge.webapi.subscan.io/api/scan/extrinsic"
    chain = "Centrifuge"
    block_ranges = []
    decimals = 18

# Phala
if (blockchain == "Phala"):
    url = "https://phala.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://phala.webapi.subscan.io/api/scan/extrinsic"
    chain = "Phala"
    block_ranges = []
    decimals = 12

# Basilisk
if (blockchain == "Basilisk"):
    url = "https://basilisk.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://basilisk.webapi.subscan.io/api/scan/extrinsic"
    chain = "Basilisk"
    block_ranges = []
    decimals = 12

# Mangata X
    # url =
    # extrinsic_url =
    # chain = "Mangata X"
    # block_ranges = []
    # decimals = 12


# ==========================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

number_of_pages = 0
extrinsic_indexes = []


# create an empty file to write the data to
with open("./Balance_Transfers/" + chain + "_transfers.csv", "w") as f:
    f.write("")
    f.close()

# if the file is not empty, clear it
with open("./Balance_Transfers/" + chain + "_transfers.csv", "r") as f:
    if f.read() != "":
        f.close()
        with open("./Balance_Transfers/" + chain + "_transfers.csv", "w") as f:
            f.write("")
            f.close()


print("Getting Transfer Data from " + chain + " Network...")

while (True):
    ranged_block = min_block + block_tick_rate
    if (ranged_block > max_block):
        ranged_block = max_block

    print("Getting data for block range: " +
          str(min_block) + "-" + str(ranged_block))
    page_number = 0

    for x in range(999):
        response = requests.post(url, headers=headers, json={
            "row": 100,
            "page": page_number,
            "direction": "all",
            "include_total": True,
            "success": True,
            "min_amount": "",
            "max_amount": "",
            "currency": "usd",
            "from_block": min_block,
            "to_block": ranged_block,
            "block_range": str(min_block) + "-" + str(ranged_block),
        })

        # Check if response is valid
        if response.status_code == 200:
            try:
                data = response.json()

                if data["data"]["transfers"] is None:
                    break

                # Check if there are extrinsics
                if data["data"]["transfers"] is not None and len(data["data"]["transfers"]) > 0:
                    # For each extrinsic
                    for transfer in data["data"]["transfers"]:

                        dateTime = datetime.fromtimestamp(
                            int(transfer["block_timestamp"])).strftime('%Y-%m-%d %H:%M:%S')

                        date = dateTime.split(" ")[0]
                        time = dateTime.split(" ")[1]

                        with open("./Balance_Transfers/" + chain + "_transfers.csv", "a") as f:
                            f.write(date +
                                    ", " + time +
                                    ", " + str(transfer["extrinsic_index"]) +
                                    ", " + str(transfer["block_num"]) +
                                    ", " + str(transfer["hash"]) +
                                    ", " + str(transfer["from"]) +
                                    ", " + str(transfer["to"]) +
                                    ", " + str(transfer["amount"]) +
                                    ", " + str(transfer["asset_symbol"]) +
                                    "\n")
                            f.close()

                        # print number of extrinsics done in data["data"]["transfers"]
                        # print("Transfer " + str(data["data"]["transfers"].index(
                        #     transfer) + 1) + " of " + str(len(data["data"]["transfers"])))
            except:
                print("Error: " + str(response.status_code))

        else:
            print("Error: " + str(response.status_code))

        # Increment the page number
        print("[" + str(min_block) + "-" + str(ranged_block) + "] Page " +
              str(page_number) + " completed.")

        page_number += 1

    min_block += block_tick_rate
    if (ranged_block == max_block):
        break

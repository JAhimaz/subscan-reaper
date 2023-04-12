# https://polkadot.webapi.subscan.io/api/scan/xcm/list
# {
#   "row":100,
#   "page":0,
#   "address":"",
#   "protocol":null,
#   "origin_para_id":null,
#   "dest_para_id":null,
#   "status":null,
#   "message_type":"transfer"
# }

import requests
import time
from datetime import datetime

# Select the network you want to scan

# Polkadot
# url = "https://polkadot.webapi.subscan.io/api/scan/xcm/list"
# chain = "Polkadot"
# block_range = "14524371-14953024"
# origin_para_id = 0

# Kusama
url = "https://kusama.webapi.subscan.io/api/scan/xcm/list"
chain = "Kusama"
block_range = "16911800-17356300"
origin_para_id = 0

# ===================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

page_number = 0
number_of_pages = 0
transfers = []


def get_amount_asset(instructions):
    version = next(iter(instructions))
    transfer_type = next(iter(instructions[version][0]))

    amounts = []

    for transfer in transfer_type:
        amounts.append(transfer["fun"]["Fungible"])

    return amounts


def is_from_chain(chainId):
    if (chainId == origin_para_id):
        return True
    else:
        return False


with open("./XCM_Transfers/" + chain + "_XCM_transfer.csv", "w") as f:
    f.write("")
    f.close()

# if the file is not empty, clear it
with open("./XCM_Transfers/" + chain + "_XCM_transfer.csv", "r") as f:
    if f.read() != "":
        f.close()
        with open("./XCM_Transfers/" + chain + "_XCM_transfer.csv", "w") as f:
            f.write("")
            f.close()

print("Getting XCM Transfer data from " + chain + " Network...")

for i in range(15):
    print("Fetching XCM transfers from page " + str(page_number))
    response = requests.post(url, headers=headers, json={
        "row": 100,
        "page": page_number,
        "address": "",
        "message_type": "transfer"
    })

    # Check if response is valid
    if response.status_code == 200:
        data = response.json()
        for transfer in data["data"]["list"]:
            transfers.append(transfer)
    else:
        print("Error: " + str(response.status_code) +
              " on Page " + str(page_number))
        break

    page_number += 1

for transfer in transfers:

    assets = []

    for asset in transfer["assets"]:
        amount = int(asset["amount"])
        # if asset does not have decimals or symbol, add it as unknown
        if (("decimals" not in asset) or ("symbol" not in asset)):
            assets.append(str(amount) + " Unknown")
            continue
        amount = round(int(asset["amount"]) /
                       (10 ** int(asset["decimals"])), 5)
        assets.append(str(amount) + " " + str(asset["symbol"]))

    assetsInText = ", ".join(assets)

    dateTime = datetime.fromtimestamp(
        int(transfer["origin_block_timestamp"])).strftime('%Y-%m-%d %H:%M:%S')

    date = dateTime.split(" ")[0]
    time = dateTime.split(" ")[1]

    with open("./XCM_Transfers/" + chain + "_XCM_transfer.csv", "a") as f:
        f.write(date +
                ", " + time +
                ", " + str(transfer["message_hash"]) +
                ", " + str(transfer["extrinsic_index"]) +
                ", " + str(transfer["from_account_id"]) +
                ", " + str(transfer["origin_para_id"]) +
                ", " + str(transfer["to_account_id"]) +
                ", " + str(transfer["dest_para_id"]) +
                ", " + str(is_from_chain(transfer["origin_para_id"])) +
                ", " + str(transfer["protocol"]) +
                ", " + str(transfer["unique_id"]) +
                ", " + assetsInText +
                "\n")
        f.close()

    # print how many extrinsics have been processed
    print("[Extrinsic_Data] " + str(transfers.index(transfer) + 1) +
          " of " + str(len(transfers)))

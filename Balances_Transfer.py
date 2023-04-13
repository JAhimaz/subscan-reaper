import requests
import time
from datetime import datetime, date

blockchain = "Polkadot"
continue_mode = False
continue_from_line = 14014

module_call = "transfer_keep_alive"
# module_call = "transfer"

# Select the network you want to scan

# Polkadot
if (blockchain == "Polkadot"):
    url = "https://polkadot.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://polkadot.webapi.subscan.io/api/scan/extrinsic"
    chain = "Polkadot"
    block_ranges = ["15036043-15050439", "15021645-15036043",
                    "15007248-15021645", "14992873-15007248",
                    "14978480-14992873", "14964096-14978480",
                    "14949703-14964096", "14935309-14949703",
                    "14920911-14935309", "14906514-14920911",
                    "14892125-14906514", "14877737-14892125",
                    "14863351-14877737", "14848961-14863351",
                    "14834575-14848961"]
    decimals = 10

# Kusama
if (blockchain == "Kusama"):
    url = "https://kusama.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://kusama.webapi.subscan.io/api/scan/extrinsic"
    chain = "Kusama"
    block_ranges = ["17427957-17442278", "17413641-17427957",
                    "17399311-17413641", "17384985-17399311",
                    "17370661-17384985", "17356300-17370661",
                    "17341969-17356300", "17327662-17341969",
                    "17313333-17327662", "17299041-17313333",
                    "17284755-17299041", "17270511-17284755",
                    "17256217-17270511", "17241927-17256217",
                    "17227647-17241927"]
    decimals = 12

# Acala
if (blockchain == "Acala"):
    url = "https://acala.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://acala.webapi.subscan.io/api/scan/extrinsic"
    chain = "Acala"
    block_ranges = []
    decimals = 12

# Karura
if (blockchain == "Karura"):
    url = "https://karura.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://karura.webapi.subscan.io/api/scan/extrinsic"
    chain = "Karura"
    block_ranges = []
    decimals = 12

# Moonriver
if (blockchain == "Moonriver"):
    url = "https://moonriver.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://moonriver.webapi.subscan.io/api/scan/extrinsic"
    chain = "Moonriver"
    block_ranges = []
    decimals = 18

# Moonbeam
if (blockchain == "Moonbeam"):
    url = "https://moonbeam.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://moonbeam.webapi.subscan.io/api/scan/extrinsic"
    chain = "Moonbeam"
    block_ranges = []
    decimals = 18

# Aleph_Zero
if (blockchain == "Aleph_Zero"):
    url = "https://alephzero.webapi.subscan.io/api/v2/scan/extrinsics"
    extrinsic_url = "https://alephzero.webapi.subscan.io/api/scan/extrinsic"
    chain = "Aleph_Zero"
    block_ranges = []
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

if (not continue_mode):
    # create an empty file to write the data to
    with open("./Balance_Transfers/" + chain + "_balances_" + module_call + ".csv", "w") as f:
        f.write("")
        f.close()

    # if the file is not empty, clear it
    with open("./Balance_Transfers/" + chain + "_balances_" + module_call + ".csv", "r") as f:
        if f.read() != "":
            f.close()
            with open("./Balance_Transfers/" + chain + "_balances_" + module_call + ".csv", "w") as f:
                f.write("")
                f.close()

    # create an empty file to write the data to
    with open("./Temp/" + chain + "_" + module_call + "_temp_extrinsic_ids_" + date.today().strftime("%d_%m_%Y") + ".csv", "w") as f:
        f.write("")
        f.close()

    # create an empty file to write the data to for total amount per day

    with open("./Balance_Transfers/" + chain + "_balances_" + module_call + "_total_per_day.csv", "w") as f:
        f.write("")
        f.close()

    # if the file is not empty, clear it
    with open("./Balance_Transfers/" + chain + "_balances_" + module_call + "_total_per_day.csv", "r") as f:
        if f.read() != "":
            f.close()
            with open("./Balance_Transfers/" + chain + "_balances_" + module_call + "_total_per_day.csv", "w") as f:
                f.write("")
                f.close()

if (continue_mode):
    print("Continuing " + module_call + " from " + chain +
          " Network from " + str(continue_from_line) + " line...")

    # get all extrinsic indexes from the temp file but start from line number 14006
    with open("./Temp/" + chain + "_" + module_call + "_temp_extrinsic_ids_" + date.today().strftime("%d_%m_%Y") + ".csv", "r") as f:
        lines = f.readlines()[continue_from_line:]
        # remove \n from the end of each line
        lines = [line.rstrip() for line in lines]
        for line in lines:
            extrinsic_indexes.append({
                "id": line.split(",")[0],
            })
        f.close()

print("Getting Balances " + module_call +
      " Data from " + chain + " Network...")

if (not continue_mode):
    for block_range in block_ranges:
        print("Getting data for block range: " + block_range)
        total_per_day = 0  # reset total per day
        page_number = 0

        for x in range(999):
            response = requests.post(url, headers=headers, json={
                "row": 100,
                "page": page_number,
                "signed": "signed",
                "address": "",
                "module": "balances",
                "call": module_call,
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

                        with open("./Temp/" + chain + "_" + module_call + "_temp_extrinsic_ids_" + date.today().strftime("%d_%m_%Y") + ".csv", "a") as f:
                            f.write(str(extrinsic["extrinsic_index"]) + "\n")
                            f.close()

                total_per_day += len(data["data"]["extrinsics"])
            else:
                print("Error: " + str(response.status_code))

            # Increment the page number
            print("[" + block_range + "] Page " +
                  str(page_number) + " completed.")
            page_number += 1
            time.sleep(0.5)

        # open balances_transfer_total_per_day.csv and append the data to it in a csv format
        with open("./Balance_Transfers/" + chain + "_balances_" + module_call + "_total_per_day.csv", "a") as f:
            f.write(str(total_per_day) +
                    "," + block_range.split("-")[0] +
                    "," + block_range.split("-")[1] +
                    "\n")

for extrinsic_index in extrinsic_indexes:
    print("[Extrinsic_Data " + str(extrinsic_index["id"]) + "] " +
          str(extrinsic_indexes.index(extrinsic_index) + 1) + " of " + str(len(extrinsic_indexes)))
    extrinsic_response = requests.post(extrinsic_url, headers=headers, json={
        "extrinsic_index": str(extrinsic_index["id"]),
        "events_limit": 10,
        "only_extrinsic_event": True
    })
    if extrinsic_response.status_code == 200:
        try:
            extrinsic_data = extrinsic_response.json()

            dateTime = datetime.fromtimestamp(
                int(extrinsic_data["data"]["block_timestamp"])).strftime('%Y-%m-%d %H:%M:%S')

            date = dateTime.split(" ")[0]
            time = dateTime.split(" ")[1]

            # open balances_transfer.csv and append the data to it in a csv format

            with open("./Balance_Transfers/" + chain + "_balances_" + module_call + ".csv", "a") as f:
                f.write(date +
                        ", " + time +
                        ", " + str(extrinsic_index["id"]) +
                        ", " + str(extrinsic_data["data"]["block_num"]) +
                        ", " + str(extrinsic_data["data"]["extrinsic_hash"]) +
                        ", " + str(extrinsic_data["data"]["account_id"]) +
                        ", " + str(extrinsic_data["data"]["params"][0]["value"]["Id"]) +
                        ", " + str(round(float(extrinsic_data["data"]["params"][1]["value"]) / (10 ** decimals), 5)) +
                        ", " + str(extrinsic_data["data"]["call_module"]) +
                        ", " + str(extrinsic_data["data"]["call_module_function"]) +
                        "\n")
                f.close()
        except Exception as e:
            print("Error: " + str(extrinsic_index["id"]))
            print(e)

    else:
        print("Error: " + str(extrinsic_response.status_code) +
              " " + str(extrinsic_index["id"]))
    # print how many extrinsics have been processed

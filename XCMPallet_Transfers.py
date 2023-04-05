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
# decimals = 10

# ===================================

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

page_number = 0
number_of_pages = 0
extrinsic_indexes = []


def get_amount_asset(instructions):
    version = next(iter(instructions))
    transfer_type = next(iter(instructions[version][0]))

    amounts = []

    for transfer in transfer_type:
        amounts.append(transfer["fun"]["Fungible"])

    return amounts

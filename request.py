import os
import requests
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

load_dotenv()


def main():
    FIRST_POS_BLOCK = 15537394
    url = os.getenv("ETH_MAINNET_URL")

    most_recent_block = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 83,
    }

    blocknumber = requests.post(url, json=most_recent_block).json()

    length = int(blocknumber["result"], 16) - FIRST_POS_BLOCK
    block = FIRST_POS_BLOCK
    prevrandao_values = []

    for idx in range(length):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex(block), True],
            "id": 1,
        }
        response = requests.post(url, json=payload).json()
        prevrandao = response["result"]["mixHash"]
        prevrandao_values.append(int(prevrandao, 0))
        block += 1

    np.savetxt("prevrandao_values.csv", prevrandao_values, delimiter=",")
    plt.hist(np.array(prevrandao_values, dtype=float) / 10**77, bins=75)
    plt.gca().set(
        title="RANDAO Histogram",
        ylabel="Frequency",
        xlabel="Normalised (10**77) RANDAO Values",
    )
    plt.show()


if __name__ == "__main__":
    main()

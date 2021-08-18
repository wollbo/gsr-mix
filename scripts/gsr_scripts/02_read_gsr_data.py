#!/usr/bin/python3
from brownie import GSRConsumer

# round_id, answer, started_at, updated_at, answered_in
def main():
    price_feed_contract = GSRConsumer[-1]
    print(f"Reading data from {price_feed_contract.address}")
    _, price_au, _, _, _ = price_feed_contract.get_latest_xau()
    _, price_ag, _, _, _ = price_feed_contract.get_latest_xag()
    print(price_au/price_ag)


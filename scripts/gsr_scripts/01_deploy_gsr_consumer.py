#!/usr/bin/python3
from brownie import GSRConsumer, config, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
)


def deploy_gsr_consumer():
    account = get_account()
    xau_price_feed_address = '0xc8fb5684f2707C82f28595dEaC017Bfdf44EE9c5'  # KOVAN
    xag_price_feed_address = '0x4594051c018Ac096222b5077C3351d523F93a963'
    gsr_consumer = GSRConsumer.deploy(
        xau_price_feed_address,
        xag_price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"GSR Consumer deployed to {gsr_consumer.address}")
    return gsr_consumer


def main():
    deploy_gsr_consumer()
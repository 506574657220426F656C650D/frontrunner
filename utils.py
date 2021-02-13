import json
from pprint import pprint
import sys
from web3 import Web3, middleware
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy
from config import DefaultConfig
from datetime import datetime
from data_models import FrontRunnerData
import time
from uniswap import Uniswap
import requests


def value_based_gas_price_strategy(web3: Web3, transaction_params=None):
    # https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken
    base_url = "https://api.etherscan.io/api"

    get_params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": DefaultConfig.ether_scan_api_key

    }

    response = requests.get(
        url=base_url,
        params=get_params).text

    fast = json.loads(response)["result"]["FastGasPrice"]
    faster = round(int(fast) * 1.1, 0)
    return Web3.toWei(int(faster), 'gwei')


def is_uni_swap_tx(front_runner_data: FrontRunnerData) -> bool:
    """
    Check if the tx has uni swap router as to addy
    todo: Figure out if we can add this stuff to the filter
    """
    return str(front_runner_data.tx['to']).lower() == DefaultConfig.uniswap_router_address.lower()


def is_whitelisted_trade(front_runner_data: FrontRunnerData) -> bool:
    """
    figure out if the method is swapExactETHForTokens
    and the coin is in the allowed coins list
    """
    # return 'swapExactETHForTokens' in str(front_runner_data.input_decoded[0])
    return 'swapExactETHForTokens' in str(front_runner_data.input_decoded[0]) \
           and front_runner_data.input_decoded[1]['path'][1] in DefaultConfig.coins_list


def get_ether_value_villain_order(front_runner_data: FrontRunnerData, w3: Web3):
    value_villain_tx = int(w3.toJSON(front_runner_data.tx['value']))
    return w3.fromWei(value_villain_tx, "ether")


def print_debug_info(front_runner_data: FrontRunnerData, w3: Web3):
    print()
    print("-------------------------------------------------")
    print(datetime.now())
    print("https://etherscan.io/tx/" + json.loads(w3.toJSON(front_runner_data.tx['hash'])))
    print("coin: ", front_runner_data.input_decoded[1]['path'][1])
    print("value: ", get_ether_value_villain_order(front_runner_data, w3), " ether")


def print_order_info(front_runner_data: FrontRunnerData, w3: Web3, uniswap_wrapper: Uniswap):
    print('\a', '\a')
    print("slippage: ", round(get_slippage_percentage(front_runner_data, w3, uniswap_wrapper), 2))
    print("public amountOutMin: ", round(w3.fromWei(front_runner_data.public_amount_min, "ether"), 4))
    print("villain amountOutMin: ", round(w3.fromWei(front_runner_data.input_decoded[1]['amountOutMin'], "ether"), 4))
    print(":: BUYSIGNAL :: ", front_runner_data.trade_amount)
    print()


def get_slippage_percentage(front_runner_data: FrontRunnerData, w3: Web3, uniswap_wrapper: Uniswap):
    value_villain_tx = int(w3.toJSON(front_runner_data.tx['value']))
    coin_villain = front_runner_data.input_decoded[1]['path'][1]
    front_runner_data.public_amount_min = uniswap_wrapper.get_eth_token_input_price(coin_villain, value_villain_tx)
    front_runner_data.amount_min = front_runner_data.input_decoded[1]['amountOutMin']
    front_runner_data.trade_amount = front_runner_data.public_amount_min - front_runner_data.amount_min

    print_debug_info(front_runner_data, w3)

    return (front_runner_data.public_amount_min - front_runner_data.amount_min) / front_runner_data.amount_min * 100


def buy(front_runner_data: FrontRunnerData, trade_amount: int, uniswap_wrapper: Uniswap, w3: Web3):
    print("buying ", trade_amount, " of ", front_runner_data.input_decoded[1]['path'][1])
    tx = uniswap_wrapper.make_trade(
        DefaultConfig.eth,
        front_runner_data.input_decoded[1]['path'][1],
        trade_amount
    )
    print("https://etherscan.io/tx/" + json.loads(w3.toJSON(tx)))


def sell(front_runner_data: FrontRunnerData, trade_amount: int, uniswap_wrapper: Uniswap, w3: Web3):
    coin = Web3.toChecksumAddress(front_runner_data.input_decoded[1]['path'][1])
    for i in range(1000):
        try:
            trade_amount = get_balance_by_token(coin)
            print("selling ", trade_amount, " of ", coin)
            tx = uniswap_wrapper.make_trade(
                coin,
                DefaultConfig.eth,
                int(trade_amount)
            )
            print("https://etherscan.io/tx/" + str(json.loads(w3.toJSON(tx))))
        except Exception as e:
            print(e)
            time.sleep(1)
        else:
            sys.exit()
            break


def get_balance_by_token(token):
    base_url = "https://api.etherscan.io/api"

    get_params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": token,
        "address": DefaultConfig.address,
        "tag": "latest",
        "apikey": DefaultConfig.ether_scan_api_key

    }

    response = requests.get(
        url=base_url,
        params=get_params).text
    print(response)
    return json.loads(response)["result"]

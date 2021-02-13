from uniswap import Uniswap
import traceback

import asyncio
import rlp
import asyncio
import json
from config import DefaultConfig
import time
from web3 import Web3, middleware
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy
from data_models import FrontRunnerData
from utils import (
    is_uni_swap_tx,
    is_whitelisted_trade,
    get_ether_value_villain_order,
    print_order_info,
    get_slippage_percentage,
    buy,
    sell,
    value_based_gas_price_strategy
)

pause = False
count = 0
front_runner_data = FrontRunnerData()
w3 = Web3(Web3.IPCProvider(DefaultConfig.ipc_provider))

# time_based_gas_price_strategy = construct_time_based_gas_price_strategy(
#     max_wait_seconds=30,
#     sample_size=50,
#     probability=99)
#
# w3.eth.setGasPriceStrategy(time_based_gas_price_strategy)
# w3.middleware_onion.add(middleware.time_based_cache_middleware)
# w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
# w3.middleware_onion.add(middleware.simple_cache_middleware)
w3.eth.setGasPriceStrategy(value_based_gas_price_strategy)

uniswap_wrapper = Uniswap(
    DefaultConfig.address,
    DefaultConfig.private_key,
    version=2,
    web3=w3,
    max_slippage=1.0
)

uni_contract = w3.eth.contract(
    address=DefaultConfig.uniswap_router_address,
    abi=json.loads(DefaultConfig.abi)
)

minimal_ether_value_order = DefaultConfig.minimal_ether_value_order
minimal_slippage_percentage = DefaultConfig.minimal_slippage_percentage


def handle_event(event):
    try:
        global front_runner_data
        global pause
        front_runner_data = FrontRunnerData()
        front_runner_data.tx = w3.eth.getTransaction(event)
        front_runner_data.input_decoded = uni_contract.decode_function_input(front_runner_data.tx.input)

        if is_uni_swap_tx(front_runner_data) and is_whitelisted_trade(front_runner_data):

            """Slippage and order size should be within the configured range"""
            slippage_percentage = get_slippage_percentage(front_runner_data, w3, uniswap_wrapper)
            ether_value_order = get_ether_value_villain_order(front_runner_data, w3)
            if slippage_percentage > minimal_slippage_percentage and ether_value_order > minimal_ether_value_order:
                print_order_info(front_runner_data, w3, uniswap_wrapper)

                pause = True
                # trade_amount = int(front_runner_data.trade_amount * 100)
                trade_amount = int(0.10 * 10 ** 18)
                buy(front_runner_data, trade_amount, uniswap_wrapper, w3)
                time.sleep(20)
                sell(front_runner_data, trade_amount, uniswap_wrapper, w3)
                time.sleep(120)
                pause = False

    except Exception as e:
        if "Transaction with hash" in str(e):
            pass
        elif "Could not find any function with matching selector" == str(e):
            # this one is a different swap call, todo: support
            pass
        else:
            print(e)
            print(traceback.format_exc())
            time.sleep(30)
            pause = False


async def log_loop(event_filter):
    while True:
        global pause
        if not pause:
            for event in event_filter.get_new_entries():
                handle_event(event)


def main():
    tx_filter = w3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter)))
    finally:
        loop.close()


if __name__ == '__main__':
    main()

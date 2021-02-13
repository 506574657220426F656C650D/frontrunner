from uniswap import Uniswap
import asyncio
import rlp
import asyncio
import json
from decimal import Decimal
from config import DefaultConfig
from datetime import datetime
import sys
import time
from web3 import Web3, middleware
from web3.gas_strategies.time_based import construct_time_based_gas_price_strategy


def value_based_gas_price_strategy(web3, transaction_params=None):
    # todo base on villain gas and value of transfer
    return Web3.toWei(150, 'gwei')


w3 = Web3(
    Web3.IPCProvider(
        DefaultConfig.ipc_provider
    )
)

w3.eth.setGasPriceStrategy(value_based_gas_price_strategy)

uniswap_wrapper = Uniswap(
    DefaultConfig.address,
    DefaultConfig.private_key,
    version=2,
    web3=w3,
    max_slippage=10.0
)

uni_contract = w3.eth.contract(
    address=DefaultConfig.uniswap_router_address,
    abi=json.loads(DefaultConfig.abi)
)

coin = Web3.toChecksumAddress("0xb1fda21901afbded910af72588c8dfd6020aced1")

trade_amount = 200 * 10 ** 9


def buy():
    for i in range(10000):
        try:
            print("buying ", trade_amount, " of ", coin)


            uniswap_wrapper.make_trade_output(
                DefaultConfig.eth,
                coin,
                trade_amount
            )
        except Exception as e:
            print(e)
            time.sleep(1)
        else:
            sys.exit()
            break


if __name__ == '__main__':
    buy()

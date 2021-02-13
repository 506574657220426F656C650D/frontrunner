# frontrunner

## Setup
- install geth node
- python3 -m venv frontrunner
- source frontrunner/bin/activate
- pip install -r requirements.txt

## resources
- https://etherscan.io/tx/0xf392f392f213aceae2ed9e11f676d63c6179a9f1997247cf0b4cb9bc28d85ca3
- https://ethereum.stackexchange.com/questions/70340/how-exactly-do-you-decode-input-data-using-web3-py-using-the-decode-function-inp
- https://github.com/shanefontaine/uniswap-python

## todo
- fix selling
- gas too slow

## responses
``` 
(
 <Function swapExactETHForTokens(uint256,address[],address,uint256)>,
    {
        'amountOutMin': 123866684381120210048,
        'path': ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        '0x72630B1e3B42874bf335020Ba0249e3E9e47Bafc'],
        'to': '0x08DcD53c5070cA76F23123980c69740eA10B707f',
        'deadline': 1606081464
    }
)
```

```
0xfE1aC70318C4b24f451420E0A174D31fb15229bB -> AttributeDict(
{
    '252': AttributeDict(
        {
            'blockHash': None, 
            'blockNumber': None, 
            'from': '0xfe1ac70318c4b24f451420e0a174d31fb15229bb', 
            'gas': '0x29053', 
            'gasPrice': '0x4a817cdb3', 
            'hash': '0xf392f392f213aceae2ed9e11f676d63c6179a9f1997247cf0b4cb9bc28d85ca3', 
            'input': '
            0x18cbafe5000000000000000000000000000000000000000000000a968163f0
            a57b4000000000000000000000000000000000000000000000000000000e6652
            aaa47737ac000000000000000000000000000000000000000000000000000000
            00000000a0000000000000000000000000fe1ac70318c4b24f451420e0a174d3
            1fb15229bb000000000000000000000000000000000000000000000000000000
            005fb230ad000000000000000000000000000000000000000000000000000000
            00000000020000000000000000000000009ed8e7c9604790f7ec589f99b94361
            d8aab64e5e000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 
            000000000000000000000000000000000000000000000a968163f0a57b400000
            'nonce': '0xfc', 
            'to': '0x7a250d5630b4cf539739df2c5dacb4c659f2488d', 
            'transactionIndex': None, 
            'value': '0x0', 
            'v': '0x25', 
            'r': '0xb6a281aa83e7c1675c34c53c62bb042ade5a57b3f0aba1ddf16c39864dc8e2a', 
            's': '0x685f4da1b0495a4e45968206691e4bd69c08159f29fa75b5aee8c5a7b13ed787'
            }
        ), 
    '253': AttributeDict(
        {
            'blockHash': None, 
            'blockNumber': None, 
            'from': '0xfe1ac70318c4b24f451420e0a174d31fb15229bb', 
            'gas': '0x290ee', 
            'gasPrice': '0x4a817cdb3', 
            'hash': '0xbc4adf5084841860829d88abe1c0c84c4e33c44b3536fe5b259057db58f992ae', 
            'input': '0x18cbafe500000000000000000000000000000000000000000000001ce8daad0265e30a210000000000000000000000000000000000000000000000000c4fd1a726351ebc00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000fe1ac70318c4b24f451420e0a174d31fb15229bb000000000000000000000000000000000000000000000000000000005fb230ad000000000000000000000000000000000000000000000000000000000000000200000000000000000000000039eae99e685906ff1c11a962a743440d0a1a6e09000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 
            'nonce': '0xfd', 
            'to': '0x7a250d5630b4cf539739df2c5dacb4c659f2488d', 
            'transactionIndex': None, 
            'value': '0x0', 
            'v': '0x26', 
            'r': '0x6050da15e247f7b4257047efd59a86c75f898dfc74f48d892ac03030739ee14e', 
            's': '0x7984dfbef5cbd5d8b8296c2e56d106e09043a0dc52bc3d656c7a2fff31ff93db'}
        )
    }
)
```



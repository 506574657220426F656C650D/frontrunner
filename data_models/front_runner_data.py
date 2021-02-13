class FrontRunnerData:
    def __init__(
            self,
            tx: str = None,
            input_decoded: tuple = None,
            public_amount_min: int = None,
            amount_min: int = None,
            trade_amount: int = None

    ):
        self.tx: str = tx
        self.input_decoded: tuple = input_decoded
        self.public_amount_min: int = public_amount_min
        self.amount_min: int = amount_min
        self.trade_amount: int = trade_amount

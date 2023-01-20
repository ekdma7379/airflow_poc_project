from typing import Optional, List
from model import model_base


class Buy(model_base.BaseElement):
    amount: Optional[str]
    quantity: Optional[str]
    price: Optional[str]

    def __init__(self, amount: Optional[str]= None, quantity: Optional[str]= None, price: Optional[str]= None) -> None:
        super().__init__()
        self.amount = amount
        self.quantity = quantity
        self.price = price

class Sell(model_base.BaseElement):
    amount: Optional[str]
    quantity: Optional[str]
    price: Optional[str]

    def __init__(self, amount: Optional[str]= None, quantity: Optional[str]= None, price: Optional[str]= None) -> None:
        super().__init__()
        self.amount = amount
        self.quantity = quantity
        self.price = price        


class ValuationCFD(model_base.BaseElement):
    buy: Buy
    sell: Buy

    def __init__(self, buy: Buy= None, sell: Buy= None) -> None:
        super().__init__()
        self.buy = buy
        self.sell = sell


class Quote(model_base.BaseElement):
    value: Optional[str]
    currency: Optional[str]
    valuationDate: Optional[str]
    valuationMethod: Optional[str]

    def __init__(self, value: Optional[str]= None, currency: Optional[str]= None, valuationDate: Optional[str]= None, valuationMethod: Optional[str]= None) -> None:
        super().__init__()
        self.value = value
        self.currency = currency
        self.valuationDate = valuationDate
        self.valuationMethod = valuationMethod


class AssetValuation(model_base.BaseElement):
    quote: Optional[Quote]

    def __init__(self, quote: Optional[Quote]= None) -> None:
        super().__init__()
        self.quote = quote


class ValuationSet(model_base.BaseElement):
    assetValuation: Optional[AssetValuation]

    def __init__(self, assetValuation: Optional[AssetValuation]= None) -> None:
        super().__init__()
        self.assetValuation = assetValuation


class TradeValuationItem(model_base.BaseElement):
    trade : Optional[model_base.trade]
    valuationSet: Optional[ValuationSet]
    valuationCfd: Optional[ValuationCFD]

    def __init__(self,trade : Optional[model_base.trade]= None, valuationSet: Optional[ValuationSet]= None, valuationCfd: Optional[ValuationCFD]= None) -> None:
        super().__init__()
        self.trade = trade
        self.valuationSet = valuationSet
        self.valuationCfd = valuationCfd


class KtrRequestReport(model_base.BaseElement):
    header: model_base.header
    tradeValuationItem: TradeValuationItem
    party: List[model_base.party]

    def __init__(self, header: model_base.header, tradeValuationItem: TradeValuationItem, party: List[model_base.party]) -> None:
        super().__init__()
        self.header = header
        self.tradeValuationItem = tradeValuationItem
        self.party = party

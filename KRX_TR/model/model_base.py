from typing import Dict, Optional, List
from xml.etree.ElementTree import Element, SubElement, ElementTree

class BaseElement:
    _attr : Dict[str, str]
    def __init__(self, attr: Dict[str, str] = None):
        self._attr = {}
    def set_attr(self, key: str, value: str) -> None:
        self._attr[key] = value
    def objtoxml(self) -> Element:
        root = Element(type(self).__name__)
        ## attr 설정
        for key, value in self._attr.items():
            root.set(key, value)
        ## Element 설정
        for key, value in self.__dict__.items():
            if key == "_attr":
                pass
            elif value == None:
                pass
            elif type(value) == list:
                for item in value:
                    if BaseElement in type(item).mro():
                        root.append(item.objtoxml())
                    else:
                        temp = Element(key)
                        temp.text = item
                        root.append(temp)
            elif BaseElement in type(value).mro():
                temp = value.objtoxml()
                root.append(temp)
            else:
                temp = Element(key)
                temp.text = value
                root.append(temp)
        return root
## TRADE
class SupervisoryRegistration(BaseElement):
    supervisorBody: Optional[str]

    def __init__(self, supervisorBody: Optional[str]= None) -> None:
        super().__init__()
        self.supervisorBody = supervisorBody
        
class ReportingRegime(BaseElement):
    supervisoryRegistration: Optional[SupervisoryRegistration]
    reportingPurpose: Optional[str]
    actionType: Optional[str]

    def __init__(self, supervisoryRegistration: Optional[SupervisoryRegistration]= None, reportingPurpose: Optional[str]= None, actionType: Optional[str]= None) -> None:
        super().__init__()
        self.supervisoryRegistration = supervisoryRegistration
        self.reportingPurpose = reportingPurpose
        self.actionType = actionType
        
class PartyReference(BaseElement):
    href: Optional[str]

    def __init__(self, href: Optional[str]= None) -> None:
        super().__init__()
        self.set_attr("href",href)

class RelatedParty(BaseElement):
    partyReference: Optional[PartyReference]
    role: Optional[str]

    def __init__(self, partyReference: Optional[PartyReference]= None, role: Optional[str]= None) -> None:
        super().__init__()
        self.partyReference = partyReference
        self.role = role    

class TimeStamps(BaseElement):
    confirmed: Optional[str]
    cleared: Optional[str]

    def __init__(self, confirmed: Optional[str]= None, cleared: Optional[str]= None) -> None:
        super().__init__()
        self.confirmed = confirmed
        self.cleared = cleared
   
class PartyTradeInformation(BaseElement):
    partyReference: Optional[PartyReference]
    reportingRegime: Optional[ReportingRegime]
    relatedParty: Optional[List[RelatedParty]]
    category1: Optional[str]
    category2: Optional[str]
    category3: Optional[str]
    executionVenueType: Optional[str]
    confirmationMethod: Optional[str]
    executionDateTime: Optional[str]
    timeStamps: Optional[TimeStamps]
    intentToClear: Optional[str]
    clearingIndicator: Optional[str]
    collateralizationType: Optional[str]
    collateralPortfolioIndicator: Optional[str]
    collateralPortfolio: Optional[str]
    collateralPortfolio2: Optional[str]
    marginRequiredForNonCca: Optional[str]
    embeddedOptionIndicator: Optional[str]

    def __init__(self, partyReference: Optional[PartyReference]= None, reportingRegime: Optional[ReportingRegime]= None, relatedParty: Optional[List[RelatedParty]]= None, category1: Optional[str]= None, category2: Optional[str]= None, category3: Optional[str]= None, executionVenueType: Optional[str]= None, confirmationMethod: Optional[str]= None, executionDateTime: Optional[str]= None, timeStamps: Optional[TimeStamps]= None, intentToClear: Optional[str]= None, clearingIndicator: Optional[str]= None, collateralizationType: Optional[str]= None, collateralPortfolioIndicator: Optional[str]= None, collateralPortfolio: Optional[str]= None, collateralPortfolio2: Optional[str]= None, marginRequiredForNonCca: Optional[str]= None, embeddedOptionIndicator: Optional[str]= None) -> None:
        super().__init__()
        self.partyReference = partyReference
        self.reportingRegime = reportingRegime
        self.relatedParty = relatedParty
        self.category1 = category1
        self.category2 = category2
        self.category3 = category3
        self.executionVenueType = executionVenueType
        self.confirmationMethod = confirmationMethod
        self.executionDateTime = executionDateTime
        self.timeStamps = timeStamps
        self.intentToClear = intentToClear
        self.clearingIndicator = clearingIndicator
        self.collateralizationType = collateralizationType
        self.collateralPortfolioIndicator = collateralPortfolioIndicator
        self.collateralPortfolio = collateralPortfolio
        self.collateralPortfolio2 = collateralPortfolio2
        self.marginRequiredForNonCca = marginRequiredForNonCca
        self.embeddedOptionIndicator = embeddedOptionIndicator

class PartyTradeIdentifier(BaseElement):
    tradeId: Optional[str]
    originatingTradeId: Optional[str]
    linkId: Optional[str]

    def __init__(self, tradeId: Optional[str]= None, originatingTradeId: Optional[str]= None, linkId: Optional[str]= None) -> None:
        super().__init__()
        self.tradeId = tradeId
        self.originatingTradeId = originatingTradeId
        self.linkId = linkId
        
class ProductSummary(BaseElement):
    productCodeFss: Optional[str]
    productName: Optional[str]
    relatedProductCode: Optional[str]
    productId: Optional[str]
    assetClass: Optional[str]
    instrumentType: Optional[str]
    exerciseStyle: Optional[str]
    optionType: Optional[str]
    pricingMethod: Optional[str]
    notionalSchedule: Optional[str]
    singleOrMultipleCurrency: Optional[str]
    singleOrMultipleTenor: Optional[str]
    contractType: Optional[List[str]]
    contractSubType: Optional[List[str]]
    seniority: Optional[str]
    settlementType: Optional[str]
    settlementCurrency: Optional[str]

    def __init__(self, productCodeFss: Optional[str] = None, productName: Optional[str]= None, relatedProductCode: Optional[str]= None, productId: Optional[str]= None, assetClass: Optional[str]= None, instrumentType: Optional[str]= None, exerciseStyle: Optional[str]= None, optionType: Optional[str]= None, pricingMethod: Optional[str]= None, notionalSchedule: Optional[str]= None, singleOrMultipleCurrency: Optional[str]= None, singleOrMultipleTenor: Optional[str]= None, contractType: Optional[List[str]] = None, contractSubType: Optional[List[str]]= None, seniority: Optional[str]= None, settlementType: Optional[str]= None, settlementCurrency: Optional[str]= None) -> None:
        super().__init__()
        self.productCodeFss = productCodeFss
        self.productName = productName
        self.relatedProductCode = relatedProductCode
        self.productId = productId
        self.assetClass = assetClass
        self.instrumentType = instrumentType
        self.exerciseStyle = exerciseStyle
        self.optionType = optionType
        self.pricingMethod = pricingMethod
        self.notionalSchedule = notionalSchedule
        self.singleOrMultipleCurrency = singleOrMultipleCurrency
        self.singleOrMultipleTenor = singleOrMultipleTenor
        self.contractType = contractType
        self.contractSubType = contractSubType
        self.seniority = seniority
        self.settlementType = settlementType
        self.settlementCurrency = settlementCurrency

class PackageIdentifier(BaseElement):
    tradeId: Optional[str]
    price: Optional[str]
    priceCurrency: Optional[str]
    priceNotation: Optional[str]
    spread: Optional[str]
    spreadCurrency: Optional[str]
    spreadNotation: Optional[str]

    def __init__(self, tradeId: Optional[str]= None, price: Optional[str]= None, priceCurrency: Optional[str]= None, priceNotation: Optional[str]= None, spread: Optional[str]= None, spreadCurrency: Optional[str]= None, spreadNotation: Optional[str]= None) -> None:
        super().__init__()
        self.tradeId = tradeId
        self.price = price
        self.priceCurrency = priceCurrency
        self.priceNotation = priceNotation
        self.spread = spread
        self.spreadCurrency = spreadCurrency
        self.spreadNotation = spreadNotation

class OriginatingPackage(BaseElement):
    packageIdentifier: Optional[PackageIdentifier]

    def __init__(self, packageIdentifier: Optional[PackageIdentifier] = None) -> None:
        super().__init__()
        self.packageIdentifier = packageIdentifier

class TradeHeader(BaseElement):
    partyTradeIdentifier: Optional[PartyTradeIdentifier]
    partyTradeInformation: Optional[PartyTradeInformation]
    productSummary: Optional[ProductSummary]
    originatingPackage: Optional[OriginatingPackage]

    def __init__(self, partyTradeIdentifier: Optional[PartyTradeIdentifier]= None, partyTradeInformation: Optional[PartyTradeInformation]= None, productSummary: Optional[ProductSummary]= None, originatingPackage: Optional[OriginatingPackage]= None) -> None:
        super().__init__()
        self.partyTradeIdentifier = partyTradeIdentifier
        self.partyTradeInformation = partyTradeInformation
        self.productSummary = productSummary
        self.originatingPackage = originatingPackage

class trade(BaseElement):
    agreementDate: Optional[str]
    earlyTerminationDate: Optional[str]
    tradeHeader: Optional[TradeHeader]
    # calculationAgent: CalculationAgent
    # documentation: Documentation
    # additionalPayment: AdditionalPayment
    # irSwap: IRSwap

    def __init__(self, agreementDate: Optional[str] = None, earlyTerminationDate: Optional[str]= None, tradeHeader: TradeHeader= None
                 #, calculationAgent: CalculationAgent, documentation: Documentation, additionalPayment: AdditionalPayment, irSwap: IRSwap
                 ) -> None:
        super().__init__()
        self.agreementDate = agreementDate
        self.earlyTerminationDate = earlyTerminationDate
        self.tradeHeader = tradeHeader
        # self.calculationAgent = calculationAgent
        # self.documentation = documentation
        # self.additionalPayment = additionalPayment
        # self.irSwap = irSwap
## TRADE END

## PARTY
class address(BaseElement):
    postalCode: str

    def __init__(self, postalCode: str= None) -> None:
        super().__init__()
        self.postalCode = postalCode


class contactInfo(BaseElement):
    address: Optional[address]

    def __init__(self, address: Optional[address]= None) -> None:
        super().__init__()
        self.address = address
    
class party(BaseElement):
    id: str
    partyIdPrefix: Optional[str]
    partyId: Optional[str]
    name: Optional[str]
    country: Optional[str]
    contactInfo: Optional[contactInfo]
    koreanResidency: Optional[str]

    def __init__(self, id: str= None
                     , partyId: Optional[str] = None
                     , partyIdPrefix: Optional[str]= None
                     , name: Optional[str]= None
                     , country: Optional[str]= None
                     , contactInfo: Optional[contactInfo] = None
                     , koreanResidency: Optional[str]= None) -> None:
        super().__init__()
        self.set_attr("id",id)
        self.partyId = partyId
        self.partyIdPrefix = partyIdPrefix
        self.name = name
        self.country = country
        self.contactInfo = contactInfo
        self.koreanResidency = koreanResidency    
## PARTY END
## HEADER
class header(BaseElement):
    version: str
    memberId: str
    submissionDate: str
    messageClassificationId: str
    localeCode: str
    reportingMethodCode: str
    reportingAccountNo: str
    reportingReferenceCode: str

    def __init__(self, version: str, memberId: str, submissionDate: str, messageClassificationId: str, localeCode: str, reportingMethodCode: str, reportingAccountNo: str, reportingReferenceCode: str) -> None:
        super().__init__()
        self.version = version
        self.memberId = memberId
        self.submissionDate = submissionDate
        self.messageClassificationId = messageClassificationId
        self.localeCode = localeCode
        self.reportingMethodCode = reportingMethodCode
        self.reportingAccountNo = reportingAccountNo
        self.reportingReferenceCode = reportingReferenceCode        
## HEADER END
class ktrRequestReport(BaseElement):
    header: header
    trade: trade
    party: List[party]

    def __init__(self, header: header, trade: trade, party: List[party]) -> None:
        super().__init__()
        self.header = header
        self.trade = trade
        self.party = party                
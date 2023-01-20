from typing import Dict, Optional, List
from KRX_TR.model.model_base import BaseElement

class Header(BaseElement):
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


class Address(BaseElement):
    postalCode: str

    def __init__(self, postalCode: str) -> None:
        self.postalCode = postalCode


class ContactInfo(BaseElement):
    address: Address

    def __init__(self, address: Address) -> None:
        self.address = address


class Party(BaseElement):
    id: str
    partyId: Optional[str]
    partyIdPrefix: Optional[str]
    name: Optional[str]
    country: Optional[str]
    contactInfo: Optional[ContactInfo]
    koreanResidency: Optional[str]

    def __init__(self, id: str= None
                     , partyId: Optional[str] = None
                     , partyIdPrefix: Optional[str]= None
                     , name: Optional[str]= None
                     , country: Optional[str]= None
                     , contactInfo: Optional[ContactInfo] = None
                     , koreanResidency: Optional[str]= None) -> None:
        super().__init__()
        self.set_attr("id",id)
        self.partyId = partyId
        self.partyIdPrefix = partyIdPrefix
        self.name = name
        self.country = country
        self.contactInfo = contactInfo
        self.koreanResidency = koreanResidency


class ErPartyReference(BaseElement):
    href: str
    text: str

    def __init__(self, href: str, text: str) -> None:
        self.href = href
        self.text = text


class PaymentAmount(BaseElement):
    amount: str
    paymentType: str
    currency: str
    paymentDate: str
    payerPartyReference: ErPartyReference
    receiverPartyReference: ErPartyReference

    def __init__(self, amount: str, paymentType: str, currency: str, paymentDate: str, payerPartyReference: ErPartyReference, receiverPartyReference: ErPartyReference) -> None:
        self.amount = amount
        self.paymentType = paymentType
        self.currency = currency
        self.paymentDate = paymentDate
        self.payerPartyReference = payerPartyReference
        self.receiverPartyReference = receiverPartyReference


class AdditionalPayment(BaseElement):
    paymentAmount1: PaymentAmount
    paymentAmount2: PaymentAmount
    paymentAmount3: PaymentAmount
    paymentAmount4: PaymentAmount
    paymentAmount5: PaymentAmount

    def __init__(self, paymentAmount1: PaymentAmount, paymentAmount2: PaymentAmount, paymentAmount3: PaymentAmount, paymentAmount4: PaymentAmount, paymentAmount5: PaymentAmount) -> None:
        self.paymentAmount1 = paymentAmount1
        self.paymentAmount2 = paymentAmount2
        self.paymentAmount3 = paymentAmount3
        self.paymentAmount4 = paymentAmount4
        self.paymentAmount5 = paymentAmount5


class Reference(BaseElement):
    href: str

    def __init__(self, href: str) -> None:
        self.href = href


class CalculationAgent(BaseElement):
    calculationAgentParty: str
    calculationAgentReference: Reference

    def __init__(self, calculationAgentParty: str, calculationAgentReference: Reference) -> None:
        self.calculationAgentParty = calculationAgentParty
        self.calculationAgentReference = calculationAgentReference


class ContractualMatrix(BaseElement):
    matrixTerm: str

    def __init__(self, matrixTerm: str) -> None:
        self.matrixTerm = matrixTerm


class MasterAgreement(BaseElement):
    masterAgreementType: str
    masterAgreementVersion: str

    def __init__(self, masterAgreementType: str, masterAgreementVersion: str) -> None:
        self.masterAgreementType = masterAgreementType
        self.masterAgreementVersion = masterAgreementVersion


class Documentation(BaseElement):
    contractualMatrix: ContractualMatrix
    masterAgreement: MasterAgreement

    def __init__(self, contractualMatrix: ContractualMatrix, masterAgreement: MasterAgreement) -> None:
        self.contractualMatrix = contractualMatrix
        self.masterAgreement = masterAgreement


class PrincipalExchanges(BaseElement):
    initialExchange: str
    intermediateExchange: str
    finalExchange: str
    initialPrincipalExchangeDate: str
    varyingNotionalCurrency: str

    def __init__(self, initialExchange: str, intermediateExchange: str, finalExchange: str, initialPrincipalExchangeDate: str, varyingNotionalCurrency: str) -> None:
        self.initialExchange = initialExchange
        self.intermediateExchange = intermediateExchange
        self.finalExchange = finalExchange
        self.initialPrincipalExchangeDate = initialPrincipalExchangeDate
        self.varyingNotionalCurrency = varyingNotionalCurrency


class CRS(BaseElement):
    principalExchanges: PrincipalExchanges

    def __init__(self, principalExchanges: PrincipalExchanges) -> None:
        self.principalExchanges = principalExchanges


class NonMarketableAssetType(BaseElement):
    maxOccurs: int
    text: str

    def __init__(self, maxOccurs: int, text: str) -> None:
        self.maxOccurs = maxOccurs
        self.text = text


class HybridCommon(BaseElement):
    hybridProduct: str
    secondAssetClass: NonMarketableAssetType

    def __init__(self, hybridProduct: str, secondAssetClass: NonMarketableAssetType) -> None:
        self.hybridProduct = hybridProduct
        self.secondAssetClass = secondAssetClass


class HybridCommodityClass(BaseElement):
    underlyingAssetIdType: NonMarketableAssetType
    underlyingAssetIdSource: NonMarketableAssetType
    underlyingAssetId: NonMarketableAssetType

    def __init__(self, underlyingAssetIdType: NonMarketableAssetType, underlyingAssetIdSource: NonMarketableAssetType, underlyingAssetId: NonMarketableAssetType) -> None:
        self.underlyingAssetIdType = underlyingAssetIdType
        self.underlyingAssetIdSource = underlyingAssetIdSource
        self.underlyingAssetId = underlyingAssetId


class HybridConstituent(BaseElement):
    hybridFx: HybridCommodityClass
    hybridEquity: HybridCommodityClass
    hybridCredit: HybridCommodityClass
    hybridCommodity: HybridCommodityClass

    def __init__(self, hybridFx: HybridCommodityClass, hybridEquity: HybridCommodityClass, hybridCredit: HybridCommodityClass, hybridCommodity: HybridCommodityClass) -> None:
        self.hybridFx = hybridFx
        self.hybridEquity = hybridEquity
        self.hybridCredit = hybridCredit
        self.hybridCommodity = hybridCommodity


class Hybrid(BaseElement):
    hybridCommon: HybridCommon
    hybridConstituent: HybridConstituent

    def __init__(self, hybridCommon: HybridCommon, hybridConstituent: HybridConstituent) -> None:
        self.hybridCommon = hybridCommon
        self.hybridConstituent = hybridConstituent


class PaymentFrequency(BaseElement):
    periodMultiplier: str
    period: str

    def __init__(self, periodMultiplier: str, period: str) -> None:
        self.periodMultiplier = periodMultiplier
        self.period = period


class InflationRateCalculation(BaseElement):
    inflationLeg: PaymentFrequency
    interpolationMethod: str
    initialIndexLevel: str

    def __init__(self, inflationLeg: PaymentFrequency, interpolationMethod: str, initialIndexLevel: str) -> None:
        self.inflationLeg = inflationLeg
        self.interpolationMethod = interpolationMethod
        self.initialIndexLevel = initialIndexLevel


class PurpleCalculation(BaseElement):
    inflationRateCalculation: InflationRateCalculation

    def __init__(self, inflationRateCalculation: InflationRateCalculation) -> None:
        self.inflationRateCalculation = inflationRateCalculation


class InflationCalculationPeriodAmount(BaseElement):
    calculation: PurpleCalculation

    def __init__(self, calculation: PurpleCalculation) -> None:
        self.calculation = calculation


class Inflation(BaseElement):
    calculationPeriodAmount: InflationCalculationPeriodAmount

    def __init__(self, calculationPeriodAmount: InflationCalculationPeriodAmount) -> None:
        self.calculationPeriodAmount = calculationPeriodAmount


class NonDeliverableSettlement(BaseElement):
    settlementRateFixingDate: NonMarketableAssetType
    settlementRateOption: NonMarketableAssetType

    def __init__(self, settlementRateFixingDate: NonMarketableAssetType, settlementRateOption: NonMarketableAssetType) -> None:
        self.settlementRateFixingDate = settlementRateFixingDate
        self.settlementRateOption = settlementRateOption


class SettlementProvision(BaseElement):
    nonDeliverableSettlement: NonDeliverableSettlement

    def __init__(self, nonDeliverableSettlement: NonDeliverableSettlement) -> None:
        self.nonDeliverableSettlement = nonDeliverableSettlement


class Structured(BaseElement):
    principalGuaranteed: str
    fundingType: str

    def __init__(self, principalGuaranteed: str, fundingType: str) -> None:
        self.principalGuaranteed = principalGuaranteed
        self.fundingType = fundingType


class CurrentNotional(BaseElement):
    amount: str
    currency: str

    def __init__(self, amount: str, currency: str) -> None:
        self.amount = amount
        self.currency = currency


class Discounting(BaseElement):
    discountingType: str
    discountingRate: str
    discountRateDayCountFraction: str

    def __init__(self, discountingType: str, discountingRate: str, discountRateDayCountFraction: str) -> None:
        self.discountingType = discountingType
        self.discountingRate = discountingRate
        self.discountRateDayCountFraction = discountRateDayCountFraction


class FixedRateSchedule(BaseElement):
    rate: str
    rateNotation: str

    def __init__(self, rate: str, rateNotation: str) -> None:
        self.rate = rate
        self.rateNotation = rateNotation


class IndexTenor(BaseElement):
    periodMultiplier: NonMarketableAssetType
    period: NonMarketableAssetType

    def __init__(self, periodMultiplier: NonMarketableAssetType, period: NonMarketableAssetType) -> None:
        self.periodMultiplier = periodMultiplier
        self.period = period


class SpreadSchedule(BaseElement):
    spread: NonMarketableAssetType
    spreadNotation: NonMarketableAssetType

    def __init__(self, spread: NonMarketableAssetType, spreadNotation: NonMarketableAssetType) -> None:
        self.spread = spread
        self.spreadNotation = spreadNotation


class FloatingRateCalculation(BaseElement):
    floatingRateIndexSource: NonMarketableAssetType
    floatingRateIndex: NonMarketableAssetType
    floatingRateIndexCurrency: NonMarketableAssetType
    indexTenor: IndexTenor
    floatingRateMultiplier: NonMarketableAssetType
    spreadSchedule: SpreadSchedule
    averagingMethod: str
    initialRate: str

    def __init__(self, floatingRateIndexSource: NonMarketableAssetType, floatingRateIndex: NonMarketableAssetType, floatingRateIndexCurrency: NonMarketableAssetType, indexTenor: IndexTenor, floatingRateMultiplier: NonMarketableAssetType, spreadSchedule: SpreadSchedule, averagingMethod: str, initialRate: str) -> None:
        self.floatingRateIndexSource = floatingRateIndexSource
        self.floatingRateIndex = floatingRateIndex
        self.floatingRateIndexCurrency = floatingRateIndexCurrency
        self.indexTenor = indexTenor
        self.floatingRateMultiplier = floatingRateMultiplier
        self.spreadSchedule = spreadSchedule
        self.averagingMethod = averagingMethod
        self.initialRate = initialRate


class Step(BaseElement):
    amount: NonMarketableAssetType
    startDate: NonMarketableAssetType
    endDate: NonMarketableAssetType

    def __init__(self, amount: NonMarketableAssetType, startDate: NonMarketableAssetType, endDate: NonMarketableAssetType) -> None:
        self.amount = amount
        self.startDate = startDate
        self.endDate = endDate


class NotionalStepSchedule(BaseElement):
    step: Step

    def __init__(self, step: Step) -> None:
        self.step = step


class NotionalSchedule(BaseElement):
    notionalStepSchedule: NotionalStepSchedule

    def __init__(self, notionalStepSchedule: NotionalStepSchedule) -> None:
        self.notionalStepSchedule = notionalStepSchedule


class FluffyCalculation(BaseElement):
    currentNotional: CurrentNotional
    notionalSchedule: NotionalSchedule
    fixedRateSchedule: FixedRateSchedule
    floatingRateCalculation: FloatingRateCalculation
    dayCountFraction: str
    discounting: Discounting
    compoundingMethod: str

    def __init__(self, currentNotional: CurrentNotional, notionalSchedule: NotionalSchedule, fixedRateSchedule: FixedRateSchedule, floatingRateCalculation: FloatingRateCalculation, dayCountFraction: str, discounting: Discounting, compoundingMethod: str) -> None:
        self.currentNotional = currentNotional
        self.notionalSchedule = notionalSchedule
        self.fixedRateSchedule = fixedRateSchedule
        self.floatingRateCalculation = floatingRateCalculation
        self.dayCountFraction = dayCountFraction
        self.discounting = discounting
        self.compoundingMethod = compoundingMethod


class SwapStream1CalculationPeriodAmount(BaseElement):
    calculation: FluffyCalculation

    def __init__(self, calculation: FluffyCalculation) -> None:
        self.calculation = calculation


class BusinessCenters(BaseElement):
    businessCenter: NonMarketableAssetType

    def __init__(self, businessCenter: NonMarketableAssetType) -> None:
        self.businessCenter = businessCenter


class Adjustments(BaseElement):
    businessDayConvention: str
    businessCenters: BusinessCenters

    def __init__(self, businessDayConvention: str, businessCenters: BusinessCenters) -> None:
        self.businessDayConvention = businessDayConvention
        self.businessCenters = businessCenters


class CalculationPeriodFrequency(BaseElement):
    periodMultiplier: str
    period: str
    rollConvention: str

    def __init__(self, periodMultiplier: str, period: str, rollConvention: str) -> None:
        self.periodMultiplier = periodMultiplier
        self.period = period
        self.rollConvention = rollConvention


class CalculationPeriodDates(BaseElement):
    calculationPeriodDatesAdjustments: Adjustments
    firstPeriodStartDate: str
    firstRegularPeriodStartDate: str
    lastRegularPeriodEndDate: str
    stubPeriodType: NonMarketableAssetType
    calculationPeriodFrequency: CalculationPeriodFrequency

    def __init__(self, calculationPeriodDatesAdjustments: Adjustments, firstPeriodStartDate: str, firstRegularPeriodStartDate: str, lastRegularPeriodEndDate: str, stubPeriodType: NonMarketableAssetType, calculationPeriodFrequency: CalculationPeriodFrequency) -> None:
        self.calculationPeriodDatesAdjustments = calculationPeriodDatesAdjustments
        self.firstPeriodStartDate = firstPeriodStartDate
        self.firstRegularPeriodStartDate = firstRegularPeriodStartDate
        self.lastRegularPeriodEndDate = lastRegularPeriodEndDate
        self.stubPeriodType = stubPeriodType
        self.calculationPeriodFrequency = calculationPeriodFrequency


class CalculationPeriod(BaseElement):
    adjustedEndDate: NonMarketableAssetType

    def __init__(self, adjustedEndDate: NonMarketableAssetType) -> None:
        self.adjustedEndDate = adjustedEndDate


class PaymentCalculationPeriod(BaseElement):
    adjustedPaymentDate: NonMarketableAssetType
    calculationPeriod: CalculationPeriod

    def __init__(self, adjustedPaymentDate: NonMarketableAssetType, calculationPeriod: CalculationPeriod) -> None:
        self.adjustedPaymentDate = adjustedPaymentDate
        self.calculationPeriod = calculationPeriod


class Cashflows(BaseElement):
    paymentCalculationPeriod: PaymentCalculationPeriod

    def __init__(self, paymentCalculationPeriod: PaymentCalculationPeriod) -> None:
        self.paymentCalculationPeriod = paymentCalculationPeriod


class EffectiveDate(BaseElement):
    unadjustedDate: str

    def __init__(self, unadjustedDate: str) -> None:
        self.unadjustedDate = unadjustedDate


class TerminationDate(BaseElement):
    unadjustedDate: str
    dateAdjustments: Adjustments

    def __init__(self, unadjustedDate: str, dateAdjustments: Adjustments) -> None:
        self.unadjustedDate = unadjustedDate
        self.dateAdjustments = dateAdjustments


class Common(BaseElement):
    payerPartyReference: Reference
    effectiveDate: EffectiveDate
    terminationDate: TerminationDate

    def __init__(self, payerPartyReference: Reference, effectiveDate: EffectiveDate, terminationDate: TerminationDate) -> None:
        self.payerPartyReference = payerPartyReference
        self.effectiveDate = effectiveDate
        self.terminationDate = terminationDate


class PaymentDaysOffset(BaseElement):
    paymentDatesOffsetDays: str

    def __init__(self, paymentDatesOffsetDays: str) -> None:
        self.paymentDatesOffsetDays = paymentDatesOffsetDays


class PaymentDates(BaseElement):
    paymentFrequency: PaymentFrequency
    payRelativeTo: str
    paymentDaysOffset: PaymentDaysOffset
    paymentDatesAdjustments: Adjustments

    def __init__(self, paymentFrequency: PaymentFrequency, payRelativeTo: str, paymentDaysOffset: PaymentDaysOffset, paymentDatesAdjustments: Adjustments) -> None:
        self.paymentFrequency = paymentFrequency
        self.payRelativeTo = payRelativeTo
        self.paymentDaysOffset = paymentDaysOffset
        self.paymentDatesAdjustments = paymentDatesAdjustments


class AlExchange(BaseElement):
    amount: str

    def __init__(self, amount: str) -> None:
        self.amount = amount


class PrincipalExchange(BaseElement):
    initialExchange: AlExchange
    finalExchange: AlExchange

    def __init__(self, initialExchange: AlExchange, finalExchange: AlExchange) -> None:
        self.initialExchange = initialExchange
        self.finalExchange = finalExchange


class ResetCutOffDaysOffset(BaseElement):
    fixingDatesOffsetDays: str

    def __init__(self, fixingDatesOffsetDays: str) -> None:
        self.fixingDatesOffsetDays = fixingDatesOffsetDays


class ResetDates(BaseElement):
    resetRelativeTo: str
    resetCutOffDaysOffset: ResetCutOffDaysOffset
    resetFrequency: PaymentFrequency
    resetDatesAdjustments: Adjustments

    def __init__(self, resetRelativeTo: str, resetCutOffDaysOffset: ResetCutOffDaysOffset, resetFrequency: PaymentFrequency, resetDatesAdjustments: Adjustments) -> None:
        self.resetRelativeTo = resetRelativeTo
        self.resetCutOffDaysOffset = resetCutOffDaysOffset
        self.resetFrequency = resetFrequency
        self.resetDatesAdjustments = resetDatesAdjustments


class SwapStream(BaseElement):
    common: Common
    calculationPeriodDates: CalculationPeriodDates
    paymentDates: PaymentDates
    resetDates: ResetDates
    calculationPeriodAmount: SwapStream1CalculationPeriodAmount
    principalExchange: PrincipalExchange
    cashflows: Cashflows

    def __init__(self, common: Common, calculationPeriodDates: CalculationPeriodDates, paymentDates: PaymentDates, resetDates: ResetDates, calculationPeriodAmount: SwapStream1CalculationPeriodAmount, principalExchange: PrincipalExchange, cashflows: Cashflows) -> None:
        self.common = common
        self.calculationPeriodDates = calculationPeriodDates
        self.paymentDates = paymentDates
        self.resetDates = resetDates
        self.calculationPeriodAmount = calculationPeriodAmount
        self.principalExchange = principalExchange
        self.cashflows = cashflows


class UnderlyingAsset(BaseElement):
    nonMarketableAssetType: NonMarketableAssetType

    def __init__(self, nonMarketableAssetType: NonMarketableAssetType) -> None:
        self.nonMarketableAssetType = nonMarketableAssetType


class IRSwap(BaseElement):
    swapStream1: SwapStream
    swapStream2: SwapStream
    crs: CRS
    inflation: Inflation
    structured: Structured
    settlementProvision: SettlementProvision
    underlyingAsset: UnderlyingAsset
    hybrid: Hybrid

    def __init__(self, swapStream1: SwapStream, swapStream2: SwapStream, crs: CRS, inflation: Inflation, structured: Structured, settlementProvision: SettlementProvision, underlyingAsset: UnderlyingAsset, hybrid: Hybrid) -> None:
        self.swapStream1 = swapStream1
        self.swapStream2 = swapStream2
        self.crs = crs
        self.inflation = inflation
        self.structured = structured
        self.settlementProvision = settlementProvision
        self.underlyingAsset = underlyingAsset
        self.hybrid = hybrid


class PackageIdentifier(BaseElement):
    tradeId: str
    price: str
    priceCurrency: str
    priceNotation: str
    spread: str
    spreadCurrency: str
    spreadNotation: str

    def __init__(self, tradeId: str, price: str, priceCurrency: str, priceNotation: str, spread: str, spreadCurrency: str, spreadNotation: str) -> None:
        self.tradeId = tradeId
        self.price = price
        self.priceCurrency = priceCurrency
        self.priceNotation = priceNotation
        self.spread = spread
        self.spreadCurrency = spreadCurrency
        self.spreadNotation = spreadNotation


class OriginatingPackage(BaseElement):
    packageIdentifier: PackageIdentifier

    def __init__(self, packageIdentifier: PackageIdentifier) -> None:
        self.packageIdentifier = packageIdentifier


class PartyTradeIdentifier(BaseElement):
    tradeId: str
    originatingTradeId: str
    linkId: str

    def __init__(self, tradeId: str, originatingTradeId: str, linkId: str) -> None:
        self.tradeId = tradeId
        self.originatingTradeId = originatingTradeId
        self.linkId = linkId


class RelatedParty(BaseElement):
    partyReference: Reference
    role: str

    def __init__(self, partyReference: Reference, role: str) -> None:
        self.partyReference = partyReference
        self.role = role


class SupervisoryRegistration(BaseElement):
    supervisorBody: str

    def __init__(self, supervisorBody: str) -> None:
        self.supervisorBody = supervisorBody


class ReportingRegime(BaseElement):
    supervisoryRegistration: SupervisoryRegistration
    reportingPurpose: str
    actionType: str

    def __init__(self, supervisoryRegistration: SupervisoryRegistration, reportingPurpose: str, actionType: str) -> None:
        self.supervisoryRegistration = supervisoryRegistration
        self.reportingPurpose = reportingPurpose
        self.actionType = actionType


class TimeStamps(BaseElement):
    confirmed: str
    cleared: str

    def __init__(self, confirmed: str, cleared: str) -> None:
        self.confirmed = confirmed
        self.cleared = cleared


class PartyTradeInformation(BaseElement):
    partyReference: Reference
    reportingRegime: ReportingRegime
    relatedParty: List[RelatedParty]
    category1: str
    category2: str
    category3: str
    executionVenueType: str
    confirmationMethod: str
    executionDateTime: str
    timeStamps: TimeStamps
    intentToClear: str
    clearingIndicator: str
    collateralizationType: str
    collateralPortfolioIndicator: str
    collateralPortfolio: str
    collateralPortfolio2: str
    marginRequiredForNonCca: str
    embeddedOptionIndicator: str

    def __init__(self, partyReference: Reference, reportingRegime: ReportingRegime, relatedParty: List[RelatedParty], category1: str, category2: str, category3: str, executionVenueType: str, confirmationMethod: str, executionDateTime: str, timeStamps: TimeStamps, intentToClear: str, clearingIndicator: str, collateralizationType: str, collateralPortfolioIndicator: str, collateralPortfolio: str, collateralPortfolio2: str, marginRequiredForNonCca: str, embeddedOptionIndicator: str) -> None:
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


class ProductSummary(BaseElement):
    productCodeFss: str
    productName: str
    relatedProductCode: str
    productId: str
    assetClass: str
    instrumentType: str
    exerciseStyle: str
    optionType: str
    pricingMethod: str
    notionalSchedule: str
    singleOrMultipleCurrency: str
    singleOrMultipleTenor: str
    contractType: NonMarketableAssetType
    contractSubType: NonMarketableAssetType
    seniority: str
    settlementType: str
    settlementCurrency: str

    def __init__(self, productCodeFss: str, productName: str, relatedProductCode: str, productId: str, assetClass: str, instrumentType: str, exerciseStyle: str, optionType: str, pricingMethod: str, notionalSchedule: str, singleOrMultipleCurrency: str, singleOrMultipleTenor: str, contractType: NonMarketableAssetType, contractSubType: NonMarketableAssetType, seniority: str, settlementType: str, settlementCurrency: str) -> None:
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


class TradeHeader(BaseElement):
    partyTradeIdentifier: PartyTradeIdentifier
    partyTradeInformation: PartyTradeInformation
    productSummary: ProductSummary
    originatingPackage: OriginatingPackage

    def __init__(self, partyTradeIdentifier: PartyTradeIdentifier, partyTradeInformation: PartyTradeInformation, productSummary: ProductSummary, originatingPackage: OriginatingPackage) -> None:
        self.partyTradeIdentifier = partyTradeIdentifier
        self.partyTradeInformation = partyTradeInformation
        self.productSummary = productSummary
        self.originatingPackage = originatingPackage


class Trade(BaseElement):
    agreementDate: str
    earlyTerminationDate: str
    tradeHeader: TradeHeader
    calculationAgent: CalculationAgent
    documentation: Documentation
    additionalPayment: AdditionalPayment
    irSwap: IRSwap

    def __init__(self, agreementDate: str, earlyTerminationDate: str, tradeHeader: TradeHeader, calculationAgent: CalculationAgent, documentation: Documentation, additionalPayment: AdditionalPayment, irSwap: IRSwap) -> None:
        self.agreementDate = agreementDate
        self.earlyTerminationDate = earlyTerminationDate
        self.tradeHeader = tradeHeader
        self.calculationAgent = calculationAgent
        self.documentation = documentation
        self.additionalPayment = additionalPayment
        self.irSwap = irSwap


class KtrRequestReport(BaseElement):
    header: Header
    trade: Trade
    party: List[Party]

    def __init__(self, header: Header, trade: Trade, party: List[Party]) -> None:
        self.header = header
        self.trade = trade
        self.party = party


class Welcome2:
    ktrRequestReport: KtrRequestReport

    def __init__(self, ktrRequestReport: KtrRequestReport) -> None:
        self.ktrRequestReport = ktrRequestReport

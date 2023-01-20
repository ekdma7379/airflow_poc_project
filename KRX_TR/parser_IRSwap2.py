from typing import Dict, Optional, List
from xml.etree.ElementTree import Element, SubElement, ElementTree
from KRX_TR.model import model_base
from model import model_base, model_IRSwap

def _pretty_print(current, parent=None, index=-1, depth=0):
    for i, node in enumerate(current):
        _pretty_print(node, current, i, depth + 1)
    if parent is not None:
        if index == 0:
            parent.text = '\n' + ('\t' * depth)
        else:
            parent[index - 1].tail = '\n' + ('\t' * depth)
        if index == len(parent) - 1:
            current.tail = '\n' + ('\t' * (depth - 1))

if __name__=='__main__':
    ## HEADER 부분 정의
    header_IRSwap = model_base.header(version="(버전)"
                                      ,memberId="(회원ID)"
                                      ,submissionDate="(제출일자)"
                                      ,messageClassificationId="(전문분류ID)"
                                      ,localeCode="(로케일구분코드)"
                                      ,reportingMethodCode="(작성방식)"
                                      ,reportingAccountNo="(보고용계좌번호)"
                                      ,reportingReferenceCode="(보고참조코드)"
                                      )
    ## HEADER 부분 정의 END
    ## TRADE 부분 정의
    
    
    list_trade_party = []
    trade_ClearingMember = model_base.RelatedParty(partyReference=model_base.PartyReference(href="ClearingMember")
                                                  ,role="ClearingClient")
    trade_CCP = model_base.RelatedParty(partyReference=model_base.PartyReference(href="CCP")
                                                  ,role="ClearingOrganization")
    trade_ExecutionVenue = model_base.RelatedParty(partyReference=model_base.PartyReference(href="ExecutionVenue")
                                                  ,role="ExecutionEntity")
    trade_Beneficiary = model_base.RelatedParty(partyReference=model_base.PartyReference(href="Beneficiary")
                                                  ,role="Beneficiary")
    trade_Broker = model_base.RelatedParty(partyReference=model_base.PartyReference(href="Broker")
                                                  ,role="Broker")
    trade_TradeParty2 = model_base.RelatedParty(partyReference=model_base.PartyReference(href="TradeParty2")
                                                  ,role="Counterparty")
    trade_TradeParty1 = model_base.RelatedParty(partyReference=model_base.PartyReference(href="TradeParty1")
                                                  ,role="ContractualParty")
    trade_ReportingEntity = model_base.RelatedParty(partyReference=model_base.PartyReference(href="ReportingEntity")
                                                  ,role="ReportingParty")
    trade_DataSubmitter = model_base.RelatedParty(partyReference=model_base.PartyReference(href="DataSubmitter")
                                                  ,role="DataSubmitter")
    list_trade_party.append(trade_ClearingMember)
    list_trade_party.append(trade_CCP)
    list_trade_party.append(trade_ExecutionVenue)
    list_trade_party.append(trade_Beneficiary)
    list_trade_party.append(trade_TradeParty2)
    list_trade_party.append(trade_Broker)
    list_trade_party.append(trade_TradeParty1)
    list_trade_party.append(trade_ReportingEntity)
    list_trade_party.append(trade_DataSubmitter)
    
    trade_supervisoryRegistration = model_base.SupervisoryRegistration(supervisorBody="KRX-TR")
    trade_reportingRegime = model_base.ReportingRegime(supervisoryRegistration=trade_supervisoryRegistration
                                                       ,reportingPurpose="T(거래정보유형)"
                                                       ,actionType="(입력유형)")
    trade_partyTradeInformation=model_base.PartyTradeInformation(partyReference=model_base.PartyReference(href="ReportingEntity")
                                                                 ,reportingRegime=trade_reportingRegime
                                                                 ,relatedParty=list_trade_party
                                                                 ,category1="(고유/신탁구분)"
                                                                 ,category2="(그룹내거래)"
                                                                 ,category3="(본지점거래)"
                                                                 ,executionVenueType="(거래플랫폼유형)"
                                                                 ,confirmationMethod="(거래확인방법)"
                                                                 ,executionDateTime="(거래일시)"
                                                                 ,timeStamps=model_base.TimeStamps(confirmed="(거래확인일시)"
                                                                                                   ,cleared="(청산일시)")
                                                                 ,intentToClear="(의무청산여부)"
                                                                 ,clearingIndicator="(청산여부)"
                                                                 ,collateralizationType="(담보유형)"
                                                                 ,collateralPortfolioIndicator="(포트폴리오담보여부)"
                                                                 ,collateralPortfolio="(포트폴리오담보코드1)"
                                                                 ,collateralPortfolio2="(포트폴리오담보코드2)"
                                                                 ,marginRequiredForNonCca="(비청산증거금적용대상여부)"
                                                                 ,embeddedOptionIndicator="(내재옵션여부)"
                                                                 )
    trade_partyTradeIdentifier=model_base.PartyTradeIdentifier(tradeId="(고유거래식별기호)"
                                                        ,originatingTradeId="(원고유거래식별기호)"
                                                        ,linkId="(거래참조코드)")
    trade_tradeheader = model_base.TradeHeader(partyTradeIdentifier=trade_partyTradeIdentifier
                                               ,partyTradeInformation=trade_partyTradeInformation)
    trade_IRSwap = model_base.trade(agreementDate="(계약변경일)"
                                    ,earlyTerminationDate="(조기종료일)"
                                    ,tradeHeader=trade_tradeheader)
    ## TARDE 부분 정의 END
    
    ## PARTY 부분 정의
    party_ReportingEntity = model_base.party(id="ReportingEntity"
                              , partyId="(보고의무자ID)")
    party_DataSubmitter = model_base.party(id="DataSubmitter"
                                           ,partyId="(보고자ID)")
    party_TradeParty1 = model_base.party(id="TradeParty1"
                                         ,partyId="(거래당사자1ID)")
    ## TODO : Contactinfo와 같이 다계층 구조 INIT 부분 수정해야함
    party_TradeParty2 = model_base.party(id="TradeParty2"
                                         ,partyIdPrefix="(거래당사자2IDPrefix)"
                                         ,partyId="(거래당사자2ID)"
                                         ,name="(거래당사자2명칭)"
                                         ,country="(거래당사자2소재지-국가)"
                                         ,contactInfo=model_base.contactInfo(address=model_base.address(postalCode="(거래당사자2소재지-우편번호)"))
                                         ,koreanResidency="(거래당사자2거주구분)")
    party_Beneficiary = model_base.party(id="Beneficiary"
                                         ,partyIdPrefix="(수익자IDPrefix)"
                                         ,partyId="(수익자ID)")
    party_Broker = model_base.party(id="Broker"
                                    ,partyId="(중개회사ID)")
    party_CalculationAgent = model_base.party(id="CalculationAgent"
                                              ,partyId="(계산대리인ID)")
    party_ExecutionVenue = model_base.party(id="ExecutionVenue"
                                            ,partyIdPrefix="(거래플랫폼IDPrefix)"
                                            ,partyId="ExecutionVenue")
    party_CCP = model_base.party(id="CCP"
                                 ,partyId="(청산회사ID)")
    party_ClearingMember = model_base.party(id="ClearingMember"
                                      ,partyId="(청산회원ID)")
    ## PARTY 부분 정의 END
    ## PARTY 부분 append
    list_party = []
    list_party.append(party_ReportingEntity)
    list_party.append(party_DataSubmitter)
    list_party.append(party_TradeParty1 )
    list_party.append(party_TradeParty2 )
    list_party.append(party_Beneficiary )
    list_party.append(party_Broker )
    list_party.append(party_CalculationAgent )
    list_party.append(party_ExecutionVenue )
    list_party.append(party_CCP )
    list_party.append(party_ClearingMember )
    ## PARTY 부분 append END
    
    ## REQUEST 정의 부분
    request = model_base.ktrRequestReport(header=header_IRSwap
                                          ,trade=trade_IRSwap
                                          ,party=list_party)
    ## REQUEST 정의 부분 END
    
    xml_request = request.objtoxml()
    _pretty_print(xml_request)
    tree = ElementTree(xml_request)
    filedest = "/app/KRX_TR/KRX_TR IRSwapTemplate_v3.0_IRSwap.xml"
    with open(filedest, "wb") as f:
        tree.write(f, encoding="utf-8")
    
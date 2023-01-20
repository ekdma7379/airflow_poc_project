from typing import Dict, Optional, List
from xml.etree.ElementTree import Element, SubElement, ElementTree
from KRX_TR.model import model_base
from model import model_base, model_Valuation

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
    header_Valuation = model_base.header(version="(버전)"
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
    trade_TradeParty2 = model_base.RelatedParty(partyReference=model_base.PartyReference(href="TradeParty2")
                                                  ,role="Counterparty")
    trade_TradeParty1 = model_base.RelatedParty(partyReference=model_base.PartyReference(href="TradeParty1")
                                                  ,role="ContractualParty")
    trade_DataSubmitter = model_base.RelatedParty(partyReference=model_base.PartyReference(href="DataSubmitter")
                                                  ,role="DataSubmitter")
    list_trade_party.append(trade_TradeParty2)
    list_trade_party.append(trade_TradeParty1)
    list_trade_party.append(trade_DataSubmitter)
    
    trade_supervisoryRegistration = model_base.SupervisoryRegistration(supervisorBody="KRX-TR")
    trade_reportingRegime = model_base.ReportingRegime(supervisoryRegistration=trade_supervisoryRegistration
                                                       ,reportingPurpose="T(거래정보유형)"
                                                       ,actionType="(입력유형)")
    trade_partyTradeInformation=model_base.PartyTradeInformation(reportingRegime=trade_reportingRegime
                                                                 ,relatedParty=list_trade_party
                                                                 ,category1="(고유/신탁구분)"
                                                                 )
    trade_partyTradeIdentifier=model_base.PartyTradeIdentifier(tradeId="(고유거래식별기호)")
    trade_tradeheader = model_base.TradeHeader(partyTradeIdentifier=trade_partyTradeIdentifier
                                               ,partyTradeInformation=trade_partyTradeInformation)
    trade_IRSwap = model_base.trade(tradeHeader=trade_tradeheader)
    ## TARDE 부분 정의 END
    ## valuationSet 부분 정의
    
    valu_TradeValuationItem = model_Valuation.TradeValuationItem(trade=trade_IRSwap
                                                           ,valuationCfd=model_Valuation.ValuationCFD(buy=model_Valuation.Buy(amount="(당일 매수금액)"
                                                                                                                              ,quantity="(당일 매수수량)"
                                                                                                                              ,price="(당일 가중평균 매수가격)")
                                                                                                      ,sell=model_Valuation.Sell(amount="(당일 매도금액)"
                                                                                                                                 ,quantity="(당일 매도수량)"
                                                                                                                                 ,price="(당일 가중평균 매도가격)"))
                                                           ,valuationSet=model_Valuation.ValuationSet(model_Valuation.AssetValuation(quote=model_Valuation.Quote(value="(평가가치)"
                                                                                                                                                                 ,currency="(가치평가통화)"
                                                                                                                                                                 ,valuationDate="(가치평가일)"
                                                                                                                                                                 ,valuationMethod="(가치평가방법)"))))
    ## valuationSet 부분 정의 END
    ## PARTY 부분 정의
    party_DataSubmitter = model_base.party(id="DataSubmitter"
                                           ,partyId="(보고자ID)")
    party_TradeParty1 = model_base.party(id="TradeParty1"
                                         ,partyId="(거래당사자1ID)")
    ## TODO : Contactinfo와 같이 다계층 구조 INIT 부분 수정해야함
    party_TradeParty2 = model_base.party(id="TradeParty2"
                                         ,partyIdPrefix="(거래당사자2IDPrefix)"
                                         ,partyId="(거래당사자2ID)")
    ## PARTY 부분 정의 END
    ## PARTY 부분 append
    list_party = []
    list_party.append(party_DataSubmitter)
    list_party.append(party_TradeParty1 )
    list_party.append(party_TradeParty2 )
    ## PARTY 부분 append END
    
    ## REQUEST 정의 부분
    request = model_Valuation.KtrRequestReport(header=header_Valuation
                                          ,tradeValuationItem=valu_TradeValuationItem
                                          ,party=list_party)
    ## REQUEST 정의 부분 END
    
    xml_request = request.objtoxml()
    _pretty_print(xml_request)
    tree = ElementTree(xml_request)
    filedest = "/app/KRX_TR/KRX_TR IRSwapTemplate_v3.0_Valuation.xml"
    with open(filedest, "wb") as f:
        tree.write(f, encoding="utf-8")
    
from typing import Dict, Optional, List
from xml.etree.ElementTree import Element, SubElement, ElementTree

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

class baseElement:
    _attr : Dict[str, str]
#    def to_xml_element(self):
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
                    root.append(item.objtoxml())
            elif baseElement in type(value).mro():
                temp = value.objtoxml()
                root.append(temp)
            else:
                root.append(Element(key, text= value))
        return root
    
class Address(baseElement):
    postalCode: str

    def __init__(self, postalCode: str= "TestCode") -> None:
        super().__init__()
        self.postalCode = postalCode


class ContactInfo(baseElement):
    address: Address

    def __init__(self, address: Address= Address()) -> None:
        super().__init__()
        self.address = address        
        
class Party(baseElement):
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



if __name__=='__main__':
    _party = Party(id="ReportingEntity"
                 , partyId="(보고의무자ID)"
                 , contactInfo = ContactInfo()
                 , partyIdPrefix="(거래당사자2IDPrefix)")
    _party_xml = _party.objtoxml()
    root = Element("ktrRequestReport")
    root.append(_party_xml)
    _pretty_print(_party_xml)
    tree = ElementTree(root)
    filedest = "/app/KRX_TR/KRX_TR IRSwapTemplate_v3.0_testresult.xml"
    with open(filedest, "wb") as f:
        tree.write(f, encoding="utf-8")
    
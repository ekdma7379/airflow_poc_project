import xmltodict, json, dicttoxml
from xml.dom.minidom import parseString

xmlfile_from = "/app/KRX_TR/KRX_TR IRSwapTemplate_v3.0.xml"
xmlfile_dest = "/app/KRX_TR/KRX_TR IRSwapTemplate_v3.0_result.xml"

with open(xmlfile_from) as fd:
    doc = xmltodict.parse(fd.read())
    json_type = json.dumps(doc)
    dict2_type = json.loads(json_type)

xml = dicttoxml.dicttoxml(dict2_type)

dom = parseString(xml)
with open(xmlfile_dest, 'w') as ofh:
    print(dom.toprettyxml(indent='  '), file=ofh)
 
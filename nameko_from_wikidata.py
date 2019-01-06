from xml.etree.ElementTree import SubElement, parse
from bs4 import BeautifulSoup
import requests

#f = open("html.html", 'w', encoding='UTF8')

xmldoc = parse("Before.osm")
root = xmldoc.getroot()

def get_html(url):
   _html = ""
   resp = requests.get(url)
   #print(resp.url)
   if resp.status_code == 200:
      _html = resp.text
   return _html
   
def remove_bracket(str):
	_str = ""
	count = 0
	str_list = list(str)
	
	for char in str_list:
		count += 1
		if char == "(":
			count -= 1
			break
	
	for char in str_list:
		count -= 1
		_str = _str + char
		if count == 0:
			break
	
	return _str


for node in root.findall("node"):
	name_ko = ""
	name_ko_value = ""
	wikidata = ""
	wikidata_value = ""
	name_from_wikidata = ""
	
	for tag in node.iter("tag"):
		if tag.attrib["k"] == "name:ko":
			name_ko = tag
			name_ko_value = name_ko.attrib["v"]
			print("name_ko: " + str(name_ko))
			print("name_ko_value: " + name_ko_value)
		if tag.attrib["k"] == "wikidata":
			wikidata = tag
			wikidata_value = wikidata.attrib["v"]
			print("wikidata: " + str(wikidata))
			print("wikidata: " + wikidata_value)
	
	if wikidata != "":
		#print("https://www.wikidata.org/wiki/" + wikidata)
		html = get_html("https://www.wikidata.org/wiki/" + wikidata_value)
		soup = BeautifulSoup(html, 'html.parser')
		#print(soup.find("a",{"hreflang": "ko"}))
		
		if soup.find("a",{"hreflang": "ko"}) != None:
			name_from_wikidata = soup.find("a",{"hreflang": "ko"}).string
			name_from_wikidata = name_from_wikidata.replace(" ", "")
			name_from_wikidata = remove_bracket(name_from_wikidata)
			print("name_from_wikidata: " + name_from_wikidata)
			
			if name_ko == "":
				element_name_ko = SubElement(node, "tag")
				element_name_ko.attrib["k"] = "name:ko"
				element_name_ko.attrib["v"] = name_from_wikidata
				print("element_name_ko.attrib['v']: " + element_name_ko.attrib["v"] + "\n\n")
				
				node.attrib["action"] = "modify"
				
				element_name_ko = ""
				
			else:
				if name_ko_value != name_from_wikidata:
					name_ko.attrib["v"] = name_from_wikidata
					print("name_ko.attrib['v']: " + name_ko.attrib["v"] + "\n")
					
					node.attrib["action"] = "modify"
				else:
					print("\n")
			
		else:
			print("name_from_wikidata: None\n\n")
		
xmldoc.write("After.osm", encoding="utf-8", xml_declaration=True)

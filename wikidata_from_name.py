from xml.etree.ElementTree import SubElement, parse
from bs4 import BeautifulSoup
import requests

xmldoc = parse("Before.osm")
root = xmldoc.getroot()

def get_html(url):
   _html = ""
   resp = requests.get(url)
   #print(resp.url)
   if resp.status_code == 200:
      _html = resp.text
   return _html

def extract_wikidata(href):
	count = -1
	_href = ""
	href_list = list(href)
	
	for char in href_list:
		count += 1
		if char == "Q":
			break
	
	for char in href_list:
		count -= 1
		if count <= -1:
			_href = _href + char
	
	return _href
			

for node in root.findall("node"):
	name = ""
	name_value = ""
	wikidata = ""
	wikidata_value = ""
	wikidata_from_name = ""
	href_from_name = ""
	list_name_value = []

	for tag in node.iter("tag"):
		if tag.attrib["k"] == "name":
			name = tag
			name_value = name.attrib["v"]
			list_name_value = list(name_value)
			print("name: " + str(name))
			print("name_value: " + name_value)
		if tag.attrib["k"] == "wikidata":
			wikidata = tag
			wikidata_value = wikidata.attrib["v"]
			print("wikidata: " + str(wikidata))
			print("wikidata: " + wikidata_value)
	
	if wikidata == "" and list_name_value != [] and list_name_value[-1] != "동":
		html = get_html("https://ko.wikipedia.org/w/index.php?title=" + name_value + "&redirect=no")
		soup = BeautifulSoup(html, 'html.parser')
		
		if soup.find("a",{"accesskey": "g"}) != None and soup.find("a",{"title": "분류:동음이의어 문서"}) == None:
			url_from_name = soup.find("a",{"accesskey": "g"})["href"]
			#print(url_from_name)
			wikidata_from_name = extract_wikidata(url_from_name)
			
			if wikidata_from_name != "Q5296":
				element_wikidata = SubElement(node, "tag")
				element_wikidata.attrib["k"] = "wikidata"
				element_wikidata.attrib["v"] = wikidata_from_name
				print("element_wikidata.attrib['v']: " + element_wikidata.attrib["v"] + "\n\n")
				
				node.attrib["action"] = "modify"
				
				element_wikidata = ""
		else:
			print("wikidata_from_name: Not one\n\n")
	else:
		print("\n")

xmldoc.write("After.osm", encoding="utf-8", xml_declaration=True)
from xml.etree.ElementTree import SubElement, parse

xmldoc = parse("Before.osm")
root = xmldoc.getroot()

def remove_bracket(str):
	_str = ""
	_name_en = ""
	count = 0
	str_list = list(str)
	
	for char in str_list:
		count += 1
		if char == "(":
			count -= 1
			break
	
	for char in str_list:
		count -= 1
		if count >= 0:
			_str = _str + char
		
		if count <= -2:
			_name_en = _name_en + char
	
	_name_en_list = list(_name_en)
	_name_en_list.pop(-1)
	_name_en = "".join(_name_en_list)
	
	_str = _str.strip()
	return [_str, _name_en]

for node in root.findall("node"):
	name = ""
	name_value = ""
	name_ko = ""
	name_ko_value = ""
	source = ""
	source_value = ""
	ncat = ""
	ncat_value = ""
	
	for tag in node.iter("tag"):
		if tag.attrib["k"] == "name":
			name = tag
			name_value = name.attrib["v"]
			print("name: " + str(name))
			print("name_value: " + name_value)
			
		if tag.attrib["k"] == "name:ko":
			name_ko = tag
			name_ko_value = name_ko.attrib["v"]
			print("name_ko: " + str(name_ko))
			print("name_ko_value: " + name_ko_value)
			
		if tag.attrib["k"] == "name:en":
			name_en = tag
			name_en_value = name_en.attrib["v"]
			print("name_en: " + str(name_en))
			print("name_en_value: " + name_en_value)
		
		if tag.attrib["k"] == "source":
			source = tag
			source_value = source.attrib["v"]
			print("source: " + str(source))
			print("source_value: " + source_value)
	
		if tag.attrib["k"] == "ncat":
			ncat = tag
			ncat_value = ncat.attrib["v"]
			print("ncat: " + str(ncat))
			print("ncat_value: " + ncat_value)
	
	if name != "" and ncat != "" and list(name_value)[0] != "(" and list(name_value)[-1] == ")":
		list1 = remove_bracket(name_value)
		name_value = list1[0]
		name_en_value = list1[1]
		list1 = []
		print("name_value(Modified): " + name_value)
		print("name_en_value(Parsed): " + name_en_value)
		
		if name_en == "":
			element_name_en = SubElement(node, "tag")
			element_name_en.attrib["k"] = "name:en"
			element_name_en.attrib["v"] = name_en_value
			print("element_name_en.attrib['v']: " + element_name_en.attrib["v"])
			
			node.attrib["action"] = "modify"
		else:
			name_en.attrib["v"] = name_en_value
			print("name_en.attrib['v']: " + name_en.attrib["v"])
			
			node.attrib["action"] = "modify"
			
		if name_ko == "":
			element_name_ko = SubElement(node, "tag")
			element_name_ko.attrib["k"] = "name:ko"
			element_name_ko.attrib["v"] = name_value
			print("element_name_ko.attrib['v']: " + element_name_ko.attrib["v"])
			
			node.attrib["action"] = "modify"
		else:
			name_ko.attrib["v"] = name_value
			print("name_ko.attrib['v']: " + name_ko.attrib["v"])
			
			node.attrib["action"] = "modify"
		
		name.attrib["v"] = name_value
		print("name.attrib['v']: " + name.attrib["v"])
		
		#node.attrib["action"] = "modify"
		
		element_name_ko = ""
		print("\n\n")
'''
for way in root.findall("way"):
	name = ""
	name_value = ""
	name_ko = ""
	name_ko_value = ""
	source = ""
	source_value = ""
	ncat = ""
	ncat_value = ""
	
	for tag in way.iter("tag"):
		if tag.attrib["k"] == "name":
			name = tag
			name_value = name.attrib["v"]
			print("name: " + str(name))
			print("name_value: " + name_value)
			
		if tag.attrib["k"] == "name:ko":
			name_ko = tag
			name_ko_value = name_ko.attrib["v"]
			print("name_ko: " + str(name_ko))
			print("name_ko_value: " + name_ko_value)
			
		if tag.attrib["k"] == "name:en":
			name_en = tag
			name_en_value = name_en.attrib["v"]
			print("name_en: " + str(name_en))
			print("name_en_value: " + name_en_value)
		
		if tag.attrib["k"] == "source":
			source = tag
			source_value = source.attrib["v"]
			print("source: " + str(source))
			print("source_value: " + source_value)
		
		if tag.attrib["k"] == "ncat":
			ncat = tag
			ncat_value = ncat.attrib["v"]
			print("ncat: " + str(ncat))
			print("ncat_value: " + ncat_value)
	
	if name != "" and ncat != "":
		if list(name_value)[0] != "(" and list(name_value)[-1] == ")":
			list1 = remove_bracket(name_value)
			name_value = list1[0]
			name_en_value = list1[1]
			list1 = []
			print("name_value(Modified): " + name_value)
			print("name_en_value(Parsed): " + name_en_value)
		
		if name_en == "":
			element_name_en = SubElement(way, "tag")
			element_name_en.attrib["k"] = "name:en"
			element_name_en.attrib["v"] = name_en_value
			print("element_name_en.attrib['v']: " + element_name_en.attrib["v"])
			
			way.attrib["action"] = "modify"
		else:
			name_en.attrib["v"] = name_en_value
			print("name_en.attrib['v']: " + name_en.attrib["v"])
			
			way.attrib["action"] = "modify"
		
		if name_ko == "":
			element_name_ko = SubElement(way, "tag")
			element_name_ko.attrib["k"] = "name:ko"
			element_name_ko.attrib["v"] = name_value
			print("element_name_ko.attrib['v']: " + element_name_ko.attrib["v"])
			
			way.attrib["action"] = "modify"
		else:
			name_ko.attrib["v"] = name_value
			print("name_ko.attrib['v']: " + name_ko.attrib["v"])
			
			way.attrib["action"] = "modify"
		
		name.attrib["v"] = name_value
		print("name.attrib['v']: " + name.attrib["v"])
		
		#way.attrib["action"] = "modify"
		
		element_name_ko = ""
		print("\n\n")
'''
xmldoc.write("After.osm", encoding="utf-8", xml_declaration=True)
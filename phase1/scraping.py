import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

url = 'https://www.toptools4learning.com/'

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
table = soup.find('table')

tbody = table.find_all('tbody')
tools_list = {}
for data in tbody:
    tr = data.find_all('tr')
    for row in tr:
        tool = row.find_all('td')
        title = None
        for value in tool:
            title_node = value.find('a')
            if title_node != None:
                
                title = title_node.text.strip()
                tools_list[title] = {}
                tools_list[title]['title'] = title
                tools_list[title]['href'] = title_node.get('href')
        if title == None:
            continue
        else:
            tools_list[title]['position'] = tool[0].text.strip()
            tools_list[title]['change'] = tool[1].text.strip()
            tools_list[title]['category'] = tool[3].text.strip()

root = Element('tools')
for value in tools_list.keys():
    child = SubElement(root, 'tool')
    child_title = SubElement(child, 'title')
    child_title.text = tools_list[value]['title']
    child_position = SubElement(child, 'position')
    child_position.text = tools_list[value]['position']
    child_href = SubElement(child, 'href')
    child_href.text = tools_list[value]['href']
    child_change = SubElement(child, 'change')
    child_change.text = tools_list[value]['change']
    child_category = SubElement(child, 'category')
    child_category.text = tools_list[value]['category']
    
xml_file = open("tools.xml", "w")
xml_file.write(minidom.parseString(tostring(root)).toprettyxml(indent="   "))
xml_file.close()



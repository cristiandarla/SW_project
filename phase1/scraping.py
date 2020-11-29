import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
URL = 'https://www.toptools4learning.com/'

req = requests.get(URL)
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

                URL = title_node.get('href')
                req = requests.get(URL)
                soup = BeautifulSoup(req.text, 'html.parser')
                div = soup.find('div', {"id" : "rml_free_content"})
                if div != None:
                    link = div.find('a')
                    if link == None:
                        tools_list[title]['href'] = URL
                    else:
                        tools_list[title]['href'] = "http://www." + link.text.strip()
                else:
                    tools_list[title]['href'] = URL
        if title == None:
            continue
        else:
            tools_list[title]['position'] = tool[0].text.strip()
            tools_list[title]['change'] = tool[1].text.strip()
            tools_list[title]['category'] = tool[3].text.strip()
            if tool[4].text.strip() != "" or tool[5].text.strip() != "":
                tools_list[title]['learning'] = "True"
            else:
                tools_list[title]['learning'] = "False"
            if tool[6].text.strip() != "":
                tools_list[title]['teaching'] = "True"
            else:
                tools_list[title]['teaching'] = "False"


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
    child_learning = SubElement(child, 'learning')
    child_learning.text = tools_list[value]['learning']
    child_teaching = SubElement(child, 'teaching')
    child_teaching.text = tools_list[value]['teaching']
    
xml_file = open(dir_path + "\\tools.xml", "w")
xml_file.write(minidom.parseString(tostring(root)).toprettyxml(indent="   "))
xml_file.close()



from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from tools import Tool
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

app = Flask(__name__)
categories = []

@app.route('/home')
def index():
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tree = ET.parse(dir_path + "\\tools.xml")
    root = tree.getroot()
    tools = []
    categories = []
    for tool in root.findall('./tool'):
        title = tool[0].text
        position = tool[1].text
        href = tool[2].text
        change = tool[3].text
        category = tool[4].text
        if tool[5].text == "True":
            learning = True
        else:
            learning = False
        if tool[6].text == "True":
            teaching = True
        else:
            teaching = False
        newTool = Tool(title, position, href, change, category, learning, teaching)
        tools.append(newTool)
        if category not in categories:
            categories.append(category)
    sorted_categories = sorted(categories, key=str.casefold)
    return render_template('index.html', tools = tools, categories = sorted_categories)

@app.route('/new', methods=['GET', 'POST'])
def new():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tree = ET.parse(dir_path + "\\tools.xml")
    root = tree.getroot()
    if request.method == "POST":
        position = len(root.findall('./tool'))
        addTool(root, request, position + 1, dir_path)
        xml_file = open(dir_path + "\\tools.xml", "w")
        xml_file.write(minidom.parseString(ET.tostring(root)).toprettyxml(indent="   "))
        xml_file.close()
        return redirect(url_for('index'))
    categories = []
    for tool in root.findall('./tool'):
        category = tool[4].text
        if category not in categories:
            categories.append(category)
    sorted_categories = sorted(categories, key=str.casefold)
    return render_template('new_tool.html', categories = sorted_categories)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('login.html')

def addTool(root, request, position, dir_path):
    child = ET.Element('tool')
    child_title = ET.SubElement(child, 'title')
    child_title.text = request.form.get('title')
    child_position = ET.SubElement(child, 'position')
    child_position.text = str(position) 
    child_href = ET.SubElement(child, 'href')
    child_href.text = "http://" + request.form.get('webAddress')
    child_change = ET.SubElement(child, 'change')
    child_change.text = "NEW"
    child_category = ET.SubElement(child, 'category')
    child_category.text = request.form.get('category')
    child_learning = ET.SubElement(child, 'learning')
    child_learning.text = str(not request.form.get('learning') == None) 
    child_teaching = ET.SubElement(child, 'teaching')
    child_teaching.text = str(not request.form.get('teaching') == None )
    root.insert(position - 1, child)
    
    
if __name__ == "__main__":
        app.run(debug=True)
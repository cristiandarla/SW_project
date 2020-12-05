from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from tools import Tool
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import date
import datetime
import lxml.etree as ET2
import os

app = Flask(__name__)
categories = []

@app.route('/home')
def index():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #dom = ET2.parse(dir_path + "\\tools.xml")
    #xslt = ET2.parse(dir_path + "\\template.xsl")
    #transform = ET2.XSLT(xslt)
    #newdom = transform(dom)
    #xml_file = open(dir_path + "\\templates\\file.html", "w")
    #xml_file.write(str(ET2.tostring(newdom)))
    #xml_file.close()
    #return render_template('file.html')
    
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
        datet = tool[7].text
        subject = tool[8].text
        if tool[5].text == "True":
            learning = True
        else:
            learning = False
        if tool[6].text == "True":
            teaching = True
        else:
            teaching = False
        newTool = Tool(title, position, href, change, category, learning, teaching, datet, subject)
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
        for elem in root.iter('*'):
            if elem.text is not None:
                elem.text = elem.text.strip()
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
    options = ['general', 'engineering', 'arts']
    return render_template('new_tool.html', categories = sorted_categories, options = options)

@app.route('/about', methods=['GET', 'POST'])
def about():
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parser = ET2.XMLParser(remove_blank_text=True)
    tree = ET2.parse(dir_path + "\\tools.xml", parser)

    name = request.form.get("title","")

    result = tree.xpath('/tools/tool[title = "'+ name +'"]')
    tool = ET2.tostring(result[0], pretty_print=True)

    root = ET.fromstring(tool)

    title = root[0].text
    position = root[1].text
    href = root[2].text
    change = root[3].text
    category = root[4].text
    datet = root[7].text
    subject = root[8].text
    if root[5].text == "True":
        learning = True
    else:
        learning = False
    if root[6].text == "True":
        teaching = True
    else:
        teaching = False
    
    newTool = Tool(title, position, href, change, category, learning, teaching, datet, subject)

    return render_template('about.html', tool = newTool)

@app.route('/days', methods=['GET', 'POST'])
def days():
    if request.method == 'POST':
        days = request.form.get("days","")
        todays = date.today().strftime("%d/%m/%Y")
        todaysdate = datetime.datetime.strptime(todays, "%d/%m/%Y")
        daysformated = datetime.timedelta(int(days))
        difference = todaysdate - daysformated
        
        differencestr = difference.strftime("%d/%m/%Y")
        differencestr = differencestr.replace("/","")
        print(differencestr)
        #/tools/tool[number(translate(date,'/','')) > 03122020]

        dir_path = os.path.dirname(os.path.realpath(__file__))
        tree = ET2.parse(dir_path + "\\tools.xml")
        result = tree.xpath("/tools/tool[number(translate(date,'/','')) >= " + differencestr +"]")
        tools = []
        for t in result:
            title = t[0].text
            position = t[1].text
            href = t[2].text
            change = t[3].text
            category = t[4].text
            datet = t[7].text
            subject = t[8].text
            if t[5].text == "True":
                learning = True
            else:
                learning = False
            if t[6].text == "True":
                teaching = True
            else:
                teaching = False
            
            newTool = Tool(title, position, href, change, category, learning, teaching, datet, subject)
            tools.append(newTool)

        return render_template('listby.html', tools = tools)

    return render_template('days.html')

@app.route('/getcategory', methods=['GET', 'POST'])
def getcategory():
    if request.method == 'POST':
        categ = request.form.get("category","")
        print(categ)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        tree = ET2.parse(dir_path + "\\tools.xml")
        result = tree.xpath('/tools/tool[category = "' + categ + '"]')
        tools = []
        for t in result:
            title = t[0].text
            position = t[1].text
            href = t[2].text
            change = t[3].text
            category = t[4].text
            datet = t[7].text
            subject = t[8].text
            if t[5].text == "True":
                learning = True
            else:
                learning = False
            if t[6].text == "True":
                teaching = True
            else:
                teaching = False
            
            newTool = Tool(title, position, href, change, category, learning, teaching, datet, subject)
            tools.append(newTool)

        return render_template('listby.html', tools = tools)


    dir_path = os.path.dirname(os.path.realpath(__file__))
    tree = ET.parse(dir_path + "\\tools.xml")
    root = tree.getroot()

    categories = []
    for tool in root.findall('./tool'):
        category = tool[4].text
        if category not in categories:
            categories.append(category)
    sorted_categories = sorted(categories, key=str.casefold)

    return render_template("catform.html", categories = sorted_categories)

@app.route('/engineering', methods=['GET', 'POST'])
def engineering():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tree = ET2.parse(dir_path + "\\tools.xml")
    sub = "engineering"
    result = tree.xpath('/tools/tool[subject = "' + sub + '"]')
    tools = []
    for t in result:
        title = t[0].text
        position = t[1].text
        href = t[2].text
        change = t[3].text
        category = t[4].text
        datet = t[7].text
        subject = t[8].text
        if t[5].text == "True":
            learning = True
        else:
            learning = False
        if t[6].text == "True":
            teaching = True
        else:
            teaching = False
        
        newTool = Tool(title, position, href, change, category, learning, teaching, datet, subject)
        tools.append(newTool)

    return render_template('listby.html', tools = tools)

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
    child_date = ET.SubElement(child, 'date')
    child_date.text = date.today().strftime("%d/%m/%Y")
    child_subject = ET.SubElement(child, 'subject')
    child_subject.text = request.form.get('subject')
    root.insert(position - 1, child)
    
    
if __name__ == "__main__":
        app.run(debug=True)
import datetime
import xml.etree.ElementTree as ET
import requests

from xmlrpc.server import SimpleXMLRPCServer
#RPC function to save a new note to the XML
def save_note(topic, note, content):
    #Try the tree from the XML file
    try:
        tree = ET.parse('notebook.xml')
    #If the file doesn't exist or it's empty, create a new XMl root.
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write("notebook.xml")
    try:
        tree = ET.parse('notebook.xml')
    except:
        print("Couldn't open XML")
    root = tree.getroot()
    #Search if the topic already exists, if it does append the note to it with the write function.
    for Topic in root.iter("topic"):
        if(Topic.get("name") == topic):
            print("Topic exists, adding new note to topic")
            new_XML_note(Topic, note, content)
            tree.write("notebook.xml")
            return(1)

    #The topic didn't exist, so create a new topic with the given topic and add the note to that.
    new_topic = ET.Element("topic")
    new_topic.set("name", topic)
    new_XML_note(new_topic, note, content)
    root.append(new_topic)
    tree.write("notebook.xml")
    return(1)

#A helper function for creating new notes. The text content and timestamp are children of the note name.
def new_XML_note(Topic, note, content):
    new_note = ET.SubElement(Topic, "note")
    new_note.set("name", note)
    new_note_content = ET.SubElement(new_note, "text")
    new_note_content.text = content
    new_note_timestamp = ET.SubElement(new_note, "timestamp")
    new_note_timestamp.text = str(datetime.datetime.today())
    return new_note

#RPC function to search for notes by topic
def search_by_topic(topic):
    tree = ET.parse('notebook.xml')
    root = tree.getroot()
    #Search for the topic, if found return it as a string
    for Topic in root.iter("topic"):
        if(Topic.get("name") == topic):
            return ET.tostring(Topic)
    return("Couldn't find topic\n")

#Query wikipedia
def query_wikipedia_api(searchterm):
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": searchterm,
        "limit": "1",
        "format": "json"
    }
    request = session.get(url=URL, params=PARAMS)
    return request.json()

#Set the server to listen on 3000
server = SimpleXMLRPCServer(("localhost", 3000))
print("Listening on port 3000")
#Register the RPC functions for proxying
server.register_function(save_note, "save_note")
server.register_function(search_by_topic, "search_by_topic")
server.register_function(query_wikipedia_api, "query_wikipedia_api")
server.serve_forever()
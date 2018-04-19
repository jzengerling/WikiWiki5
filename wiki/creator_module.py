import json
from flask_login import current_user
from time import strftime

def get_page_data(url):
    jsonFile = open('creators.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    data = data[url][0]
    return data
    
def add_to_json(url):
        user = current_user.name
        now = strftime("%m-%d-%Y %H:%M:%S")
        jsonFile = open('creators.json', 'r')
        data = json.load(jsonFile)
        jsonFile.close()
        data[url] = []
        data[url].append({
            'creator': user,
            'time': now
        })
        jsonFile = open('creators.json', 'w')
        json.dump(data, jsonFile, indent=4, sort_keys=True)
        jsonFile.close()
        
def search_by_creator(pages, regex):
    matched = []
    jsonFile = open('creators.json', 'r')
    data = json.load(jsonFile)
    for page in pages:
        if regex.search(data[page.url][0]['creator']):
            matched.append(page)
                        
    return matched
    
def delete_creator_entry(url):
    jsonFile = open('creators.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    
    for dict in data:
        if(dict == url):
            data.pop(dict)
            break
    
    jsonFile = open('creators.json', 'w')		
    json.dump(data, jsonFile, indent=4, sort_keys=True)
    jsonFile.close()
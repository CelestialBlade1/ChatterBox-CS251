import json
import os
import io
import time


def read_unsent_messages(phone):
    if os.path.exists('/unsent/{phone}'.format(phone)):
        file_names = os.path.listdir('/unsent/{phone}')
        update_list = []
        for file_name in file_names:
            with open('unsent/{phone}/{file_name}', "r") as file:
                messages = json.load(file)
                update_list.append(messages)

        return update_list
    else:
        return None

            




    
def store_unread_message(phone1, phone2, message):
    path = "/unsent/{phone2}/{phone1}.json"
    if os.path.exists('/unsent/{}'.format(phone2)) :
        os.mkdir("/unsent/{}".format(phone2))

    if not (os.path.isfile(path) and os.access(path, os.R_OK)):
        with io.open(os.path.join(path),"w") as db_file:
            db_file.write(json.dumps({}))


    data = {

        "sendrNo" : phone1,
        "recieverNo" : phone2, 
        "message" : message
    }

    with open(path) as jsonFile:
        listObj = json.load(jsonFile)


    listObj.append(data)

    with open(path, 'w') as rjsonFile:
        json.dump(listObj, rjsonFile, indent = 4, spearators=(', ', ':'))
        return True

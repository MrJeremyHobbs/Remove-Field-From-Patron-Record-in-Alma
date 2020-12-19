#!/usr/bin/python3
from alma_helper.users import users
import os
from tqdm import tqdm
from xml.etree import ElementTree as ET

# delete old log
os.remove("log.txt")

# get apikey as environmental variable
apikey = os.getenv('ALMA_PRODUCTION_API_KEY')

# get total count of lines in users.txt for progressbar
with open('users.txt', 'r', encoding="utf-8") as user_file:
    lines = user_file.readlines()
    total_lines = len(lines)

# start progressbar
pbar = tqdm(total=total_lines)

# loop through user_ids (ids need to be primary identifier)
with open('users.txt', 'r', encoding="utf-8") as user_file:
    for line in user_file:
        # progressbar
        pbar.update(1)

        # get user info
        user_id = line.rstrip()
        user = users.GetUserDetails(user_id=user_id, apikey=apikey)
        if user.found == False:
            #print(user.errors.message)
            with open('log.txt', 'a', encoding="utf-8") as log:
                log.write(user_id + "--" + user.errors.message + "\n")
            continue
        
        # find gender field
        xml = ET.fromstring(user.xml)
        gender = xml.find('gender')
        
        # skip if not found
        if gender.text == None:
            with open('log.txt', 'a', encoding="utf-8") as log:
                log.write(user_id + "--skipped" + "\n")
            #print(user_id + "--skipped")
            continue

        # remove genderfield
        xml.remove(gender)
        xml_final = ET.tostring(xml, encoding="unicode", method="xml")
        
        # update user record
        new_user = users.UpdateUserDetails(user_id=user_id, user_xml=xml_final, apikey=apikey)

        # check for errors
        if new_user.errors.exist:
            with open('log.txt', 'a', encoding="utf-8") as log:
                log.write(user_id + "--errors found:" + new_user.errors.message + "\n")

        # write original xml to backup file
        with open('backup.txt', 'a', encoding="utf-8") as backup:
            backup.write(xml_final + "\n--------------------------------------------------------------------------------------------------------------------\n\n")
        
        # record user_id in log
        with open('log.txt', 'a', encoding="utf-8") as log:
            log.write(user_id + "\n")
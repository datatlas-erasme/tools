import os
import json
import requests
import time


# open the instance.json  file based on the instance name
def getInstanceJson(instance_name) :
    with open(os.path.join(ConfigsPath + sub_folders[int(instance_name)] + '/instance.json'), encoding="utf-8") as f:
        instance_json = f.read()
        return instance_json
    
# open the kepler.json file based on the instance name
def getkeplerJson(instance_name) :
    with open(os.path.join(ConfigsPath + sub_folders[int(instance_name)] + '/kepler.json'), encoding="utf-8") as f:
        kepler_json = f.read()
        return kepler_json
    

# make an api call to the server to push the conf using {instanceurl}/api/conf/kepler/ and post in body the kepler.json
def pushConf(url,token, keplerJson, instanceJson) :

    headers = {'Authorization': 'Bearer ' + token}
    files = []
    
    # push kepler conf to the server
    setkeplerRoute = url + '/api/conf/kepler/'
    print(setkeplerRoute)

    keplerData={'configuration_kepler': keplerJson}
    response = requests.request("POST",setkeplerRoute, headers=headers, data=keplerData, files=files, )
    print(response.text)
    time.sleep(3)
    # push instance conf to the server
    setInstanceRoute = url + '/api/conf/instance/'
    print(setInstanceRoute)
    instanceData={'configuration_instance': instanceJson}
    response = requests.request("POST",setInstanceRoute,  headers=headers, data=instanceData, files=files,)
    print(response.text)


ConfigsPath = './configs/'

sub_folders = [name for name in os.listdir(ConfigsPath) if os.path.isdir(os.path.join(ConfigsPath, name))]

print("Select the instance name:")

# for each folder print the name of the folder with an index
for folder in sub_folders:
    print(sub_folders.index(folder), ".", folder)

# wait for user to type a number
instance_name = input()

# get the instance.json and kepler.json files based on the instance name
instanceJson = getInstanceJson(instance_name)
keplerJson = getkeplerJson(instance_name)

backUrls = []

# open backUrls.json file and store the data in a variable
with open(os.path.join(ConfigsPath + 'backUrls.json')) as f:
    backUrls = json.load(f)


print("######################")
# for each url in backUrls print the name and url
for url in backUrls:
    print(backUrls.index(url),".", url['name'], url['url'])

# wait for user to type a number
print("Select the server to push conf to:")
server_number = input()


print("are you sure you want to push the conf ", sub_folders[int(instance_name)],"to the server :", backUrls[int(server_number)]["name"], "with url :",backUrls[int(server_number)]["url"]  ,"? (y/n)")

# wait for user to type y or n if n exit
startPush = input()
if startPush == "y":
    print("pushing conf to server")
    pushConf(backUrls[int(server_number)]["url"],backUrls[int(server_number)]["token"], keplerJson, instanceJson)
else :
    print("exiting")
    exit()



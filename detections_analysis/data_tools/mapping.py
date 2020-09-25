import json

home_detections = "/media/slawekstu/CREDO1/Api/credo-data-export/"

path_to_mapping_team = home_detections+"team_mapping.json"
path_to_mapping_user = home_detections+"user_mapping.json"
path_to_mapping_device = home_detections+"device_mapping.json"

list_mapping ={
    "teams": path_to_mapping_team,
    "users": path_to_mapping_user,
    "devices": path_to_mapping_device
}

def read_mapping(option):
    """
    :param option: what kind of mapping we are interested in
    :return:
    """
    with open(list_mapping[option]) as json_file:
        json_load = json.load(json_file)

    dict = {}
    print (len(json_load[option]))
    for record in json_load[option]:
        id = int(record["id"])
        dict[id]=record
    return dict

def join_device_user(users,devices):
    """
    join device with user
    :return:
    """
    Dictionary = {}
    for user in users:
        id = user["id"]
        name = user["display_name"]
        Dictionary[id]={}
        Dictionary[id]["name"]=name
        Dictionary[id]["device"] = {}
        Dictionary[id]["team"] = 0 #id team

    for device in devices:
        id = device["id"]
        user_id = device["user_id"]
        model = device["device_model"]
        Dictionary[user_id]["device"][id]= {}
        Dictionary[user_id]["device"][id]["model"] = model
        Dictionary[user_id]["device"][id]["ping"] = 0
        Dictionary[user_id]["device"][id]["detection"] = {}
        Dictionary[user_id]["device"][id]["detection"]["all"] = 0
        Dictionary[user_id]["device"][id]["detection"]["too_often"] = 0
        Dictionary[user_id]["device"][id]["detection"]["bad"] = 0
        Dictionary[user_id]["device"][id]["detection"]["good"] = 0

    return Dictionary

def info_team(teams):
    """
    We create a dictionary for each team, with information
    "id" - team id
    "name" - team name
    "competition" - does the team take part in the competition
    "users" - information about users, we only store id

        "All" - list of all users
        "edition" - users participating in a given edition of the competition
    :param teams: Dict with all teams
    :return: Dict of teams
    """
    Dict_teams = {}
    for team in teams:
        id = team["id"]
        name = team["name"]
        Dict_teams[id]={}
        Dict_teams[id]["name"] = name
        Dict_teams[id]["competition"] = {"1": "No", "2": "No", "3": "No"}
        Dict_teams[id]["users"] = {}
        Dict_teams[id]["devices"] = {}
        Dict_teams[id]["devices"]["All"] = []  # information from the entire working time range
        Dict_teams[id]["devices"]["edition"] = {"1": [], "2": [], "3": []}
        Dict_teams[id]["users"]["All"] = []#information from the entire working time range
        Dict_teams[id]["users"]["edition"] = {"1": [], "2": [], "3": []}

    return Dict_teams

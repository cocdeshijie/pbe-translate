import requests
import json
from fuzzywuzzy import process
import re

class data:
    def __init__(self):
        self.latest_version = json.loads(requests.get("https://ddragon.leagueoflegends.com/api/versions.json").text)[0]
        self.item_data = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + str(self.latest_version) + "/data/en_US/item.json").text)["data"]
        self.champion_data = json.loads(requests.get("http://ddragon.leagueoflegends.com/cdn/" + str(self.latest_version) + "/data/en_US/champion.json").text)["data"]
    def champion_fuzzy_list(self):
        list = []
        for champion in self.champion_data:
            list.append(champion)
        return list

    def item_fuzzy_list(self):
        list = []
        for item in self.item_data:
            list.append(self.item_data[item]["name"])
        return list


class zh_CN:
    def __init__(self, selection, input):
        self.selection = selection
        if self.selection == "英雄":
            self.input = process.extractOne(input, data().champion_fuzzy_list())[0]
            self.data_url = "http://ddragon.leagueoflegends.com/cdn/" + str(data().latest_version) + "/data/zh_CN/champion/" + self.input + ".json"
        if self.selection == "装备":
            self.input = process.extractOne(input, data().item_fuzzy_list())[0]
            self.data_url = "http://ddragon.leagueoflegends.com/cdn/" + str(data().latest_version) + "/data/zh_CN/item.json"
            for item_id, item in data().item_data.items():
                if item["name"] == self.input:
                    self.input = item_id
                    break

    def champion_data(self):
        champion_data = json.loads(requests.get(self.data_url).text)["data"][self.input]
        skins = []
        for n, skin in enumerate(champion_data["skins"]):
            skins += [champion_data["skins"][n]["name"]]
        return (
            "<h2>" + champion_data["name"] + " " + champion_data["title"] + "</h2>" +
            "<h3>" + champion_data["blurb"] + "</h3>" +
            "<h3>被动 " + champion_data["passive"]["name"] + "</h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", champion_data["passive"]["description"])) +
            "<h3>Q " + champion_data["spells"][0]["name"] + "</h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", champion_data["spells"][0]["tooltip"])) +
            "<h3>W " + champion_data["spells"][1]["name"] + "</h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", champion_data["spells"][1]["tooltip"])) +
            "<h3>E " + champion_data["spells"][2]["name"] + "</h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", champion_data["spells"][2]["tooltip"])) +
            "<h3>R " + champion_data["spells"][3]["name"] + "</h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", champion_data["spells"][3]["tooltip"])) +
            "<h3>皮肤: </h3>" +
            "<br>".join(skins)
        )

    def item_data(self):
        item_data = json.loads(requests.get(self.data_url).text)["data"][self.input]
        return (
            "<h2>" + item_data["name"] + "</h2>" +
            "<h3>" + re.sub(r'\{\{.*?\}\}', "", re.sub(r'\<.*?\>', "", item_data["description"])) + "</h3>" +
            "<h3>" + item_data["plaintext"] + "</3>"
        )



import json as js
import pandas as pd
import csv
import requests
import json


def temp_response_giver(name,url,headers):
    response = requests.get( url, headers=headers)
    response = response.json()
    with open("store/response_"+str(name)+".json",'w+') as response_saver:
        json.dump(response,response_saver)
    with open("store/response_"+str(name)+".json") as resp:
        json_response = js.load(resp)
    return json_response


def parse_to_csv_coronavirus_world(name,json_dict_try):
    count = 1 # to be later automate with dash
    column_names = list(json_dict_try['countries_stat'][0].keys())#to be later automate with dash

    # temp_list.remove('country_name')
    # counter = 0
    with open("store/parsed_"+str(name)+".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
    for each_country in json_dict_try["countries_stat"]:
        # print(each_country['country_name'])
        temp_list = [None] * (len(column_names))
        # temp_list[0] = counter
        for diff_cols in each_country:

            if diff_cols!="country_name":
                value = each_country[diff_cols].replace(',', '')
                try:
                    temp_list[column_names.index(diff_cols)] = int(value)
                except:
                    pass
            else:
                temp_list[column_names.index(diff_cols)] = each_country[diff_cols]
        with open("store/parsed_" + str(name) + ".csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow(temp_list)
        # counter+=1
    df = pd.read_csv("store/parsed_"+str(name)+".csv")
    return df


def parse_to_csv_coronavirus_india(name,json_dict_try):
    count = 2 # to be later automate with dash
    # column_names = list(json_dict_try["state_wise"][0].keys())#to be later automate with dash
    column_names = ["name","active","confirmed","deaths","recovered"]
    # temp_list.remove('country_name')
    # counter = 0
    with open("store/parsed_"+str(name)+".csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
    state_wise_dict = json_dict_try["state_wise"]
    for each_state in state_wise_dict:
        # print(each_country['country_name'])
        temp_list = [None] * (len(column_names))
        # temp_list[0] = counter
        temp_list[0] = each_state
        particular_state_dict = state_wise_dict[each_state]
        for diff_cols in particular_state_dict:
            if diff_cols in column_names:
                value = particular_state_dict[diff_cols].replace(',', '')
                try:
                    temp_list[column_names.index(diff_cols)] = int(value)
                except:
                    pass
            else:
                pass
                # temp_list[column_names.index(diff_cols)] = each_country[diff_cols]
        with open("store/parsed_" + str(name) + ".csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow(temp_list)
        # counter+=1
    df = pd.read_csv("store/parsed_"+str(name)+".csv")
    return df


def get_latest_dataframe(api_name):
    if api_name == "coronavirus_world":
        url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api"

        headers = {
            'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
            'x-rapidapi-key': "f1503f90c1msh8c6f6079c76f7f4p11da66jsneb0130349249"
        }
        json_response = temp_response_giver(api_name,url, headers)
        df = parse_to_csv_coronavirus_world(api_name,json_response)
    elif api_name == "coronavirus_india":
        url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

        headers = {
            'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
            'x-rapidapi-key': "f1503f90c1msh8c6f6079c76f7f4p11da66jsneb0130349249"
        }
        json_response = temp_response_giver(api_name,url, headers)
        df = parse_to_csv_coronavirus_india(api_name,json_response)
    return df

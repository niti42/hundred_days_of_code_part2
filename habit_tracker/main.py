import requests
import datetime

pixela_endpoint = 'https://pixe.la/v1/users'
USERNAME = 'nithish42'
TOKEN = 'afdsl1342nfnvd432'
GRAPH_ID = 'graph1'

headers = {
    "X-USER-TOKEN": TOKEN
}

# User Id creation and login - first time
# Data to be posted in json format
user_params = {
    "token": "afdsl1342nfnvd432",
    "username": "nithish42",
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)  # To tell the programmer if there is any issue with the post request


# Creating the blank pixel graph
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
graph_config = {
    "id": f"{GRAPH_ID}",
    "name": "Reading Graph",
    "unit": "Pages",
    "type": "int",
    "color": "ichou",
    "timezone": "Asia/Kolkata"
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)

# today = datetime.datetime(year=2023, month=6, day=7)
# datetime.datetime.today().strftime('%Y%m%d')

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_plot = {
    "date": datetime.datetime.now().strftime('%Y%m%d'),
    "quantity": f'{input("how many pages did you read today?:" )}',
}

# print(datetime.datetime.now().strftime('%Y%m%d'))
response = requests.post(url=pixel_creation_endpoint, json=pixel_plot, headers=headers)


update_date = datetime.datetime(year=2023, month=6, day=7).strftime('%Y%m%d')

pixel_update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{update_date}"
pixel_update = {
    "quantity": '250',
}

# response = requests.put(url=pixel_update_endpoint, json=pixel_update, headers=headers)


delete_date = datetime.datetime(year=2023, month=6, day=8).strftime('%Y%m%d')
pixel_delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{delete_date}"
# response = requests.delete(url=pixel_delete_endpoint,  headers=headers)
print(response.text)

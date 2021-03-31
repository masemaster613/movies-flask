import requests, json

url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

querystring = {"q":"get:new30:US","p":"1","t":"ns","st":"adv"}

headers = {
    'x-rapidapi-key': "a56202b91dmsh81158e9e1b233b6p1c3ae6jsn5687ad0165c3",
    'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

whole_list=json.loads(response.text)

things_to_watch = whole_list['ITEMS']

movies = []

for thing in things_to_watch:
	if thing['type'] == 'movie':
		movies.append(thing)




with open('movies.json', 'w') as f:
    json.dump(movies, f)

import bs4, requests, re, json

page = requests.get('https://www.netflix.com/browse/genre/34399')
page.raise_for_status()

soup = bs4.BeautifulSoup(page.text, 'html.parser')
links = soup.find_all('a')
print(len(links))

movies=[]
for link in links:
	if re.match(r'https://www.netflix.com/title/.*', link.get('href')):
		movies.append((link.get('href'), link.img.get('src')))

json_to_save=[]
for movie in movies:
	url = movie[0]
	page = requests.get(url)
	page.raise_for_status()

	soup = bs4.BeautifulSoup(page.text, 'html.parser')
	image = movie[1]
	title = soup.find_all(attrs={'data-uia':'title-info-title'})[0].string
	synopsis = soup.find_all(attrs={'data-uia':'title-info-synopsis'})[0].string
	released = soup.find_all(attrs={'data-uia':'item-year'})[0].string
	saver={'image':image, 'title':title, 'synopsis':synopsis, 'released':released}
	json_to_save.append(saver)

with open('netflix_movies.json', 'w') as f:
	json.dump(json_to_save, f)









# movies_info=[]
# for movie in movies:
# 	url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

# 	querystring = {"t":"loadvideo","q":movie}

# 	headers = {
# 	    'x-rapidapi-key': "a56202b91dmsh81158e9e1b233b6p1c3ae6jsn5687ad0165c3",
# 	    'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com"
# 	    }

# 	response = requests.request("GET", url, headers=headers, params=querystring)
# 	if response.text:
# 		whole_list=json.loads(response.text)
# 		movie=whole_list['RESULT']['nfinfo']
# 		movie['image']=movie['image1']
# 		movies_info.append(movie)

# with open('movies2.json', 'w') as f:
# 	json.dump(movies_info, f)

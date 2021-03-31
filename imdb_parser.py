import bs4, requests, re, json

def get_movie_by_title(title, released):
	url = 'https://www.imdb.com/find?q=' + '+'.join(title.split(' ')) + '+' + released +'&ref_=nv_sr_sm'
	page = requests.get(url)
	page.raise_for_status()
	soup = bs4.BeautifulSoup(page.text, 'html.parser')
	links = soup.find_all('a')
	for link in links:
		if link.string == title:
			return 'https://www.imdb.com' + link.get('href')

def get_movie_info(url):
	page = requests.get(url)
	page.raise_for_status()
	soup = v
	image = soup.img.get('src')
	x = []
	for string in soup.h1.strings:
		x.append(string)
	title = x[0].strip()
	released = x[2]
	synopsis = soup.find_all('div', class_='summary_text')[0].string.strip()
	rating = soup.find_all('span', itemprop='ratingValue')[0].string
	movie_info = {'title':title, 'released':released, 'synopsis':synopsis, 'image': image, 'rating':rating}
	return movie_info

def get_info_from_list(url):
	page = requests.get(url)
	page.raise_for_status()
	soup = bs4.BeautifulSoup(page.text, 'html.parser')
	links = soup.find_all('a')
	all_movies = []
	movie_links = []
	for link in links:
		if re.match('/title/[\d\w]+/$', str(link.get('href'))):
			if link.get('href') not in movie_links:
				movie_links.append(link.get('href'))
	for link_string in movie_links:
		try:
			all_movies.append(get_movie_info('https://www.imdb.com' + link_string))
			print('got one')
		except:
			print('not a movie')
	return all_movies

def get_popular_genres(genres):
	for genre in genres:
		url = 'https://www.imdb.com/search/title/?genres=' + genre + '&explore=title_type,genres&title_type=movie&ref_=adv_explore_rhs'
		genre_movies = get_info_from_list(url)
		with open('./genres/' +genre + '.json', 'w') as f:
			json.dump(genre_movies, f)
			print(genre + ' has been dumped')

def ask_for_list():
	list_page = input('what movie list? ')
	file = input('where to dump? ')

	all_movies=get_info_from_list(list_page)

	with open(file, 'w') as f:
		json.dump(all_movies, f)


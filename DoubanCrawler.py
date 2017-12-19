import requests
import expanddouban
from bs4 import BeautifulSoup
import csv




#Task 1 Get the url of pages for each distric and type


"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"+category+","+location
	return str(url)




#Task 2


html = expanddouban.getHtml(url,True)
# get the full html (incl. loadmore)in text for a indicated url.


#Task 3,4,5,6

def generate_movie_CSV(category,location=''):

	url = getMovieUrl(category,location)

	html = expanddouban.getHtml(url,True)

	soup = BeautifulSoup(html,'html.parser')

	Movie_object_list = []
	location_list = []

	for element in soup.find_all(class_='item'):
		m_object = []
		
		m_object.append(element.p.find(class_='title').get_text())
		m_object.append(element.p.find(class_='rate').get_text())

		detail_url = element.get('href')
		response = requests.get(detail_url)
		detail_html = response.text
		soup_detail = BeautifulSoup(detail_html,'html.parser')
		movie_location = soup_detail.find(id = 'info').find(text='制片国家/地区:').next_element
		m_object.append(str(movie_location).strip())
		m_object.append(category)
		m_object.append(element.get('href'))
		m_object.append(element.find('img').get('src'))
		Movie_object_list.append(m_object)
		location_list.append(str(movie_location).strip())
		
		
	with open("movies.csv","a") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(Movie_object_list)

	cnt_d = {} #def 'country_count_dict' to store country and its counts

	for country in location_list:
		cnt_d[country] = location_list.count(country)

	no_of_top1 = max(cnt_d.values())
	for x in cnt_d:
		if cnt_d[x] == no_of_top1:
			top1 = x

	
	del cnt_d[top1]

	no_of_top2 = max(cnt_d.values())
	for x in cnt_d:
		if cnt_d[x] == no_of_top2:
			top2 = x


	del cnt_d[top2]

	no_of_top3 = max(cnt_d.values())
	for x in cnt_d:
		if cnt_d[x] == no_of_top3:
			top3 = x


	no_of_all = len(location_list)

	percentage_top1 = "%.2f%%" % (no_of_top1/no_of_all * 100)
	percentage_top2 = "%.2f%%" % (no_of_top2/no_of_all * 100)
	percentage_top3 = "%.2f%%" % (no_of_top3/no_of_all * 100)

	print_text = '\nThe top 3 districts of movies in type of {} are: '.format(category)

	output_str = str(print_text)+str(top1)+', '+str(top2)+', '+str(top3)+'. \nThe percentages in all movies of list are '+str(percentage_top1)+', '+str(percentage_top2)+', '+str(percentage_top3)+'.'

	with open('output.txt','a') as output:
			output.write(output_str)

location = ''
category = '科幻' #Favorate Type 1
generate_movie_CSV(category,location)
category = '剧情' #Favorate Type 2
generate_movie_CSV(category,location)
category = '励志' #Favorate Type 3
generate_movie_CSV(category,location)

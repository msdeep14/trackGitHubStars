import urllib, urllib2, cookielib
import requests
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import re
import operator

top_limit = 9

def openWebsite():
	username = str(raw_input("enter GitHub username: "))
	repo_dict = {}
	url = "https://github.com/"+username+"?tab=repositories"
	while True:
		# print "url: ",url
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		resp = opener.open(url)
		doc = html.fromstring(resp.read())
		# print html.tostring(doc, pretty_print=True)
		repo_name = doc.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]/div[@class="d-inline-block mb-1"]/h3/a/text()')

		repo_list = []
		
		for name in repo_name:
			name = ' '.join(''.join(name).split())
			repo_list.append(name)
			repo_dict[name] = 0

		# print repo_list
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')

		soup = BeautifulSoup(response.text, 'html.parser')
		div = soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom public source'})
		# print div

		for d in div:
			temp = d.find_all('div',{'class':'f6 text-gray mt-2'})
			for t in temp:
				x = t.find_all('a', attrs={'href': re.compile("^\/[a-zA-Z0-9\-\_.]+\/[a-zA-Z0-9.\-\_]+\/stargazers")})
				if len(x) is not 0:
					name = x[0].get('href')
					name = name[len(username)+2:-11]
					repo_dict[name] = int(x[0].text)
		

		# check if next page exists for more repos
		div = soup.find('a',{'class':'next_page'})
		# print div
		if div is not None:
			url = div.get('href')
			url = "https://github.com/"+url
		else:
			break	

	# get the sorted list of all repos and print top 10
	i = 0
	sorted_repo = sorted(repo_dict.iteritems(), key = operator.itemgetter(1))
	for val in reversed(sorted_repo):
		repo_url = "https://github.com/" + username + "/" + val[0]
		print "\nrepo name : ",val[0], "\nrepo url  : ",repo_url, "\nstars     : ",val[1]
		i = i + 1
		if i > top_limit:
			break

		

if __name__ == "__main__":
	openWebsite()

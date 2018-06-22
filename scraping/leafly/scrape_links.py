from urllib.request import urlopen
from bs4 import BeautifulSoup
from math import ceil
import time
import os

# TODO: update 'explore_box' var to better name


# scrape leafly website and put all the strains in a list 
# plan: access each individual strain's site and extract all strain's info

# ------- initialized vars -------
start_time = time.time()
effects = {}
medical = {}
negatives = {}
types = {}
links = set()
# page_num = 0
# quote_page = 'https://www.leafly.com/explore/page-%d/sort-alpha' % page_num
type_set = {"{{category}}Hybrid", "{{category}}Sativa","{{category}}Indica"}

# ------- functions -------

def extract_strain_urls(links, explore_box):
	"""
	Take the "explore box" part of the leafly explore pages and extract
	the urls of the individual strains and add them to 'links'
	input: strains (lis) - master list of strains
		   explore_box (lis) - list of BeautifulSoup.Tag elements to extract 
		   					   strain names from
	output: ///

	example of the 'a' tag containing a single strain url:

	<a class="ga_Explore_Strain_Tile" href="/hybrid/100-og"> [...] </a>
	"""
	for e in explore_box:
		link = e["href"]
		links.add(link)

# ------- scrape strain urls -------
num_pages = ceil(2500 / 48) # values found manually from leafly - 2500 total strains; 48 listed per page

for i in range(num_pages):
	quote_page = 'https://www.leafly.com/explore/page-%d/sort-alpha' % i

	# open page and get page data
	page = urlopen(quote_page)

	# parse the html
	soup = BeautifulSoup(page, 'html.parser')

	# extract the tags that contain strain name info
	# found manually from leafly
	explore_box = soup.find_all('a', attrs={"class": "ga_Explore_Strain_Tile"})
	extract_strain_urls(links, explore_box)
	# break # only check one page [debug]

def write_links(links, outfile='urls.txt'):
	"""
	Take a collection of links and write them to a file for later use

	input: links (iterable) - list/set/etc of links
	output: /// 

	"""
	mode = 'a' if os.path.isfile(outfile) else 'w'

	with open(outfile, mode) as f:
		for link in links:
			f.write(link + '\n')

		f.close()



# for i,link in enumerate(links):
# 	if (i+1)%8 == 0:
# 		print(link)
# 	else:
# 		print(link,end=' ')

# for link in links:
# 	print(link)

write_links(links)

# ------- scrape strain data from urls ---------


print("--- %d strains ---" % len(links))
print("--- %f seconds ---" % (time.time() - start_time))

from urllib.request import urlopen
from bs4 import BeautifulSoup
from math import ceil
import time

# TODO: line 40 finish e.get()'s for all the unique attributes 
# 		use the gets to do a full extraction of strain info and put them into different dictionaries


# scrape leafly website and put all the strains in a list 
# plan: access each individual strain's site and extract all strain's info

# ------- initialized vars -------
start_time = time.time()
# page_num = 0
# quote_page = 'https://www.leafly.com/explore/page-%d/sort-alpha' % page_num
type_set = {"{{category}}Hybrid", "{{category}}Sativa","{{category}}Indica"}

# ------- functions -------

def extract_strains(strains, explore_box):
	"""
	Take the "explore box" part of the leafly explore pages and extract
	the names of the strains and add them to 'strains'
	input: strains (lis) - master list of strains
		   explore_box (lis) - list of BeautifulSoup.Tag elements to extract 
		   					   strain names from
	output: ///

	examples of the (up to) 4 tspan tags that are part of a single strain:

	<tspan text-anchor="end" x="10" y="340">'98 Aloha White</tspan>
	<tspan text-anchor="end" x="0" y="380">Widow</tspan>
	<tspan ng-attr-y="{{380 - (40 * key)}}" ng-repeat="(key, value) in name" text-anchor="end" x="0">{{value}}</tspan>
	<tspan style="font-weight: 900" text-anchor="middle">{{symbol}}Awh</tspan>
	<tspan x="14" y="47">{{category}}Hybrid</tspan>
	"""
	name = ""
	for e in explore_box:
		# print(e.get('y'))
		is_name, is_abbr, is_type =  # extract name, abbr, and type tags
		if is_name and e.text:
			name += e.text + " "
		else:
			strains.append(name[:-1]) # leave off trailing space 
			name = ""

# ------- scrape pages -------
num_pages = ceil(2500 / 48) # values found manually from leafly
strains = []

for i in range(num_pages):
	quote_page = 'https://www.leafly.com/explore/page-%d/sort-alpha' % i

	# open page and get page data
	page = urlopen(quote_page)

	# parse the html
	soup = BeautifulSoup(page, 'html.parser')

	# extract the tags that contain strain name info
	# found manually from leafly
	explore_box = soup.find_all('tspan')
# 	extract_strains(strains, explore_box)

# for i,strain in enumerate(strains):
# 	if (i+1)%8 == 0:
# 		print(strain)
# 	else:
# 		print(strain,end=' ')

print("--- %d strains ---" % len(strains))
print("--- %f seconds ---" % (time.time() - start_time))

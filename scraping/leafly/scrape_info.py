#############
# Scrape the info of each leafly strain's own page and put the 
# info into dictionaries containing strain attributes: effect, negatives, & medical info
# and type from {Sativa, Indica, Hybrid, Sativa-Hybrid, Indica-Hybrid}

from urllib.request import urlopen
from bs4 import BeautifulSoup
from math import ceil
import time
import os
import json

# ------- initialized vars -------
start_time = time.time()
effects = {}
negatives = {}
medical = {}
types = {}
cnt = 1

# ------- functions ---------
def scrape_attributes(bs, strain, dic):
	"""
	for the given BeautifulSoup obj 'bs' representing attribute 'attr', 
	scrape all effects and add them to the appropriate dictionary

	input: bs (BeautifulSoup Object) - parent tag 
		   strain (string) - the name of the strain being queried 
		   dic (dictionary) - the dictionary corresponding to the strain type

	output: /// 
	"""
	dic[strain] = []
	all_effects = bs.findAll('div', attrs={'class': "m-attr-label copy--sm"})
	all_effects = [a.text for a in all_effects]
	all_percentages = bs.findAll('div', attrs={'class': "m-attr-bar"})
	all_percentages = [float(a['style'].strip('width:%')) for a in all_percentages]
	for tup in zip(all_effects,all_percentages):
		dic[strain].append(tup)



# ------- query each url for effect and type data ---------
while True:
	fname = "urls.txt"
	with open(fname, "r") as f:
		urls = f.readlines()

		for i,url in enumerate(urls):

			url.strip('\n')

			tmp,strain_type,strain_abbr = url.split('/')

			while True:

				# open page and get page data
				try:
					page = urlopen('https://www.leafly.com' + url, timeout=30)

					# parse the html
					soup = BeautifulSoup(page, 'html.parser')

					# get full name of strain
					strain_name = soup.find('h1').text

					# if necessary, extract the type of hybrid

					# extract the tags that contain strain description info
					# found manually from leafly
					description = soup.find('p')

					if strain_type == "hybrid":
						description = description.text
						if 'sativa-dominant' in description: strain_type = 'sativa-hybrid'
						if 'indica-dominant' in description: strain_type = 'indica-hybrid'

					# RECORD strain type
					types[strain_name] = strain_type

					# --------- get the effects' bar graphs + percentages into dicrionaries ---------
					# query for Effects
					effects_page = soup.find('div', attrs={'ng-show': "currentAttributeTab==='Effects'"})
					if effects_page:
						# run function to get all the relevant attributes' effects + their percentages
						scrape_attributes(effects_page, strain_name, effects)

					# query for Medical
					medical_page = soup.find('div', attrs={'ng-show': "currentAttributeTab==='Effects'"})
					if medical_page:
						scrape_attributes(medical_page, strain_name, medical)

					# query for Negatives
					negatives_page = soup.find('div', attrs={'ng-show': "currentAttributeTab==='Effects'"})
					if negatives_page:
						scrape_attributes(negatives_page, strain_name, negatives)
					break
				except:
					if cnt == 5: 
						cnt = 1
						break
					cnt+=1
					print('next attempt, %s' % url)
					continue
			print('completed %d' % i)
		f.close()


	# write the results to JSON files 
	with open('types.json', 'w') as fp:
	    json.dump(types, fp, sort_keys=True)
	    fp.close()

	with open('effects.json', 'w') as fp:
	    json.dump(effects, fp, sort_keys=True)
	    fp.close()

	with open('medical.json', 'w') as fp:
	    json.dump(medical, fp, sort_keys=True)
	    fp.close()

	with open('negatives.json', 'w') as fp:
	    json.dump(negatives, fp, sort_keys=True)
	    fp.close()


	print("--- %f seconds ---" % (time.time() - start_time))
	break
# File name: news_scraper.py
# Description: Scrape the political news from El Pais, El Periódico, El Mundo and ABC
# Author: Blanca Calvo Figueras
# Date: 02-02-2020

# How to run: 
# From El Pais: python3 news_scraper.py --media El_Pais --which 91273 --n_page 3 --out elpais_trial.csv
# 		where --which is the page to start scraping from and --n_pages the number of pages to scrape
# From El Mundo: python3 news_scraper.py --media El_Mundo --which 01 --n_page 1 --out elmundo_trial.csv
# 		where --which is the month of the year to scrape. --n_page should not be changed.
# From ABC: python3 news_scraper.py --media ABC --which 2 --n_page 2 --out ABC_trial.csv
#		where --which is the page to start scraping from and --n_pages the number of pages to scrape
# From El Periodico: python3 news_scraper.py --media El_Periodico --which 614 --n_page 1000 --out elPeriodico_4.csv
# 		where --which is the page to start scraping from and --n_pages the number of pages to scrape

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import sys
import argparse, re
import logging
import csv

def load_page(url):
	with requests.get(url) as f:
		page = f.text
	return page

def get_news_elPais(page):
	url = 'https://elpais.com/tag/politica/a/' + str(page)
	print(url)
	index_page = BeautifulSoup(load_page(url), 'lxml') # Parse the page
	data = list()
	media = 'El Pais'
	for row in index_page.find_all(class_='articulo'): 
		titulo = row.find(class_='articulo-titulo').find('a').text.strip() # Link text
		link = row.find(class_='articulo-titulo').find('a').get('href') # Link url
		fecha = row.find(class_='articulo-actualizado').text.strip()
		try:
			autor = row.find(class_='autor-nombre').find('a').text.strip()
		except:
			autor = ''
			pass
		# Store the data in a dictionary, and add that to our list
		data.append({
				 'media' : media,
				 'titulo': titulo,
				 'link': link,
				 'fecha': fecha,
				 'autor': autor,
				})
	return data


def get_news_ABC(page):
	url = 'https://www.abc.es/espana/pagina-' + str(page) + '.html'
	print(url)
	index_page = BeautifulSoup(load_page(url), 'lxml') # Parse the page
	data = list()
	media = 'ABC'
	for row in index_page.find_all(class_='articulo-portada'): 
		titulo = row.find(class_='titular').find('a').text.strip() # Link text
		link = row.find(class_='titular').find('a').get('href') # Link url
		fecha = ''
		try:
			autor = row.find(class_='autor').text.strip()
		except:
			autor = ''
			pass
		# Store the data in a dictionary, and add that to our list
		data.append({
				 'media' : media,
				 'titulo': titulo,
				 'link': link,
				 'fecha': fecha,
				 'autor': autor,
				})
	return data

def get_news_elPeriodico(page): # CREC QUE ESTIC ESCRAPEJANT UNA PART INICIAL O LATERAL QUE ES CADA DIA IGUAL??
	url = 'https://www.elperiodico.com/es/politica/p' + str(page) + '/'
	print(url)
	index_page = BeautifulSoup(load_page(url), 'lxml') # Parse the page
	data = list()
	media = 'El Periodico'
	for row in index_page.find_all(class_='ep-article'): 
		#print(row)
		titulo = row.find(class_='title').find('a').text.strip() # Link text
		link = row.find(class_='title').find('a').get('href') # Link url
		fecha = ''
		try:
			autor = row.find(class_='author').text.strip()
		except:
			autor = ''
			pass
		# Store the data in a dictionary, and add that to our list
		data.append({
				 'media' : media,
				 'titulo': titulo,
				 'link': link,
				 'fecha': fecha,
				 'autor': autor,
				})
	return data

def get_news_elMundo(year, month, day, moment):
	url = 'https://www.elmundo.es/elmundo/hemeroteca/' + year +'/'+ month +'/'+ day +'/'+ moment + '/espana.html?intcmp=MENUHOM24801&s_kw=espana'
	print(url)
	try:
		index_page = BeautifulSoup(load_page(url), 'lxml') # Parse the page
	except:
		print(day + '-' + month)
		data = list()
		return data
	items = index_page.find(class_='auto-items') # Get the list on from the webpage
	data = list()
	media = 'El Mundo'
	if items:
		for row in items.find_all(class_='content-item'): 
			#print(row)
			titulo = row.find(class_='mod-header').text.strip() # Link text
			#print(titulo)
			link = row.find(class_='mod-header').find('a').get('href') # Link url
			try:
				fecha = row.find(class_='mod-date').text.strip()
			except:
				fecha = month + '-' + year
				pass
			try:
				autor = row.find(class_='mod-author').text.strip()
			except:
				autor = ''
				pass
			# Store the data in a dictionary, and add that to our list
			data.append({
					 'media' : media,
					 'titulo': titulo,
					 'link': link,
					 'fecha': fecha,
					 'autor': autor,
					})
	else: # EL MUNDO CHANGED ITS WEBSITE IN MARCH 2019
		for row in index_page.find_all(class_='ue-c-cover-content__main'): 
		#print(row)
			titulo = row.find(class_='ue-c-cover-content__headline-group').text.strip() # Link text
			link = row.find(class_='ue-c-cover-content__headline-group').find('a').get('href') # Link url
			try:
				fecha = row.find(class_='mod-date').text.strip()
			except:
				fecha = month + '-' + year
				pass
			try:
				autor = row.find(class_='ue-c-cover-content__list-inline').text.strip()
			except:
				autor = ''
				pass
			# Store the data in a dictionary, and add that to our list
			data.append({
					 'media' : media,
					 'titulo': titulo,
					 'link': link,
					 'fecha': fecha,
					 'autor': autor,
					})
	return data

def elMundo_scraper(url):
	html = BeautifulSoup(load_page(url), 'lxml')
	content = []
	try:
		sentence = html.find_all('p')
		for element in sentence:
			content.append(element.text) # Link text
	except:
		pass
	try:
		fecha = html.find('time').text.strip()
		#print(fecha)
		return {'content': content, 'fecha': fecha} 
	except:
		return {'content': content} 
		pass
		

def ABC_scraper(url):
	if re.search("https://www.abc.es/espana", url):
		pass
		#print(url)
	elif re.search("^/espana/abci", url):
		url = "https://www.abc.es/" + url
		#print(url)
	else:
		#print(url)
		return dict()
	html = BeautifulSoup(load_page(url), 'lxml')
	content = []
	try:
		fecha = html.find(class_='actualizado').text.strip()
		try:
			cuerpo = html.find(class_='cuerpo-texto')
			sentence = cuerpo.find_all('p')
			for element in sentence:
				content.append(element.text) # Link text
		except:
			print('no content')
			pass
	except:
		return {'content': content} 
		print('no date')
		pass
	#print(content)

	return {'fecha':fecha, 'content': content} 

def elPeriodico_scraper(url):
	#print(url)
	html = BeautifulSoup(load_page(url), 'lxml')
	content = []
	try:
		fecha = html.find(class_='dateModified').text.strip()
	except:
		fecha = html.find(class_='datePublisher').text.strip()
	try:
		cuerpo = html.find(class_='ep-detail-body')
		sentence = cuerpo.find_all('p')
		for element in sentence:
			text = element.text
			clean_text = re.sub('\t', '', text)
			clean_text = re.sub('\n', '', clean_text)
			clean_text = re.sub('\xa0', '', clean_text)
			content.append(clean_text) # Link text
	except:
		pass
	#print(content)

	return {'fecha':fecha, 'content': content} 


def elPais_scraper(url):
	if not re.search("https", url):
		url = 'https:' + url
	html = BeautifulSoup(load_page(url), 'lxml')
	content = []
	try:
		cuerpo = html.find(class_='articulo-cuerpo')
		sentence = cuerpo.find_all('p')
		for element in sentence:
			content.append(element.text) # Link text
	except:
		pass

	return {'content': content} 

def parse_arguments():
	'''Read arguments from a command line'''
	parser = argparse.ArgumentParser(description='Read the SICK dataset files')
	parser.add_argument('--media', metavar = 'media', required = True, help='Media to scrap. Options: El_Pais, El_Mundo, ABC, El_Periodico', choices=['El_Pais', 'El_Mundo', 'ABC', 'El_Periodico'])
	parser.add_argument('--which', metavar='PAGE', required=True, help='Number of the page to start scrapping')
	parser.add_argument('--n_page', metavar='N_PAGE', required=True, help='Number of pages to keep on scrapping', argument_default='1')
	parser.add_argument('--out', metavar = 'data', required = True, help='Define the CSV to save the data')

	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()

	with open('data/'+args.out, 'w', encoding='utf-8') as f: # Open a csv file for writing
		fieldnames=['media','titulo', 'link', 'fecha', 'autor','content'] # These are the values we want to store
		writer = csv.DictWriter(f,delimiter=',', quotechar='"', # Common quote character
								quoting=csv.QUOTE_NONNUMERIC, # Make sure that all strings are quoted
								fieldnames=fieldnames
								)
		writer.writeheader() # Create headers in our csv file

		n = int(args.n_page)
		page = int(args.which)
		while n > 0:
			if args.media == 'El_Pais':
				n -= 1
				news = get_news_elPais(page) # 91273
				page += 1
				for row in news:
					info_news = elPais_scraper(row['link']) 
					for key, value in info_news.items():
						row[key] = value # Add the new data to our dictionary
				#print(news)
				for row in news:
					writer.writerow({k:v for k,v in row.items() if k in fieldnames})

			if args.media == 'El_Mundo':
				n = 0
				year = '2019'
				month = args.which
				days = list(range(1,32)) # (1,32)
				days = [str(item).zfill(2) for item in days]
				for day in days:
					#try:
					news = get_news_elMundo(year, month, day, 'm')
					#except:
						#print(day + ' ' + month)
						#pass
					for row in news:
						try:
							info_news = elMundo_scraper(row['link']) 
							for key, value in info_news.items():
								row[key] = value 
						except:
							pass
					for row in news:
						writer.writerow({k:v for k,v in row.items() if k in fieldnames})

			if args.media == 'ABC':
				n -= 1
				news = get_news_ABC(page)
				page += 1
				for row in news:
					info_news = ABC_scraper(row['link']) 
					for key, value in info_news.items():
						row[key] = value # Add the new data to our dictionary
				#print(news)
				for row in news:
					writer.writerow({k:v for k,v in row.items() if k in fieldnames})

			if args.media == 'El_Periodico':
				n -= 1
				news = get_news_elPeriodico(page)
				page+=1
				for row in news:
					info_news = elPeriodico_scraper(row['link']) 
					for key, value in info_news.items():
						row[key] = value # Add the new data to our dictionary
				#print(news)
				for row in news:
					writer.writerow({k:v for k,v in row.items() if k in fieldnames})
	print(page)
	#print(news['fecha']) # no probat



if __name__ == '__main__':
	main()
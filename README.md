# Spanish-Newspapers-Scraper
Find a python script to scrape the political news of four main newspapers in Spain: El Pais, El Mundo, El Peródico, ABC. 

The script of this project can be used to download the political news from the mentioned Spanish newspapers in 2019. If you use this script, please citate the github post. If you need to make changes to the script, you can contact me at blancacalvofigueras@gmail.com . Changes in the websites of these newspapers can prevent the script from working properly.

The script should be run as follows. 

For news from El Pais:
```
python3 news_scraper.py --media El_Pais --which 3 --n_page 3 --out elpais_news.csv
```
The parameter --which is the page number in the website from which to start scraping in the section "España". For intance, --which 3 will start scraping in the page https://elpais.com/noticias/politica/3/. Higher numbers means older news. The parameter --n_page indicates how many pages to scrape (with around 27 articles per page). The parameter --out defines the name of the document where the information will be saved, it should be a csv document.

For news from El Mundo: 
```
python3 news_scraper.py --media El_Mundo --which 01 --n_page 1 --out elmundo_news.csv
```
The parameter --which in this case refers to the month of the year. For instance, --which 01 will scrape the news of January. The number of pages can't be changed, the parameter --n_page should be kept as 1.  

For news from El Periódico: 
```
python3 news_scraper.py --media El_Periodico --which 3 --n_page 2 --out elPeriodico_news.csv
```
The parameter --which is the page number in the website from which to start scraping in the section "Política". For intance, --which 3 will start scraping in the page https://www.elperiodico.com/es/politica/p3/. Higher numbers means older news. The parameter --n_page indicates how many pages to scrape (with around 10 articles per page). 

For news from ABC: 
```
python3 news_scraper.py --media ABC --which 2 --n_page 2 --out ABC_news.csv
```
The parameter --which is the page number in the website from which to start scraping in the section "España". For intance, --which 2 will start scraping in the page https://www.abc.es/espana/pagina-2.html. Higher numbers means older news. The parameter --n_page indicates how many pages to scrape (with around 24 articles per page). 


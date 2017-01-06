import urllib3
from bs4 import BeautifulSoup
from queue import *
import sys
import nltk
import json


def crawl_urls(base_url):

    urls_to_crawl = Queue()
    urls_to_crawl.put(base_url)
    http = urllib3.PoolManager()
    urllib3.disable_warnings()
    no_out_links = {}
    in_links = {}
    urls_crawled = set()

    while urls_to_crawl.not_empty and urls_to_crawl.qsize()<3000:
        url = urls_to_crawl.get()
        try:
            if url not in urls_crawled:
                urls_crawled.add(url)
                page = http.request('GET',url)
                soup = BeautifulSoup(page.data,'lxml')
                links = soup.find_all('a')
                count = 0          
                for link in links:
                    if 'href' in link.attrs:
                        str = link['href']
                        if str.startswith('http') | str.startswith('/') and str!=url:
                            if str.startswith('http'):
                                weburl = link['href']
                            else:
                                weburl = url + str.rstrip('/')
                            urls_to_crawl.put(weburl)
                       
                            if url not in no_out_links.keys():
                                no_out_links[url]=1
                            else:
                                 no_out_links[url]+=1

                            if weburl not in in_links.keys():
                                in_links[weburl] = set()
                                in_links[weburl].add(url) 
                            else:
                                 in_links[weburl].add(url)   
        except:
            print('Some exception occured')               
            
    return no_out_links,in_links


def calculate_page_ranks(out_links,in_links):
    damping_fator = 0.85
    number_of_iterations = 10
    ranks = {}
    # intialize the ranks for each of the webpage as 1
    for key in out_links.keys():
        ranks[key] = 1
    for i in range(0, number_of_iterations + 1):
        for page in out_links.keys():
            sum=0
            for link in in_links[page]:
                sum+=ranks[link]/out_links[link]
        ranks[page]=(1-damping_fator)+(sum*damping_fator)
    
    return ranks


if __name__ == '__main__':
    seed_url = 'http://www.iitg.ernet.in'
    out_links,inlinks = crawl_urls(seed_url)
    page_ranks = calculate_page_ranks(out_links,inlinks)
    print(page_ranks)


import urllib3
from bs4 import BeautifulSoup
import json

http = urllib3.PoolManager()
urllib3.disable_warnings()
page_count = 0
file = open('vatan_review.json','w')
review_dict = {}
count = 1
for i in range(0,19):
    page = http.request('GET','https://www.yelp.com/biz/vatan-indian-vegetarian-new-york-2?start=' + str(page_count))
    soup = BeautifulSoup(page.data,'lxml')
    reviews_div = soup.findAll("div", { "class" : "review-content" })

    try:
        for div in reviews_div: 
            reiew_paragraph = div.find_all('p')
            review = reiew_paragraph[0].text
            review_dict[count] = review
            count+=1
        page_count+=20
    except:
        print('Some error generated')
json.dump(review_dict,file,sort_keys=True,indent=4, separators=(',', ': '))
file.flush()
file.close() 

with open('vatan_review.json') as data_file:
    data = json.loads(data_file.read())
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path" : "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser = init_browser()
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")
    
    titles = soup.find_all('div', class_='content_title')
    news_title = titles[0].a.text
    blurbs = soup.find_all('div', class_ = 'article_teaser_body')
    news_p = blurbs[0].text

    # Mars Space Images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_basic = "https://www.jpl.nasa.gov/spaceimages"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    images = soup.find_all('article', class_='carousel_item')[0]
    image_url = images['style']
    featured_image_url = url_basic + image_url[35:75]

    # Mars Weather tweet
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = tweets[0].p.text

    # Mars Facts
    url = "https://space-facts.com/mars/"
    # may need to change this 0 to a 1 
    mars_info = pd.read_html(url)[1]
    mars_info.columns = ["description", "value"]
    mars_info.set_index("description", inplace=True)
    mars_html_table = mars_info.to_html(classes="dataframe table-responsive table-striped table-bordered")

    # Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_basic = "https://astrogeology.usgs.gov"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []
    
    for i in range(0,4):
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        link = soup.find_all('div', class_='description')[i].a['href']
        
        browser.visit(url_basic+link)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        title = soup.find_all('section', class_ = 'block metadata')[0].h2.text
        image = soup.find_all('li')[0].a['href']
        hemisphere_dict = {"title": title, "img_url": image}
        hemisphere_image_urls.append(hemisphere_dict)
        
        i = i+1
    
    # create a dictionary that we'll call in the app.py and index.html files.
    mars_dict = {
        "mars_news_title":news_title,
        "mars_news_p":news_p,
        "mars_table":mars_html_table,
        "mars_img":featured_image_url,
        "weather_report":mars_weather,
        "mars_hemispheres":hemisphere_image_urls
    }

    # def scrape1()
    # return 

    # def scrape2()
    # return
    
    # def scrape_all()
    # initiate the chromedriver in this function too (init_browser currently)
        # mars_dict = {
        #   "key1": scrape1() 
        #   "key2": scrape2() 
        # }  create a dictionary that calls the four other scrape functions
    # browser.quit()
    # return mars_dict

    browser.quit()

    return mars_dict
    

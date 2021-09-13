# Import Splinter and BeautifulSoup
import re
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
        }

    # data_dic = {
    #     "img_url": img_url,
    #     "img_title": img_title
    #      }
    

    # img_url, img_title = mars_image(browser)


    

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

#browser.quit()

# Image Scraping
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    #img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

#df = pd.read_html('https://galaxyfacts-mars.com')[0]
#df.columns=['description', 'Mars', 'Earth']
#df.set_index('description', inplace=True)
#df

#df.to_html()

#browser.quit()

def mars_facts():
    try:
        #Use 'read_html' to scrape the facts table into a dataframe
        #df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, and bootstrap
    #return df.to_html()
    return df.to_html(classes="table table-striped")

# def mars_image(browser):
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)
#     html = browser.html
#     hemi_soup = soup(html, 'html.parser')
#     #hemi_image_urls = []
#     results = hemi_soup('div', class_='item')

#     for result in results:
#         try:
#             hemispheres = {}
#             html_page = result.find('a', 'href').click()
#             img_elem = result.find_by_tag('button')
            
#             img_elem.click()
#             html = browser.html
#             img_soup = soup(html, 'html.parser')

# #['img', class_='thumb']
#             img_url = f'https://marshemispheres.com/{img_url_r}'
        
#             img_title = result.find('h3').text

#            # data_dic.append({
#             #    'img_url': img_url,
#              #   'title': img_title,
#             #})

#         except BaseException:
#             return None
            
#         #return hemi_image_urls
    

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

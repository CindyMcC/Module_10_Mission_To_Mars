#!/usr/bin/env python
# coding: utf-8


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[35]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[36]:


slide_elem.find('div', class_='content_title')


# In[37]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[38]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# Image Scraping

# In[39]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[40]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[41]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[42]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[43]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[44]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[45]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[46]:


df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[47]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[63]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html, 'html.parser')

#hemisphere_image_urls = hemisphere_soup.find_all('div', class_='itemLink product-item')
results = hemi_soup('div', class_='item')

#hiu_all = hemisphere_image_urls.find_all('')

for result in results:
 # Error handling
    try:
        # Identify and return link to listing
        #img_url_r = hemi_soup.find('img', class_='fancybox-image').get('src')
        img_url_r = result.find('img', class_='thumb').get('src')
        img_url = f'https://marshemispheres.com/{img_url_r}'

 
        
        # Identify and return title of listing
        title = result.find('h3').text

        hemisphere_image_urls.append({
            'img_url': img_url,
            'title': title,
            })
        
    except Exception as e:
        print(e)
    


# In[64]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[65]:


# 5. Quit the browser
browser.quit()


# In[ ]:





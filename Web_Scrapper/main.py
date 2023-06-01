import requests
import string
import os
from bs4 import BeautifulSoup

def task1_showing_content():
    """Getting a json using the URL from input.
    Printing an error if there's non-200 code or no content inside."""
    url = input()
    try:
        response = requests.get(url)
        if response.json()['content'] == "" or response.json()['content'] == None:
            print("Invalid quote resource!")
        else:
            print(response.json()['content'])
    except:
        print("Invalid quote resource!")

def task2_url_checker():
    """Function is to get the URL from input.
    If isn't from domain nature.com, the command stops"""
    url = input()
    if "nature.com" not in url:
        print("Invalid page!")
        exit()
    return url
def task2_showing_title_and_description(url):
    """This function is printing a title and description from metadata tag"""
    articles_dictionary = {}
    retrieved_data = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    parsed_retrieved_data = BeautifulSoup(retrieved_data.content, 'html.parser')
    # print(parsed_retrieved_data.find('title').text)
    # print(parsed_retrieved_data.find("meta", property="og:description")["content"])
    articles_dictionary["title"] = parsed_retrieved_data.find('title').text
    articles_dictionary["description"] = parsed_retrieved_data.find("meta", property="og:description")["content"]
    print(articles_dictionary)

def task3_saving_binary_webpage_content():
    """This function gets URL. Saves the content in Binary. If
    return code isn't 200, the function sends a notification."""
    print("Input the URL:")
    url_to_download = input()
    downloaded_page = requests.get(url_to_download)
    if downloaded_page.status_code != 200:
        print("The URL returned {}!".format(downloaded_page.status_code))
    else:
        file = open('source.html', 'wb')
        file.write(downloaded_page.content)
        file.close()
        print("Content saved.")

def task4_finding_links_to_news():
    """1. Find News in the URL
    2. Save link and title in the dictionary"""
    dictionary_of_news_urls_n_titles = {}
    url_to_scan = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    retrieved_data = requests.get(url_to_scan, headers={'Accept-Language': 'en-US,en;q=0.5'})
    parsed_retrieved_data = BeautifulSoup(retrieved_data.content, 'html.parser')
    for article in parsed_retrieved_data.findAll('article'):
        if article.find('span', {'class': 'c-meta__type'}, text='News') != None:
            # print(article.find('a', href=True)["href"])
            # print(article.find('a', href=True).text)
            dictionary_of_news_urls_n_titles[article.find('a', href=True)["href"]] = article.find('a', href=True).text
    return dictionary_of_news_urls_n_titles
    # {'/articles/d41586-020-03621-6': 'Biden’s pick to head US environment agency heartens scientists',
    # '/articles/d41586-020-03593-7': 'Moderna COVID vaccine becomes second to get US authorization',
    # '/articles/d41586-020-03561-1': 'Is lightning striking the Arctic more than ever before?'}

def task4_getting_text_of_required_articles(dictionary_link_title):
    """In this function I take in cicle link and name, retrieve the data and write it"""
    list_of_file_name = []
    for link, title in dictionary_link_title.items():
        article_url = "https://www.nature.com" + link
        # print(article_url)
        retrieved_data = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        parsed_retrieved_data = BeautifulSoup(retrieved_data.content, 'html.parser')
        # print(parsed_retrieved_data.find('p', {'class': "article__teaser"}).text)
        str_to_save = parsed_retrieved_data.find('p', {'class': "article__teaser"}).text
        str_to_save_encoded = str_to_save.encode(encoding = 'UTF-8',errors = 'strict')
        title_no_punc = title.translate(str.maketrans('', '', string.punctuation))
        title_final = title_no_punc.replace(' ', '_')
        title_final = title_final.strip() + ".txt"
        list_of_file_name.append(title_final)
        # print(title_final)
        file = open(title_final, 'wb')
        file.write(str_to_save_encoded)
        file.close()

    print("Saved articles:  {}".format(list_of_file_name))

def task5_getting_list_of_articles(topic, amount_of_pages):
    """In this function I get amount of pages from1 to N. I filter the links of the required topic"""
    dictionary_of_pages_n_links = {}
    list_of_urls_on_page = []
    for n in range(1, (int(amount_of_pages) + 1)):
        url_to_scan = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={}".format(n)
        retrieved_data = requests.get(url_to_scan, headers={'Accept-Language': 'en-US,en;q=0.5'})
        parsed_retrieved_data = BeautifulSoup(retrieved_data.content, 'html.parser')
        for article in parsed_retrieved_data.findAll('article'):
            dictionary_link_title = {}
            if article.find('span', {'class': 'c-meta__type'}, text=topic) != None:
                # print(article.find('a', href=True)["href"])
                # print(article.find('a', href=True).text)
                title = article.find('a', href=True).text
                title_no_punc = title.translate(str.maketrans('', '', string.punctuation))
                title_final = title_no_punc.replace(' ', '_')
                title_final = title_final.strip() + ".txt"
                dictionary_link_title[article.find('a', href=True)["href"]] = title_final
                list_of_urls_on_page.append(dictionary_link_title)
        dictionary_of_pages_n_links[n] = list_of_urls_on_page
        list_of_urls_on_page = []
    return dictionary_of_pages_n_links

def task5_creating_files_in_required_folders(dictionary_w_pages_links_titles):
    """Takes a dictionary of format {page_number: list_of_[link: file name]}"""
    for page_number, list_of_articles in dictionary_w_pages_links_titles.items():
        for article in list_of_articles:
            # print(list(article.keys())[0])
            article_url = "https://www.nature.com" + list(article.keys())[0]
            retrieved_data = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            parsed_retrieved_data = BeautifulSoup(retrieved_data.content, 'html.parser')
            str_to_save = parsed_retrieved_data.find('p', {'class': "article__teaser"}).text
            str_to_save_encoded = str_to_save.encode(encoding='UTF-8', errors='strict')
            file = open("Page_{}/{}".format(page_number, article[list(article.keys())[0]]), 'wb')
            file.write(str_to_save_encoded)
            file.close()
    print("Saved all articles.")

def task5_creating_folders(amount_of_pages):
    """Creating directories named from 'Folder 1' to 'Folder N'"""
    for n in range(1, (int(amount_of_pages) + 1)):
        directory = "Page_" + str(n)
        # Check if the directory exists
        if not os.path.exists(directory):
            # If it doesn't exist, create it
            os.makedirs(directory)

if __name__ == '__main__':
    # task4_getting_text_of_required_articles(task4_finding_links_to_news())
    amount_of_pages = input()
    topic_of_article = input()
    task5_creating_folders(amount_of_pages)
    task5_creating_files_in_required_folders(task5_getting_list_of_articles(topic_of_article, amount_of_pages))

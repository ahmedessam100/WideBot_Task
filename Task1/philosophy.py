import time
import urllib
import sys
import bs4
import requests


class philosphy:
    
    def __init__(self, first_url, max_iterations=30, end_url = "https://en.wikipedia.org/wiki/Philosophy"):
        self.first_url = first_url
        self.end_url = end_url
        self.visited = [first_url]
        self.max_iterations = max_iterations

    def scraping(self):
        
        # Iterate through links
        while(self.check_point()):
            print(self.visited[-1])
            next_url = self.get_next_reference(self.visited[-1])

            if next_url:
                self.visited.append(next_url)
                time.sleep(1)
            else:
                print("No outgoing links!")
                break

    
    def get_next_reference(self, current_url):

        # Get request to retrieve the article html
        response = requests.get(current_url)
        text = response.text

        # Parsing HTML text
        html = bs4.BeautifulSoup(text, "html.parser")
        find = False
        
        # Searching for the first link inside the paragraphs
        for tag in html.find_all("p"):
            if tag.find("a"):
                # Retieve the url of the link
                url = tag.find("a").get("href")
                find = True
                break
        
        # If we find link child
        if find:
            return urllib.parse.urljoin('https://en.wikipedia.org/', url)
        
    def check_point(self):

        # previously visited nodes
        prev_visited = self.visited[:-1]
        current_node = self.visited[-1]
        if current_node == self.end_url:
            print(current_node)
            print("Destination reached!")
            return False
        elif self.max_iterations <= len(self.visited):
            print("Time out")
            return False
        elif current_node in prev_visited:
            print("Stucked in a loop!")
            return False
        # Can continue to iterate
        else:
            return True

first_url = "https://en.wikipedia.org/wiki/" + sys.argv[1] 
scrap = philosphy(first_url=first_url)
scrap.scraping()

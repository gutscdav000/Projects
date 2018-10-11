
#url: https://sbir.defensebusiness.org/topics
PASSWORD_FOR_SUDO = ""


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import urllib.request, os, sys, subprocess, time, re, csv

# purpose: a function which takes a url and extracts the contents as a string
# depends on selenium webdriver to turn js-scripts into html as well as time and os libraries
# signature: pull_html_page(url:string, write:optional boolean) -> string 
def pull_html_page(url, write = False):

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    content = driver.page_source.encode('utf-8')

    driver.quit()
    

    if write == True:
        # the "my dick computer won't let me be root" workaround
        if os.geteuid() == 0:
            print("We're root!")
        else:
            print("We're not root.")
            CURRENT_SCRIPT = os.path.realpath(__file__)
            os.system('echo ' + PASSWORD_FOR_SUDO + '|sudo -S python '+ CURRENT_SCRIPT)

            clean = BeautifulSoup(content, "html.parser").prettify()
            
            f = open("out.html", "w+")
            f.write(clean)
            f.close()
    
    return content

# purpose: a function which takes a html table and extracts all of the href url's
# depends on regex and BeautifulSoup
# signature: parse_table_bs4(url_contents: String) -> List of partial url's
def parse_table_bs4(url_contents):
    
    # build html tree
    soup = BeautifulSoup(url_contents, "html.parser")
    clean = soup.prettify() # just a string
    #print(clean)
    
    # pull out table
    table = soup.findAll("table")
    #print(table)

    # extract <a> tags
    regex = "(?<=<a).+?(?=>)"  #use re.DOTALL if needing to parse multiple lines
    a_tags = re.findall(regex, str(table))

    # exctract hrefs
    regex = '(?<=href=").+?(?=")'
    hrefs = []
    for tag in a_tags: 
        hrefs.append(re.findall(regex, str(tag))[0])
    
    return hrefs

# purpose: a function which extracts a few table columns given the specific
#          url for the topic 
# depends on BeaurifulSoup and hella regular expressions
# signature: scrape_sbir_page(url: string) -> topicNum:string, component:string, techArea:string, title:string, objective:string
def scrape_sbir_page(url):
    
    contents = pull_html_page(url)
    soup = BeautifulSoup(contents, "html.parser")
    
    # extract: Component, Topic #, Tech Area, Title
    top_div = str(soup.find('div', {'class' : r'topic-head topic-box'}))
    #print(top_div)
    paragraphs = re.findall(r"(?<=<p>).+?(?=</p>)", top_div, re.DOTALL)
    # some columns
    component = re.findall("(?<=:).+?(?=</strong>)", paragraphs[0].strip())[0].strip()
    topic_num = re.findall("(?<=:</strong>).+", paragraphs[1].strip())[0].strip()
    title = re.findall('(?<=topic-title">).+?(?=</span>)', paragraphs[2].strip())[0].strip()
    tech_area = re.findall("(?<=</strong>).+", paragraphs[3].strip(), re.DOTALL)[0].strip()
    
    # extract: objective
    objective_div = str(soup.find('div', {'class' : r'topic-body topic-box autolink'}))
    # another column
    obj = re.search("(?<=<p>).+?(?=</p>)", objective_div, re.DOTALL).group()[11:].strip()

    return topic_num, component, tech_area, title, obj

########################################
##              MAIN
########################################

content = pull_html_page("https://sbir.defensebusiness.org/topics")
partial_urls = parse_table_bs4(content)
partial_urls = list(set(partial_urls))
print(partial_urls)

# csv / google sheet columns
CSV_HEADERS = ["Topic #", "url", "Proposal #", "Component", "Technology Area", "Title", "Sign up to possibly lead", \
"Sign up to possibly assist", "Potential Partners", "Objective", "Keywords", "Notes", "Key Personnel", \
"TPOC 1 Name", "TPOC 1 Phone", "TPOC 1 Email", "TPOC 2 Name", "TPOC 2 Phone", "TPOC 2 Email"]

URL = "https://sbir.defensebusiness.org"
UNSCRIPTABLE_VALUE = "TBD" # value given to attributes not found on topics pages


 
#test_url = URL + "/topics?topicId=29333"

FILE_NAME = "sbir_contracts.csv"
with open(FILE_NAME, "w") as csvfile:
    # instantiate writer & write headers
    writer = csv.DictWriter(csvfile, fieldnames = CSV_HEADERS)
    writer.writeheader()
    # write rows (each row corresponds with a contract and a different topic page)
    for part in partial_urls:
        
        topic_url = URL + part
        print("url:",topic_url)
        print("^" * 70)
        topic_num, component, tech_area, title, objective = scrape_sbir_page(topic_url)
        scriptable_cols_dict = {"Topic #" : topic_num, "url" : topic_url, "Component" : component, "Technology Area" : tech_area, "Title" : title, "Objective" : objective}
        row_dict = {}
        for col in CSV_HEADERS:
            if col in list(scriptable_cols_dict.keys()):
                row_dict[col] = scriptable_cols_dict[col]
            else:
                row_dict[col] = UNSCRIPTABLE_VALUE
            
        
        writer.writerow(row_dict)
        
        print("topic #:", topic_num)
        print("component:", component)
        print("tech area:", tech_area)
        print("title:", title)
        print("objective:", objective)
        print("*" * 70)

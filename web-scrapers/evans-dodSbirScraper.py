
###########################################
"""
run times on https://sbir.defenseebusiness.org/topics url q4 2018

single thread: 497 s
2 threads:     453 s
3 threads:     460 s
4 threads:     456 s
5 threads:     458 s
"""
###########################################

#url: https://sbir.defensebusiness.org/topics
PASSWORD_FOR_SUDO = ""


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import urllib.request, os, sys, subprocess, time, re, csv
#import readPDF
from FunctionThread import FunctionThread

# purpose: a function which takes a url and extracts the contents as a string
# depends on selenium webdriver to turn js-scripts into html as well as time and os libraries
# signature: pull_html_page(url:string, write:optional boolean) -> string 
def pull_html_page(url, write = False):

    driver = webdriver.Chrome()
    #time.sleep(3)
    driver.get(url)
    time.sleep(1)
    content = driver.page_source.encode('utf-8')
    #time.sleep(3)
    driver.quit()
    

    if write == True:
        # the "my computer won't let me be root" workaround
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
# depends on BeautifulSoup and regular expressions
# signature: scrape_sbir_page(url: string) -> topicNum:string, component:string, techArea:string, title:string, objective:string
def scrape_sbir_page(url):
    
    contents = pull_html_page(url)
    soup = BeautifulSoup(contents, "html.parser")
    
    # extract: Component, Topic #, Tech Area, Title
    top_div = str(soup.find('div', {'class' : r'topic-head topic-box'}))
    #print(top_div)
    paragraphs = re.findall(r"(?<=<p>).+?(?=</p>)", top_div, re.DOTALL)
    # some columns
    
    try:
        component = re.findall("(?<=:).+?(?=</strong>)", paragraphs[0].strip())[0].strip()
    except:
        component = "TBD"

    try:
        topic_num = re.findall("(?<=:</strong>).+", paragraphs[1].strip())[0].strip()
    except:
        topic_num = "TBD"

    try:
        title = re.findall('(?<=topic-title">).+?(?=</span>)', paragraphs[2].strip())[0].strip()
    except:
        title='TBD'
        pass
    tech_area = re.findall("(?<=</strong>).+", paragraphs[3].strip(), re.DOTALL)[0].strip()
    
    # extract: objective
    objective_div = str(soup.find('div', {'class' : r'topic-body topic-box autolink'}))
    # another column
    obj = re.search("(?<=<p>).+?(?=</p>)", objective_div, re.DOTALL).group()[11:].strip()
    #print(objective_div)
    #print(obj)

    p_tags= soup.find('div', {'class' : r'topic-body topic-box autolink'}).find_all('p')

    desc=p_tags[1].text[13:].strip()
    #print(desc)

    P1=p_tags[2].text[9:].strip()
    #print(P1)

    P2=p_tags[3].text[10:].strip()
    #print(P2)

    try:
        P3=p_tags[4].text
        #print(P3)
    except:
        P3='TBD'
        pass

    Keywords=p_tags[5].text[10:].strip()
    #print(Keywords)

    try:
        TPOC1=p_tags[6].text
        TPOC1=re.sub(r'\s+', ' ',TPOC1)
        #print(TPOC1)
    except:
        TPOC1='TBD'
        pass


    try:
        TPOC2=p_tags[7].text
        TPOC2=re.sub(r'\s+', ' ',TPOC2)
        #print(TPOC2)
    except:
        TPOC2='TBD'
        pass

    try:
        TPOC3=p_tags[8].text
        TPOC3=re.sub(r'\s+', ' ',TPOC3)
        #print(TPOC2)
    except:
        TPOC3='TBD'
        pass
    
##    for p in p_tags:
##        print(p.text)
  
    return topic_num, component, tech_area, title, obj, Keywords, TPOC1, TPOC2, TPOC3

        


def main():

    MAX_THREADS = 5


    content = pull_html_page("https://sbir.defensebusiness.org/topics")
    partial_urls = parse_table_bs4(content)
    partial_urls = list(set(partial_urls))
    print(partial_urls)

    # csv / google sheet columns
    CSV_HEADERS = ["Topic #", "url", "Proposal #", "Component", "Technology Area", "Title", "Sign up to possibly lead", \
"Sign up to possibly assist", "Potential Partners", "Objective", "Keywords", "Notes", "Key Personnel", \
"TPOC 1", "TPOC 2", "TPOC 3"]

    URL = "https://sbir.defensebusiness.org"
    UNSCRIPTABLE_VALUE = "TBD" # value given to attributes not found on topics pages

 
    
    FILE_NAME = "sbir_contracts.csv"
    with open(FILE_NAME, "w") as csvfile:
        # instantiate writer & write headers
        writer = csv.DictWriter(csvfile, fieldnames = CSV_HEADERS)
        writer.writeheader()
        threads = []
        
        i = 0
        j = len(partial_urls)

        # while we haven't made it to the end of the url's list
        while i < j:
            
            # add threads until we've reached the capacity
            while len(threads) < MAX_THREADS and i < j:
                
                searchUrl = URL + partial_urls[i]
                i += 1
                    #start a thread and add it to the threads list
                t = FunctionThread(searchUrl) 
                threads.append(t)

            addThread = False
            
            # check if the threads are alive until one terminates
            while addThread != True:
                
                for t in threads:
                    # remove the thread when it's done and 
                    if not t.isAlive():
                        addThread = True
                        threads.remove(t)

                        #write to file routine
                        row = {'Topic #': t.topic_num, 'url': t.url, 'Proposal #': 'TBD', 'Component': t.component, 'Technology Area': t.tech_area, \
'Title': t.title, 'Sign up to possibly lead': 'TBD', 'Sign up to possibly assist': 'TBD', 'Potential Partners': 'TBD', 'Objective': t.obj, 'Keywords': t.keywords, 'Notes': 'TBD', 'Key Personnel': 'TBD', 'TPOC 1': t.TPOC1, 'TPOC 2': t.TPOC2, 'TPOC 3': t.TPOC3 }

                        writer.writerow(row)
        

                        #print routine
                        print("topic #:", t.topic_num)
                        print("component:", t.component)
                        print("tech area:", t.tech_area)
                        print("title:", t.title)
                        print("objective:", t.obj)
                        print("keywords:", t.keywords)
                        print("TPOC1:", t.TPOC1)
                        print("TPOC2:", t.TPOC2)
                        print("TPOC3:", t.TPOC3)
                        print("*" * 70)


        return

########################################
##              MAIN
########################################
start_time = time.time()
main()
print ("EXECUTION TIME:::\t", time.time() - start_time)
#old_main()

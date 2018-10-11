
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import urllib.request, os, sys, subprocess, time, re, csv, threading


class FunctionThread (threading.Thread):

    url = ""
    topic_num = "TBH"
    component = "TBH"
    tech_area = "TBH"
    title = "TBH"
    obj = "TBH"
    keywords = "TBH"
    TPOC1 = "TBH"
    TPOC2 = "TBH"
    TPOC3 = "TBH"

    # this constructor takes a URL (note: designed for scraping sbir topics, but may be refactored) and 
    # starts scraping the topic page via the scrape_sbir_page function
    def __init__(self, url):
        self.url = url
        threading.Thread.__init__(self)
        self.start()
        self.scrape_sbir_page(url)



    # purpose: a function which extracts a few table columns given the specific
    #          url for the topic  
    # depends on BeautifulSoup and regular expressions
    # signature: scrape_sbir_page(self, url: string) -> void 
    # *** (values are saved to field variables to be retreived via the object)
    def scrape_sbir_page(self, url):
    
        contents = pull_html_page(url)
        soup = BeautifulSoup(contents, "html.parser")
    
        # extract: Component, Topic #, Tech Area, Title
        top_div = str(soup.find('div', {'class' : r'topic-head topic-box'}))
        
        paragraphs = re.findall(r"(?<=<p>).+?(?=</p>)", top_div, re.DOTALL)
        # some columns
    
        try:
            self.component = re.findall("(?<=:).+?(?=</strong>)", paragraphs[0].strip())[0].strip()
        except:
            pass

        try:
            self.topic_num = re.findall("(?<=:</strong>).+", paragraphs[1].strip())[0].strip()
        except:
            pass
            
        try:
            self.title = re.findall('(?<=topic-title">).+?(?=</span>)', paragraphs[2].strip())[0].strip()
        except:
            pass
        
        try:
            self.tech_area = re.findall("(?<=</strong>).+", paragraphs[3].strip(), re.DOTALL)[0].strip()
        except:
            pass

        # extract: objective
        objective_div = str(soup.find('div', {'class' : r'topic-body topic-box autolink'}))
        # another column
        try:
            self.obj = re.search("(?<=<p>).+?(?=</p>)", objective_div, re.DOTALL).group()[11:].strip()
        except: 
            pass
        
        try:
            p_tags = soup.find('div', {'class' : r'topic-body topic-box autolink'}).find_all('p')

            desc=p_tags[1].text[13:].strip()

            P1=p_tags[2].text[9:].strip()
    

            P2=p_tags[3].text[10:].strip()
            P3=p_tags[4].text
            self.keywords=p_tags[5].text[10:].strip()
            self.TPOC1=p_tags[6].text
            self.TPOC1=re.sub(r'\s+', ' ',self.TPOC1)
            self.TPOC2=p_tags[7].text
            self.TPOC2=re.sub(r'\s+', ' ',self.TPOC2)
        except:
            pass



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



###########################
#main test:
###########################

#searchUrl = "https://sbir.defensebusiness.org/topics?topicId=29693"
#t1 = FunctionThread(searchUrl)
#searchUrl = "https://sbir.defensebusiness.org/topics?topicId=29704"
#t2 = FunctionThread(searchUrl) 
#searchUrl = "https://sbir.defensebusiness.org/topics?topicId=29709"
#t3 = FunctionThread(searchUrl)

#print(t1.url)
#print(t2.url)
#print(t3.url)
#while t1.isAlive() or t2.isAlive() or t3.isAlive():
#    pass

        
#print("topic #:", t1.topic_num)
#print("component:", t1.component)
#print("tech area:", t1.tech_area)
#print("title:", t1.title)
#print("objective:", t1.obj)
#print("keywords:", t1.keywords)
#print("TPOC1:", t1.TPOC1)
#print("TPOC2:", t1.TPOC2)
#print("TPOC3:", t1.TPOC3)
#print("*" * 70)


#print("topic #:", t1.topic_num)
#print("component:", t2.component)
#print("tech area:", t2.tech_area)
#print("title:", t2.title)
#print("objective:", t2.obj)
#print("keywords:", t2.keywords)
#print("TPOC1:", t2.TPOC1)
#print("TPOC2:", t2.TPOC2)
#print("TPOC3:", t2.TPOC3)
#print("*" * 70)

#print("topic #:", t3.topic_num)
#print("component:",t3.component)
#print("tech area:", t3.tech_area)
#print("title:", t3.title)
#print("objective:", t3.obj)
#print("keywords:", t3.keywords)
#print("TPOC1:", t3.TPOC1)
#print("TPOC2:", t3.TPOC2)
#print("TPOC3:", t3.TPOC3)
#print("*" * 70)

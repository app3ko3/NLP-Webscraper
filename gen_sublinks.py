from pyvis.network import Network
from selenium import webdriver
import networkx as nx
import pandas as pd

PATH = 'C:\Program Files (x86)\chromedriver.exe'
SITES = []
EDGES = []
EDGE_LIST_DIR = 'Edgelists'
NETWORK_GRAPH_DIR = 'Network Graphs'
MAX_DEPTH = 2
invalid_sites = [  'youtube.com',
                   'youtu.be',
                   'github.com',
                   'chrome.google',
                   'goo.gl',
                   'google.com',
                   'facebook.com',
                   'twitter.com',
                   'instagram.com',
                   'linkedin.com',
                   'messenger.com',
                   'wevolver',
                   'reddit',
                   'bulletin.com',
                   'cloudflare.com',
                   'apps.apple',
                   'rsci.app.link',
                   'policy.medium',
                   'help.medium',
                   'medium.com/tag/',
                   'https://medium.com/@',
                   'https://medium.com/m/signin',
                   'apple.com',
                   'knowable.fyi'
                   'camerapositioning.io',
                ]

invalid_ext = ['.jpg', '.jpeg', '.svg', '.png', '.mp4',
               '.ch', '/ch', '=ch',
               '.jp', '/jp', '=jp',
               '.zh', '/zh', '=zh',
               '.es', '/es', '=es',
               '.de', '/de', '=de',
               '.ko', '/ko', '=ko',
               '.fr', '/fr', '=fr',
               '/about', '/team', '/join-us', '/jobs', '/careers',
               '/contact', '/support', '/warranty', '/shipment', '/payment-methods', '/downloads', '/help',
               '/terms', '/privacy', '/privacy-policy', '/copyright', 
               ]

def check_link(url, s):
    if not s:
        return ''
    
    if url+'#'==s or url+'/#'==s:
        return ''
    
    if 'http' not in s:
        if (s[0] == '/' or s[0] == '#') and len(s)>1:
            return (url + s).rstrip('#').rstrip('/')
        return ''
    
    for inv in invalid_sites:
        if inv in s:
            return ''

    for ext in invalid_ext:
        if s.endswith(ext):
            return ''

    return s.rstrip('#').rstrip('/')

def get_sublinks(url):
    try:
        driver.get(url)
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = check_link(url, elem.get_attribute('href'))
            if href and href not in SITES:  
                SITES.append(href)
                EDGES.append((url, href))
    except:
        pass
    

driver = webdriver.Chrome(PATH)

# timeout if doesn't load within 20s
#driver.manage().timeouts().pageLoadTimeout(20, TimeUnit.SECONDS);

options = webdriver.ChromeOptions()
options.add_argument('--enable-javascript')
options.add_argument('--lang=en') 
options.add_argument('headless')

df = pd.read_excel('companies-sensor.xlsx')
df.dropna(axis=0, inplace=True)
df['actual_url'] = df['actual_url'].apply(lambda x:x.rstrip('/'))

for i, row in df.iloc[11:].iterrows():
    print('##############################')
    print('Company:', row['Company Name'])
    print('Root   :', row['actual_url'])
    print('##############################\n')
    url = row['actual_url']
    SITES.append(url)

    # iteratively add on the sublinks to our list
    n = 0
    for d in range(MAX_DEPTH):
        limit = len(SITES)
        while n < limit:
            print(SITES[n])
            get_sublinks(SITES[n])
            n += 1

    # create edgelist to plot network graph
    df_network = {'Source':[],
                  'Target':[]}
    
    for e in EDGES:
        df_network['Source'].append(e[0])
        df_network['Target'].append(e[1])

    df_network = pd.DataFrame(df_network)
    df_network.to_csv('{}/{}.csv'.format(EDGE_LIST_DIR,
                                         row['Company Name']), index=False)

    G = nx.from_pandas_edgelist(df_network, source='Source', target='Target')
    net = Network('100vh', '100vw')
    net.from_nx(G)
    net.show('{}/{}.html'.format(NETWORK_GRAPH_DIR,
                                 row['Company Name']))

    SITES.clear()
    EDGES.clear()
    print()

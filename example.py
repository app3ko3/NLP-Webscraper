from companycrawler.crawler import CompanyCrawler
from clientextraction.heuristic_extraction import clients_from_json, print_clients
import pandas as pd
import os

# define variables
data_path = 'saved_data' # save scaped data here
max_depth = 2
client_output_path = 'clients.csv' # create client csv here

'''
+--------------+
| Web scraping |
+--------------+
'''

CC = CompanyCrawler(save_webtree=False, save_network_graph=True)

def scrape_excel(companies):
    # load excel data from 'companies-software.xlsx'
    df = pd.read_excel(companies)
    df.dropna(axis=0, inplace=True, subset=['actual_url'])
    df.reset_index(drop=True, inplace=True)

    # enumerate rows in excel
    for i, row in df.iterrows():
        CC.crawl_company(
            root=row['actual_url'], 
            company=row['Company Name'], 
            save_dir=data_path,
            max_depth=max_depth
        )

def scrape_single(company, url):
    CC.crawl_company(
        root=url,
        company=company, 
        save_dir=data_path,
        max_depth=max_depth
    )

scrape_single('ViewAR', 'https://www.viewar.com/')
#scrape_excel('companies-software.xlsx')

'''
+-------------------+
| Client extraction |
+-------------------+
'''

def extract_clients(data_path, companies):
    results = {
        'url': [],
        'page': [],
        'alt': [],
        'url_tail': [],
        'common': []
    }

    # for each company data folder found in data_path, 
    # extract client data from each company's clients.json
    for company in companies:
        clients = clients_from_json(os.path.join(data_path, company, 'clients.json'), company)
        results['url'].extend(clients['url'])
        results['page'].extend(clients['page'])
        results['alt'].extend(clients['alt'])
        results['url_tail'].extend(clients['url_tail'])
        results['common'].extend(clients['common'])
        #print_clients(clients)

    # save client data to csv at client_output_path
    client_df = pd.DataFrame(results)
    client_df.to_csv(client_output_path, index=False, encoding='utf-8-sig')

#extract_clients(data_path, ['Intermodalics'])

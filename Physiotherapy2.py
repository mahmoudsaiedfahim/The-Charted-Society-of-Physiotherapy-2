import requests
from bs4 import BeautifulSoup
import pandas as pd

all_links = []
profiles = {
    "profile_url": [],
    "full_name": [],
    "membership_number": [],
    "specialism": [],
    'LinkedIn': [],
    'Twitter': [],
    'Facebook': [],
    'Email': [],
    'Company Website': [],
    'address': []
}

for page in range(1, 73):
    url = f"https://www.macpweb.org/physios/?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    listing_container = soup.find("div", class_="listing-container")
    links = listing_container.find_all("a")

    page_links = [link["href"] for link in links]
    try:
        for link in page_links:
            try:
                page_link = "https://www.macpweb.org" + link
                page_response = requests.get(page_link)
                page_soup = BeautifulSoup(page_response.text, "html.parser")

                header = page_soup.find("header", class_="profile-header")
                full_name=''
                profile_url=''
                membership_number=''
                try:
                    full_name=header.find("h2").text.strip()
                    profile_url=page_link
                    membership_number=header.find("h4").text.split(':')[1].strip()
                    profiles["full_name"].append(full_name)
                    profiles["profile_url"].append(profile_url)
                    profiles["membership_number"].append(membership_number)
                except:
                    profiles["full_name"].append(full_name)
                    profiles["profile_url"].append(profile_url)
                    profiles["membership_number"].append(membership_number)
                try:
                    specialism=header.find("ul").text.replace('\n',' | ').strip()[2:-2]
                    profiles["specialism"].append(specialism)
                except:
                    profiles["specialism"].append('')

                icon_list = page_soup.find('ul', class_='icon-list')
                facebook=''
                linkedIn=''
                twitter=''
                email=''
                company_website=''
                try:
                    for item in icon_list.find_all('li'):
                        item_link = item.find('a')
                        if item_link:
                            href = item_link['href']
                            text = item_link.get_text(strip=True)
                            if 'facebook' in href:
                                facebook=href

                            elif 'linkedin' in href:
                                linkedIn=href

                            elif 'twitter' in href:
                                twitter=href

                            elif 'mailto:' in href:
                                email=href

                            else:
                                company_website=href
                    profiles['Facebook'].append(facebook)
                    profiles['LinkedIn'].append(linkedIn)
                    profiles['Twitter'].append(twitter)
                    profiles['Email'].append(email)
                    profiles['Company Website'].append(company_website)
                except:
                    profiles['Facebook'].append('')
                    profiles['LinkedIn'].append('')
                    profiles['Twitter'].append('')
                    profiles['Email'].append('')
                    profiles['Company Website'].append('')



                try:
                    profiles['address'].append(page_soup.find(class_='profile-address').text.strip())
                except:
                    profiles['address'].append('')
            except:
                pass
    except:
        pass
#print(profiles)
df = pd.DataFrame(profiles)
df.to_csv('Physiotherapy2.csv', index=False)

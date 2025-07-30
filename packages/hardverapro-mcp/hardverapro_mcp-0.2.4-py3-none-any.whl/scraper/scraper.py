import requests
from bs4 import BeautifulSoup


BASE_URL ="https://hardverapro.hu/aprok/"
SEARCH_URL="keres.php?stext="

categoriesMap = {
    "All": "",
    "Hardver": "hardver",
    "Alaplap": "hardver/alaplap/",
    "Processzor": "hardver/processzor/",
    "Memória": "hardver/memoria/",
    "Hűtés": "hardver/hutes/",
    "Ház, táp": "hardver/haz_tapegyseg/",
    "Videokártya": "hardver/videokartya/",
    "Monitor": "hardver/monitor/",
    "SSD, HDD": "hardver/merevlemez_ssd/",
    "Szerver SSD, HDD": "hardver/merevlemez_ssd/szerver_hdd_ssd/",
    "Adathordozó": "hardver/adathordozo/",
    "Hálózati termékek": "hardver/halozati_termekek/",
    "Switch, HUB": "hardver/halozati_termekek/router_switch_repeater/switch_hub/",
    "3D nyomtatás": "hardver/3d_nyomtatas/",
    "Nyomtató, szkenner": "hardver/nyomtato_szkenner/",
    "Játékvezérlő, szimulátor": "hardver/jatekvezerlo/",
    "VR": "hardver/vr/",
    "Billentyűzet, egér(pad)": "hardver/billentyuzet_eger_pad/",
    "Egyéb hardverek": "hardver/egyeb_hardverek/",
    "Retró hardverek": "hardver/retro_hardverek/",
}

categories = list(categoriesMap.keys())

def search(query: str,offset: int = 0,category: str ="All"):
    url = BASE_URL + categoriesMap[category] +  SEARCH_URL + query
    if offset != 0:
        url += "&offset="+offset

    response = requests.get(url)
    print(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: get all paragraph texts
    media_items = soup.find_all('li', class_='media')
    results = []

    # Print inner HTML of each
    for item in media_items:
        title_div = item.find('div', class_='uad-col-title')
        price_div = item.find('div', class_='uad-col-price')
    
        a_tag = title_div.find('a') if title_div else None
        title_text = a_tag.text.strip() if a_tag else 'No title'
        href = a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link'
        price_text = price_div.text.strip() if price_div else 'No price'

        #print(f'Title: {title_text} | Price: {price_text} | Link: {href}')
        results.append({
            "title": title_text,
            "price": price_text,
            "link": BASE_URL + href if href.startswith('/') else href
        })
    return results

def fetch(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('div', class_='uad-content-block').text.strip()
    price = soup.find('h2', class_='text-md-left').text.strip()
    description = soup.find('div', class_='uad-content').text.strip()
    img = soup.find('div', class_='carousel-item').find('img')['src']

    return {
        "title": title,
        "price": price,
        "description": description,
        "img": img
    }


def findCategories(url= "https://hardverapro.hu/aprok/hardver/index.html"):


    response = requests.get(url)
    print(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    categories = soup.findAll('div', class_="uad-categories-item")
    for category in categories:
        a_tag = category.find('a')
        name = a_tag.text.strip()
        href = a_tag['href'] if a_tag and a_tag.has_attr('href') else 'No link'
        href = href.rsplit('/',1)[0][6:] + '/'
        print(f"\"{name}\": \"{href}\",")


# Export it explicitly
__all__ = ['categories', 'search', 'fetch']  # optional, but good practice
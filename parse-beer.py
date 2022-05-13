from re import sub


def clean(dirty): return sub(r'[^a-zA-Z0-9 .,_°%-]', '', dirty)


def clean_num(dirty): return sub(r'\D', '', dirty)


def find_categories(_soup):
    properties = _soup.find_all('li', class_='property')
    for prop in properties:
        category = prop.find(attrs={'class': None}).text.strip(': ')
        content = clean(prop.findChild('span', class_='content').text)
        yield category, content


def find_rating(_soup):
    ratings = _soup.find('div', class_='votebar').find('div', class_='rating')
    rating = ratings.find(attrs={'class': None}).text.strip()
    rate_count = clean_num(ratings.find('div', class_='rate-count').text)
    return rating, rate_count


def find_description(_soup):
    return _soup.find('div', class_='head-block').find('div', class_='content').text


def find_price(_soup):
    _offer = _soup.select_one('.offers-block > div:nth-of-type(2)')
    price = _offer.find('div', class_='shop-price').text
    vol = _offer.find('div', class_='variants').text
    return price, vol


def yield_data(_soup):
    """
    :param _soup: Webpage of a product on wikiliq (BeautifulSoup)
    :return: Yields key and value of all the info it can get
    """

    for category, content in find_categories(_soup):
        yield category, content

    rate = find_rating(_soup)
    yield 'Rating', rate[0]
    yield 'Rate Count', rate[1]

    offer = find_price(_soup)
    yield 'Price', offer[0]
    yield 'Volume', offer[1]

    yield 'Description', find_description(_soup)

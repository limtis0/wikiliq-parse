from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    # https://wikiliq.org/brands/ENTER_CATEGORY/ preloaded and saved as a file
    with open('ENTER_HTML_FILE_PATH', 'rb') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    brands = soup.find_all('a', class_='brandcard')
    df = pd.DataFrame(columns=['brand', 'product_count', 'href'], index=range(len(brands)))

    for ind, brand in enumerate(brands):
        df['brand'][ind] = brand.findChild('div', class_='brandtitle').text
        df['product_count'][ind] = brand.findChild('div', class_='brandcount').text.replace('Products: ', '')
        df['href'][ind] = brand['href']

    # df['product_count'] = pd.to_numeric(df['product_count'])
    df.to_csv('brands.csv')

    print(df.head(3))

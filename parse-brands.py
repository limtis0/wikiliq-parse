from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    # https://wikiliq.org/brands/ENTER_CATEGORY/ preloaded and saved as a file
    with open('ENTER HTML FILE HERE', 'rb') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    brands = soup.find_all('a', class_='brandcard')
    df = pd.DataFrame(columns=['brand', 'product_count', 'href'], index=range(len(brands)))

    for ind, brand in enumerate(brands):
        df['brand'][ind] = brand.findChild('div', class_='brandtitle').text
        df['product_count'][ind] = brand.findChild('div', class_='brandcount').text.replace('Products: ', '')
        df['href'][ind] = brand['href']

    df.to_csv('brands.csv')

    print(df.head(3))

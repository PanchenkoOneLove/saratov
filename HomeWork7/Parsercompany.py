import requests
from bs4 import BeautifulSoup
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import locale


def create_top_10_companies_json(input_file, output_file):
    # Загрузка данных из файла
    with open(input_file, 'r') as file:
        data = file.read()

    # Преобразование JSON в структуру данных
    companies = json.loads(data)

    # Установка локали для удаления разделителей
    locale.setlocale(locale.LC_ALL, '')

    # Функция для удаления разделителей и преобразования строки в число
    def delocalize(string):
        return locale.atof(string.replace('.', '').replace(',', '.'))

    # Сортировка компаний по цене акций
    sorted_companies = sorted(companies, key=lambda x: delocalize(x['Price']) if isinstance(x['Price'], str) else x['Price'], reverse=True)

    # Выбор Топ 10 компаний
    top_10_companies = sorted_companies[:10]

    # Создание нового JSON объекта с Топ 10 компаниями
    top_10_json = json.dumps(top_10_companies, indent=4)

    # Запись в новый JSON файл
    with open(output_file, 'w') as file:
        file.write(top_10_json)



def create_top_10_low_pe_json(input_file, output_file):
    # Загрузка данных из файла
    with open(input_file, 'r') as file:
        data = file.read()

    # Преобразование JSON в структуру данных
    companies = json.loads(data)

    # Фильтрация компаний с ненулевым P/E
    filtered_companies = [company for company in companies if company['P/E Ratio'] != 'null']

    # Преобразование P/E в числовой тип
    for company in filtered_companies:
        if company['P/E Ratio'] is not None:
            company['P/E Ratio'] = float(company['P/E Ratio'])

    # Сортировка компаний по возрастанию P/E
    sorted_companies = sorted(filtered_companies, key=lambda x: x['P/E Ratio'] if x['P/E Ratio'] is not None else float('inf'))

    # Выбор Топ 10 компаний с самым низким P/E
    top_10_companies = sorted_companies[:10]

    # Запись в новый JSON файл
    with open(output_file, 'w') as file:
        json.dump(top_10_companies, file, indent=4)


def create_top_10_high_growth_json(input_file, output_file):
    # Загрузка данных из файла
    with open(input_file, 'r') as file:
        data = file.read()

    # Преобразование JSON в структуру данных
    companies = json.loads(data)

    # Преобразование "yearly_growth_percentage" в числовой тип
    for company in companies:
        growth_percentage = company['yearly_growth_percentage']
        if growth_percentage.endswith('%'):
            growth_percentage = growth_percentage[:-1]  # Удаление символа процента
        company['yearly_growth_percentage'] = float(growth_percentage)

    # Сортировка компаний по убыванию "yearly_growth_percentage"
    sorted_companies = sorted(companies, key=lambda x: x['yearly_growth_percentage'], reverse=True)

    # Выбор Топ 10 компаний с самым высоким ростом
    top_10_companies = sorted_companies[:10]

    # Добавление знака процента
    for company in top_10_companies:
        company['yearly_growth_percentage'] = str(company['yearly_growth_percentage']) + '%'

    # Запись в новый JSON файл
    with open(output_file, 'w') as file:
        json.dump(top_10_companies, file, indent=4)


def create_top_10_profit_json(input_file, output_file):
    # Загрузка данных из файла
    with open(input_file, 'r') as file:
        data = file.read()

    # Преобразование JSON в структуру данных
    companies = json.loads(data)

    # Фильтрация компаний с ненулевыми значениями "52 Week Low" и "52 Week High"
    filtered_companies = [company for company in companies if company['52 Week Low'] != 'null' and company['52 Week High'] != 'null']

    # Сортировка компаний по убыванию "Profit Percentage" или значениям по умолчанию
    sorted_companies = sorted(filtered_companies, key=lambda x: float(x.get('Profit Percentage', 0)), reverse=True)

    # Выбор Топ 10 компаний с наибольшей прибылью
    top_10_companies = sorted_companies[:10]

    # Запись в новый JSON файл
    with open(output_file, 'w') as file:
        json.dump(top_10_companies, file, indent=4)



def format_price_string(price_str):
    # Установка текущей локали
    locale.setlocale(locale.LC_ALL, '')

    # Проверка, содержит ли строка запятые
    if "," in price_str:
        # Удаление разделителей и замена запятой на точку
        price_str = price_str.replace(",", "")

    # Проверка, что осталось число
    try:
        price = float(price_str)
        return price
    except ValueError:
        return None


def get_currency_rate():
    url = "http://www.cbr.ru/scripts/XML_daily.asp"

    response = requests.get(url)
    xml_data = response.text

    soup = BeautifulSoup(xml_data, "xml")
    currency_element = soup.find("CharCode", string="USD")
    currency_rate = currency_element.find_next_sibling("Value").string if currency_element else None

    return float(currency_rate.replace(",", ".")) if currency_rate else None


def calculate_price_in_rubles(price_in_usd, currency_rate):
    if currency_rate is not None:
        price_in_rubles = price_in_usd * currency_rate
        return round(price_in_rubles, 2)
    else:
        return None


def get_total_pages():
    url = "https://markets.businessinsider.com/index/components/s&p_500"
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount(url, adapter)
    response = session.get(url)
    html_data = response.text

    soup = BeautifulSoup(html_data, "html.parser")
    paging_div = soup.find("div", class_="finando_paging margin-top--small")

    if paging_div is not None:
        page_links = paging_div.find_all("a")
        total_pages = len(page_links)
        return total_pages
    else:
        return 0


def get_companies_info():
    base_url = "https://markets.businessinsider.com/index/components/s&p_500?p="
    page_number = 1
    companies = []
    total_page = get_total_pages()

    while page_number != total_page + 1:
        url = base_url + str(page_number)
        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount(url, adapter)
        response = session.get(url)
        html_data = response.text

        soup = BeautifulSoup(html_data, "html.parser")
        company_elements = soup.select("table.table > tbody > tr")

        if not company_elements:
            break

        for element in company_elements:
            name_element = element.select_one("td > a")
            name = name_element.string.strip() if name_element and name_element.string else None

            company_url = "https://markets.businessinsider.com" + name_element["href"]
            company_response = session.get(company_url)
            company_html_data = company_response.text
            company_soup = BeautifulSoup(company_html_data, "html.parser")

            code_element = company_soup.select_one(".price-section__category")
            code = code_element.text.strip() if code_element else None

            price_element = company_soup.select_one(".price-section__current-value")
            price = price_element.text.strip() if price_element else None

            pe_ratio_element = company_soup.select_one(
                ".snapshot__data-item:has(.snapshot__header:-soup-contains('P/E Ratio'))")
            pe_ratio = pe_ratio_element.get_text(strip=True).replace("P/E Ratio", "") if  pe_ratio_element else None

            week_low_element = company_soup.select_one(
                ".snapshot__data-item:has(.snapshot__header:-soup-contains('52 Week Low'))")
            week_low = week_low_element.get_text(strip=True).replace("52 Week Low", "") if week_low_element else None

            week_high_element = company_soup.select_one(
                ".snapshot__data-item:has(.snapshot__header:-soup-contains('52 Week High'))")
            week_high = week_high_element.get_text(strip=True).replace("52 Week High",
                                                                       "") if week_high_element else None
            growth_elements = element.select(
                "td.table__td span.colorRed.font-color-red, td.table__td span.colorGreen.font-color-green")
            growth_percentage = growth_elements[-1].string.strip() if growth_elements else None

            company_info = {
                "Name": name,
                "Code": code,
                "Price": price,
                "P/E Ratio": pe_ratio,
                "52 Week Low": week_low,
                "52 Week High": week_high,
                "yearly_growth_percentage": growth_percentage
            }
            companies.append(company_info)

        page_number += 1

    return companies




def main():
    # Установка текущей локали
    locale.setlocale(locale.LC_ALL, '')

    # Получение данных о компаниях
    companies_info = get_companies_info()

    # Запись данных о компаниях в JSON файл
    with open("companies_info.json", "w") as file:
        json.dump(companies_info, file, indent=4)

    # Чтение данных о компаниях из JSON файла
    with open("companies_info.json", "r") as file:
        companies_info = json.load(file)
        currency_rate = get_currency_rate()

    # Обход данных о компаниях
    for company_info in companies_info:
        week_low = company_info.get("52 Week Low")
        week_high = company_info.get("52 Week High")
        price = company_info.get("Price")
        price = format_price_string(price)

        # Проверка, есть ли значения 52 Week Low, 52 Week High и Price
        if week_low is not None and week_high is not None and price is not None:
            # Преобразование цен в рубли
            price_in_rubles = calculate_price_in_rubles(price, currency_rate)

            # Добавление значения цены в рублях в словарь company_info
            company_info["Price"] = price_in_rubles

            week_low = format_price_string(week_low)
            week_high = format_price_string(week_high)

            # Проверка, что осталось число
            if isinstance(week_low, float) and isinstance(week_high, float):
                # Вычисление процента прибыли
                if week_low != 0:
                    profit_percentage = (week_high - week_low) / week_low * 100
                    company_info["Profit Percentage"] = round(profit_percentage, 2)
                else:
                    company_info["Profit Percentage"] = None
            else:
                company_info["Profit Percentage"] = None

    # Обновление JSON файла с новыми данными о прибыли
    with open("companies_info.json", "w") as file:
        json.dump(companies_info, file, indent=4)

    create_top_10_companies_json('companies_info.json', 'top_10_companies.json')
    create_top_10_low_pe_json('companies_info.json', 'top_10_low_pe_companies.json')
    create_top_10_high_growth_json('companies_info.json', 'top_10_growth_companies.json')
    create_top_10_profit_json('companies_info.json', 'top_10_profit_companies.json')

# Вызов функции main
if __name__ == "__main__":
    main()
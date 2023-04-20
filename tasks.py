import time
import datetime
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from utilities import (
    get_months_to_search,
    identify_money_format,
    count_phrase_in_article,
    create_excel_file
)

# from RPA.Robocloud.Secrets import get_secret

# Get parameters from Robocloud Secrets.
# secrets = json.loads(get_secret("work-item-secrets"))
# variables = secrets["variables"]

# Initialize variables for further use.
# months = variables["months"]
# section = variables["section"]
# search_phrase = variables["search_phrase"]

months = 1
section = "Travel"
search_phrase = "python"
browser_lib = Selenium()


def open_the_website(url, section):
    section = section.lower()
    browser_lib.open_available_browser(url + f"section/{section}")
    browser_lib.maximize_browser_window()


def extract_elements():
    dates = get_months_to_search(months)
    continue_controller = True
    article_counter = 1
    elements = []
    while continue_controller:
        try:
            list_date = []
            element_xpath = browser_lib.get_webelement(
                f'xpath=//*[@id="stream-panel"]/div[1]/ol/\
                    li[{article_counter}]/div/div[2]/span'
            )
            browser_lib.scroll_element_into_view(
                element_xpath
                )
            element_date = element_xpath.text
            element_date = datetime.datetime.strptime(
                element_date,
                '%B %d, %Y'
                )
            element_month = int(element_date.strftime('%m'))
            element_year = int(element_date.strftime('%Y'))
            list_date.append(element_month)
            list_date.append(element_year)
            if list_date in dates:
                element = browser_lib.get_webelement(
                    f'xpath=//*[@id="stream-panel"]/div[1]/ol/\
                        li[{article_counter}]/div'
                )
                # self.consolidate_elements(element)
                # browser_lib.execute_javascript("window.scrollBy(0, 200);")
                time.sleep(0.5)
                elements.append(element)
                print(article_counter)
                article_counter += 1
            else:
                continue_controller = False
        except ElementNotInteractableException:
            print(f"Error for article {article_counter}.")
    return elements


def extract_needed_information(elements):
    result = []
    for element in elements:
        elements_dict = {}
        try:
            title = element.find_element(By.TAG_NAME, 'h2').text
        except Exception:
            title = None
        try:
            date = element.find_elements(
                By.TAG_NAME,
                "span"
                )[-1].text
        except Exception:
            date = None
        try:
            description = element.find_element(
                By.TAG_NAME,
                'p'
                ).text
        except Exception:
            description = None
        try:
            image = element.find_element(
                By.TAG_NAME, 'img'
                ).get_attribute('src')
        except Exception:
            image = None
        try:
            if title and description:
                phrase_count = count_phrase_in_article(
                    title,
                    description
                    )
            else:
                phrase_count = 0
        except Exception:
            phrase_count = 0
        money_format = identify_money_format(
            title,
            description
            )
        elements_dict['title'] = title
        elements_dict['date'] = date
        elements_dict['description'] = description
        elements_dict['image'] = image
        elements_dict['phrase_count'] = phrase_count
        elements_dict['money_format'] = money_format
        result.append(elements_dict)
    create_excel_file(article_information=result)
    return result

# def search_for(term):
#     input_field = "css:input"
#     browser_lib.input_text(input_field, term)
#     browser_lib.press_keys(input_field, "ENTER")


# def store_screenshot(filename):
#     browser_lib.screenshot(filename=filename)


# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website(
            url='https://www.nytimes.com/',
            section=section
            )
        extract_needed_information(extract_elements())
    finally:
        browser_lib.close_all_browsers()


# Call the main() function, checking that we are running
# as a stand-alone script:
if __name__ == "__main__":
    main()

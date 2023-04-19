import datetime
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class AutomationTest:

    def __init__(self, section=None, months=1, search_phrase=None):
        """
        Constructor for the AutomationTest class
        """
        self.months = months
        self.section = section
        self.search_phrase = search_phrase
        self.data = []
        self.url_to_visit = 'https://www.nytimes.com/'
        self.driver = webdriver.Chrome(executable_path='./chromedriver')

    def execute(self) -> None:
        """
        This method will execute the automation.
        """
        # Initialize the driver
        driver = self.driver
        driver.implicitly_wait(0)
        driver.maximize_window()

        # Visit the url
        driver.get(self.url_to_visit)

        # Get the requested section
        section = self.get_requested_section()

        # Get the articles elements.
        article_elements = self.visit_selected_section(section)

        # Parse the elements to get the information requested.
        articles_information = self.parse_all_elements(article_elements)

        # Create the excel file.
        self.create_excel_file(article_information=articles_information)

        # Close the driver.
        automation.driver.quit()

    def get_months_to_search(self):
        """This method will return the number
        of months to search"""
        # Get actual date
        today = datetime.date.today()
        result = []
        # Get current month and year
        start_month = today.month
        start_year = today.year
        # Flag that must be changed when the year changes
        change_year = False
        # Iterate over the number of months requested
        for i in range(self.months):
            date_list = []
            # While the year is not changed, subtract according to for loop
            if not change_year:
                month = start_month - i
            else:
                month -= 1
            year = start_year

            # If the month is 0, change the year and set the month to 12
            if month == 0:
                month = 12
                start_month = 12
                start_year -= 1
                change_year = True
            date_list.append(month)
            date_list.append(year)
            result.append(date_list)
        return result[::-1]

    def get_section_dictionary(self):
        """This method will return a dictionary of all
        the sections on the nytimes.com homepage"""
        section_list = self.driver.find_element(
            By.XPATH,
            '//*[@id="app"]/div[2]/div[2]/header/div[4]'
            )
        section_links = section_list.find_elements(By.TAG_NAME, 'a')
        section_dict = {}
        for section in section_links:
            section_dict[section.text] = section.get_attribute('href')
        return section_dict

    def get_requested_section(self):
        """This method will return the requested section
        from the nytimes.com homepage"""
        section_dict = self.get_section_dictionary()
        if self.section not in section_dict:
            raise Exception('Section not found')
        return section_dict[self.section]

    def visit_selected_section(self, section):
        """This method will visit the requested section
        from the nytimes.com homepage"""
        self.driver.get(section)
        dates = self.get_months_to_search()
        continue_controller = True
        article_counter = 1
        elements = []
        while continue_controller:
            list_date = []
            element_xpath = self.driver.find_element(
                By.XPATH,
                f'//*[@id="stream-panel"]/div[1]/ol/li[{article_counter}]/div/div[2]/span'
            )
            element_date = element_xpath.text
            print(element_date)
            element_date = datetime.datetime.strptime(
                element_date,
                '%B %d, %Y'
                )
            element_month = int(element_date.strftime('%m'))
            element_year = int(element_date.strftime('%Y'))
            list_date.append(element_month)
            list_date.append(element_year)
            print(f"Fecha noticia: {list_date}")
            if list_date in dates:
                try:
                    element = self.driver.find_element(
                        By.XPATH,
                        f'//*[@id="stream-panel"]/div[1]/ol/li[{article_counter}]/div'
                    )
                    # self.consolidate_elements(element)
                    self.driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(1.4)
                except NoSuchElementException:
                    time.sleep(5)
                    element = self.driver.find_element(
                        By.XPATH,
                        f'//*[@id="stream-panel"]/div[1]/ol/li[{article_counter}]/div'
                    )
                    self.consolidate_elements(element)
                elements.append(element)
                print(article_counter)
                article_counter += 1
            else:
                continue_controller = False
        return elements

    def count_phrase_in_article(self, title, description):
        """This method will count the number of times the search
        phrase appears in the article"""
        phrase = self.search_phrase
        title_count = title.count(phrase)
        description_count = description.count(phrase)
        return title_count + description_count

    def consolidate_elements(self, element):
        elements_dict = {}
        title = element.find_element(By.TAG_NAME, 'h2').text
        date = element.find_element(
            By.XPATH,
            '/html/body/div/div[2]/main/section/div[2]/'
            'div/section/div[1]/ol/li[1]/div/div[2]/span'
        ).text
        description = element.find_element(By.TAG_NAME, 'p').text
        image = element.find_element(
            By.TAG_NAME, 'img'
            ).get_attribute('src')
        phrase_count = self.count_phrase_in_article(
            title,
            description
            ) if title or description else 0

        money_format = self.identify_money_format(
            title,
            description
            )
        elements_dict['title'] = title
        elements_dict['date'] = date
        elements_dict['description'] = description
        elements_dict['image'] = image
        elements_dict['phrase_count'] = phrase_count
        elements_dict['money_format'] = money_format
        self.data.append(elements_dict)
        return self.data

    def create_excel_file(self, article_information):
        """This method will create an excel file with
        the results of the search."""
        df = pd.DataFrame(article_information)
        df.to_excel('results.xlsx', index=False)
        return True

    def parse_all_elements(self, elements):
        result = []
        for element in elements:
            elements_dict = {}
            try:
                title = element.find_element(By.TAG_NAME, 'h2').text
            except Exception:
                title = None
            try:
                date = element.find_element(
                    By.XPATH,
                    '/html/body/div/div[2]/main/section/div[2]/'
                    'div/section/div[1]/ol/li[1]/div/div[2]/span'
                ).text
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
                    phrase_count = self.count_phrase_in_article(
                        title,
                        description
                        )
                else:
                    phrase_count = 0
            except Exception:
                phrase_count = 0
            money_format = self.identify_money_format(
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
        return result

    def identify_money_format(self, title, description):
        """This method will identify if the title or description
        of the article includes any money format."""
        # To do: Identify money format.
        format_1_description = re.search(
            r'\$\d{1,3}(,\d{3})*(\.\d+)?',
            description
        )
        format_2_description = re.search(
            r'\b\d+(\.\d+)?\s+(dollars|USD)\b',
            description,
            flags=re.IGNORECASE
        )
        format_1_title = re.search(
            r'\$\d{1,3}(,\d{3})*(\.\d+)?',
            title
        )
        format_2_title = re.search(
            r'\b\d+(\.\d+)?\s+(dollars|USD)\b',
            title,
            flags=re.IGNORECASE
            )
        return bool(
            format_1_description or format_2_description
            or format_1_title or format_2_title
            )


if __name__ == '__main__':
    # To do: Manage exceptions for inputs.
    # To do: Try border cases.
    automation = AutomationTest(
        section='World',
        months=1,
        search_phrase='Trump'
    )
    automation.execute()

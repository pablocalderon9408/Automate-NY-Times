import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


class AutomationTest:

    def __init__(self, section=None, months=1, search_phrase=None):
        """
        Constructor for the AutomationTest class
        """
        self.months = months
        self.section = section
        self.search_phrase = search_phrase

    def execute(self) -> None:
        """
        This method will execute the automation.
        """
        self.get_months_to_search()
        self.driver = webdriver.Chrome(executable_path='./chromedriver')
        driver = self.driver
        driver.implicitly_wait(0)
        driver.maximize_window()
        driver.get('https://www.nytimes.com/')
        section = self.get_requested_section()
        article_information = self.visit_selected_section(section)
        self.create_excel_file(article_information=article_information)
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
            result.append((month, year))
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
        elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            '#stream-panel li'
            )
        # To do: Logic to scroll down if the last item date is not
        # within the range requested.
        elements_list = []
        for element in elements:
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
                ) if title and description else 0

            # To do: Review wheter title or description
            # include any money format.
            elements_dict['title'] = title
            elements_dict['date'] = date
            elements_dict['description'] = description
            elements_dict['image'] = image
            elements_dict['phrase_count'] = phrase_count
            elements_list.append(elements_dict)
        return elements_list

    def count_phrase_in_article(self, title, description):
        """This method will count the number of times the search
        phrase appears in the article"""
        phrase = self.search_phrase
        title_count = title.count(phrase)
        description_count = description.count(phrase)
        return title_count + description_count

    def create_excel_file(self, article_information=None):
        """This method will create an excel file with
        the results of the search."""
        df = pd.DataFrame(article_information)
        df.to_excel('results.xlsx', index=False)
        return True


if __name__ == '__main__':
    # To do: Manage exceptions for inputs.
    # To do: Try border cases.
    automation = AutomationTest(
        section='World',
        months=10,
        search_phrase='Trump'
    )
    automation.execute()

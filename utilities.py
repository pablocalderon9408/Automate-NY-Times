"""This module contains all the functions needed for the automation"""

import datetime
import pandas as pd
import re


def get_months_to_search(months):
    """This function will return the number
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
    for i in range(months):
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


def count_phrase_in_article(phrase, title, description):
    """This method will count the number of times the search
    phrase appears in the article"""
    title_count = title.count(phrase)
    description_count = description.count(phrase)
    return title_count + description_count


def create_excel_file(article_information):
    """This method will create an excel file with
    the results of the search."""
    df = pd.DataFrame(article_information)
    df.to_excel('results.xlsx', index=False)
    return True


def identify_money_format(title, description):
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

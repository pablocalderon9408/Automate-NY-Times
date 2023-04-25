*** Settings ***
Documentation   This robot returns an excel file with information about the news retrieved. 
...             The information is stored in a table with the following columns: 
...             "Date", "Title", "Source", "Link", "Summary", "Image"
Library         task.py
Library         RPA.Tables

*** Variables ***
${url}           https://www.nytimes.com/
${months}        1
${section}       Travel
${search_phrase}    python
${path_to_file}    ${OUTPUT_DIR}

*** Keywords ***
Open the website
    [Arguments]    ${url}    ${section}
    task.open_the_website    ${url}    ${section}

Extract news information
    [Arguments]    ${path_to_file}
    task.extract_needed_information    ${path_to_file}


*** Tasks ***
Obtain news information
    Open the website    ${url}    ${section}
    Extract news information    ${path_to_file}

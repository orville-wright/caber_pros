#! /home/dbrace/venv/dave02/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import re

# URL to open
url = "https://blogs.microsoft.com/blog/2025/03/10/https-blogs-microsoft-com-blog-2024-11-12-how-real-world-businesses-are-transforming-with-ai/"

# Create a session
session = HTMLSession()

# Open the URL
response = session.get(url)

# Open data_file.txt in write mode
with open('data_file.txt', 'w') as file:
    # Write header to the file
    file.write("Section\tRow\tCompany\tURL\tDescription\n")

    # Select the XPath item
    xpath_li = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]')
    #xp_li_count = len(response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[*]/li'))
    xpath_href = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]/li[2]/a/@href')
    xpath_href_text = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]/li[1]/text()')


    # Get all data/info in this list section
    # Loop through the list items and print the href and text
    print (f" " )

    row_count = 1

    for outer in range(2, 10):
        formed_li = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[*]"
        xp_li_count = len(response.html.xpath(formed_li))
        #print (f"\n=================================================================" )
        #print (f"START section {outer} / {xp_li_count} items" )
        #print (f"Section\t Row\t   Company\n" )

        for li_element in range(1, xp_li_count + 1):
            formed_xpath = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[{li_element}]/a/@href"
            formed_href_text = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[{li_element}]/text()"

            formed_co_name = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[{li_element}]/a/strong/em/text()"
            xht_company_name = response.html.xpath(formed_co_name)
            try:
                xht_company_name[0]
            except IndexError:
                #print (f"Error: {outer} / {li_element} - NO <em> TAG -", end="" )
                formed_co_name = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[{li_element}]/a/strong/text()"
                xht_company_name = response.html.xpath(formed_co_name)
                try:
                    xht_company_name[0]
                except IndexError:
                    print (f"{outer}\t {li_element}\t BAD Data ! - Uncorrectible" )
                    break
                else:
                    #print (f" {outer} / {li_element} / {xht_company_name[0]}" )
                    pass
                
            xpath_href = response.html.xpath(formed_xpath)
            xpath_href_text = response.html.xpath(formed_href_text)
            xht_company_name = response.html.xpath(formed_co_name)

            xht_cleaned1 = re.sub(r'\\xa0', '', str(xpath_href_text))
            xht_cleaned2 = re.sub(r'\[\'', '\'', str(xht_cleaned1))
            xht_cleaned3 = re.sub(r'\'\]', '\'', str(xht_cleaned2))

            file.write(f"{outer}\t{row_count}\t'{xht_company_name[0]}'\t{xpath_href[0]}\t{xht_cleaned3}\n")
            row_count += 1
    #print (f"{xht_cleaned3}" )

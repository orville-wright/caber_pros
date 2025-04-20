#! python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
import re
import argparse
import logging
import sys


# Globals
global args
global file
global parser
args = {}
parser = argparse.ArgumentParser(description="Customer prospect data collector tool")
parser.add_argument('-d','--datafile', help='Write data out to file data_file.txt', action='store_true', dest='bool_datafile', required=False, default=False)
parser.add_argument('-p','--printonly', help='Just print the output only', action='store_true', dest='print_only', required=False, default=False)
parser.add_argument('-r','--readurl', help='scrape and display text content from URLs found', action='store_true', dest='bool_readurl', required=False, default=False)
parser.add_argument('-v','--verbose', help='verbose error logging', action='store_true', dest='bool_verbose', required=False, default=False)
parser.add_argument('-x','--xray', help='dump detailed debug data structures', action='store_true', dest='bool_xray', required=False, default=False)

# +------------------------------------------------
# | 1 - extract data and return a list[] of data
# +------------------------------------------------
def extract_data():
    # URL to open
    url = "https://blogs.microsoft.com/blog/2025/03/10/https-blogs-microsoft-com-blog-2024-11-12-how-real-world-businesses-are-transforming-with-ai/"
    # Create a session
    session = HTMLSession()
    # Open the URL
    response = session.get(url)
    temp_data_list = []
    temp_data_dict = {}
    
    # Select the XPath item
    xpath_li = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]')
    xpath_href = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]/li[2]/a/@href')
    xpath_href_text = response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[2]/li[1]/text()')
    #xp_li_count = len(response.html.xpath('/html/body/div/div[2]/section/main/div[1]/article/div/ol[*]/li'))

    # Get all data/info in this list section
    # Loop through the list items and print the href and text
    row_count = 1
    temp_data_list.clear()
    for outer in range(2, 10):
        formed_li = f"/html/body/div/div[2]/section/main/div[1]/article/div/ol[{outer}]/li[*]"
        xp_li_count = len(response.html.xpath(formed_li))

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
                    print (f"** {outer} / {li_element} / BAD Data ! - Uncorrectible" )
                    break
                else:
                    pass
                
            xpath_href = response.html.xpath(formed_xpath)
            xpath_href_text = response.html.xpath(formed_href_text)
            xht_company_name = response.html.xpath(formed_co_name)

            xht_cleaned1 = re.sub(r'\\xa0', '', str(xpath_href_text))
            xht_cleaned2 = re.sub(r'\[\'', '\'', str(xht_cleaned1))
            xht_cleaned3 = re.sub(r'\'\]', '\'', str(xht_cleaned2))

            temp_data_dict = ({'Row': row_count, 'Sec': outer, 'Co': xht_company_name[0], 'URL': xpath_href[0], 'Desc': xht_cleaned3})
            temp_data_list.append(temp_data_dict)   # list where each row is a dict

            row_count += 1
    return temp_data_list  # entire data set is in this list

# +------------------------------------------------
# | 2 - This is where you want to add LLM summarization, sentiment analysis, etc.
# +------------------------------------------------
def scrape_and_display_text(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render(sleep=1)  # Render JavaScript if needed
        # Extract all text content from the body
        text_content = response.html.xpath('//body//text()')
        # Join and clean text content
        cleaned_text = ' '.join([t.strip() for t in text_content if t.strip()])
        print(f"\n--- Text content from {url} ---\n")
        print(cleaned_text[:2000])  # Display first 2000 characters for brevity
        print("\n--- End of content ---\n")
    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
    finally:
        session.close()

# +------------------------------------------------
# | 3
# +------------------------------------------------
def close_file(file):
    file.close()
    print ( "Closing file data_file.txt" )
    print ( " " )
    return

# +------------------------------------------------
# | 0 - Main program
# +------------------------------------------------

def main():
    final_list = []
    args = vars(parser.parse_args())        # args as a dict []
    if args['bool_verbose'] is True:        # Logging level
        print ( "Enabeling verbose info logging..." )
        logging.disable(0)                  # Log level = OFF
    else:
        logging.disable(20)                 # Log lvel = INFO

    if args['bool_datafile'] is True:
        print ( " " )
        print ( f"dumping data to file: data_file.txt" )
        # Open data_file.txt in write mode
        with open('data_file.txt', 'a') as file:
            final_list = extract_data()
            # Write each row (dict element) to the file
            for row in final_list:
               file.write(f"{row}\n")
            close_file(file)

    if args['bool_readurl']:
        print ( " " )
        print ( f"Recursive;y scraping every URL" )    # We will scrape URLs found in the main extraction process and display text
        final_list = extract_data()
        for row in final_list:
            data_url = row["URL"]
            print (f"Scraping URL: {data_url}" )
            scrape_and_display_text(data_url)

    if args['print_only']:
        print ( " " )
        print ( f"data file will NOT be created" )
        final_list = extract_data()
        for row in final_list:
            data = row["URL"]
            print (f"{data}" )

    if len(sys.argv) == 1:  # Only script name was provided
        print("No options provided - doing nothing!")
        parser.print_help()
        print ( " " )
    # End of main program   
    
# ==========================================================
if __name__ == '__main__':
    main()


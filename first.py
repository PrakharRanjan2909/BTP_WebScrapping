import requests
from bs4 import BeautifulSoup
import os

# Replace "new_link" with the actual URL of the website
url = "https://etherscan.io/charts"
url_home = "https://etherscan.io"

# Set a user-agent header to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Send a GET request with headers
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    grand_parent = soup.find('div', {'class': 'col-lg-9 col-xl-10'})

    # Find the parent section with classname="parent" and id="parent_id"
    parent_sections = grand_parent.find_all(
        'section', {'class': 'offset-scroll border-bottom pb-10 mb-10'})
    for parent_section in parent_sections:

        parent_title_element = parent_section.find(
            'h2', class_='fs-base fw-medium mb-5')

        parent_title = parent_title_element.text.strip()

        print(f"Parent Title: {parent_title}")
        
        
        folder_path = os.path.join('output', parent_title)
        os.makedirs(folder_path, exist_ok=True)

        # Find all <a> tags with classname="card link-dark h-100" inside the parent section
        link_elements = parent_section.find_all(
            'a', class_='card link-dark h-100')

        for link_element in link_elements:
            # Extract the href attribute (link)
            link = link_element['href']

            # Extract the title text inside <h3> with classname="h6 fw-normal mb-6"
            title_element = link_element.find('h3', class_='h6 fw-normal mb-6')
            title = title_element.text.strip()

            # Print the link and title
            print(f"Link: {link}, Title: {title}\n")

            graph_url = url_home + link

            graph_response = requests.get(graph_url, headers=headers)

            if graph_response.status_code == 200:
                graph_soup = BeautifulSoup(graph_response.text, 'html.parser')
                csv_element = graph_soup.find(
                    'div', class_='col-12 mb-5 mb-lg-0 col-lg-8 col-xl-9')

                if csv_element is None:
                    print(f"CSV format cannot not found. Skipping...")
                    continue

                # inside_p = csv_element.find(
                #     'p', class_='d-flex align-items-baseline fs-sm text-muted gap-1 mb-3')
                data_csv = csv_element.find('a')
                csv_format = url_home + data_csv['href']

                # Extract the title text inside <h3> with classname="h6 fw-normal mb-6"
                title_element = link_element.find(
                    'h3', class_='h6 fw-normal mb-6')
                title = title_element.text.strip()

                # Download in the form of the CSV file
                csv_response = requests.get(csv_format, headers=headers)
                

                if csv_response.status_code == 200:
                    # Save the content to a local CSV file with the title as the filename
                    csv_filename = f"{title}.csv"
                    file_path = os.path.join(folder_path, csv_filename)
                    with open(file_path, 'wb') as csv_file:
                        csv_file.write(csv_response.content)
                    print(
                        f"Graph Data Downloaded in form of '{csv_filename}' successfully.")
                else:
                    print(
                        f"Failed to download the data. Status code: {csv_response.status_code}")
            else:
                print(
                    f"Failed to fetch the graph page. Status code: {graph_response.status_code}")


else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")

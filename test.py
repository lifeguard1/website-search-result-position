import requests
import csv
import time
import json

# Configuration
API_KEY = ''  # Replace with your API key
CX = ''  # Replace with your Custom Search Engine ID
keywords = [""]  # Add more keywords as needed
target_url = ""
max_results = 100  # Maximum number of results to search

def get_search_results(query, start):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}&start={start}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def check_keyword_position(keyword):
    for start in range(1, max_results + 1, 10):
        results = get_search_results(keyword, start)
        
        # Debugging: Print the entire response
        print(f"Results for '{keyword}' starting at {start}:")
        print(json.dumps(results, indent=2))
        
        if 'items' not in results:
            print(f"No items found in results for start={start}")
            continue

        for i, item in enumerate(results['items'], start=start):
            print(f"Checking item {i}: {item['link']}")
            if target_url in item['link']:
                return i
    return None

def main():
    results = []
    for keyword in keywords:
        print(f"Checking keyword: {keyword}")
        position = check_keyword_position(keyword)
        results.append([keyword, position])
        time.sleep(1)  # To avoid hitting API rate limits

    with open('keyword_positions.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Keyword", "Position"])
        writer.writerows(results)
    
    for result in results:
        print(f"Keyword: {result[0]}, Position: {result[1]}")

if __name__ == "__main__":
    main()

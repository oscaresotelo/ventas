import csv
import asyncio

from duckduckgo_search import AsyncDDGS


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

async def aget_results(query):
    search = AsyncDDGS(headers=headers, proxies=None)
    results = await search.text(query, max_results=100)
    return results

async def aget_multiple_results(query_list):
    tasks = [aget_results(query) for query in query_list]
    results = await asyncio.gather(*tasks)
    results_all = []
    for result in results:
        results_all.extend(result)
    return results_all

if __name__ == '__main__':
    queries = [
        "retail shop in England that sells Marine fish",
        "retail shop in England that sells Invertebrates",
        "retail shop in England that sells Corals",
        "retail shop in England that sells Ornamental Fresh",
        "retail shop in England that sells Coldwater fish"
    ]
    data = asyncio.run(aget_multiple_results(queries))

    # Specify the CSV file name
    csv_file_name = 'business_info.csv'

    # Open the file in write mode
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        
        # Write the header row
        writer.writeheader()
        
        # Write the data rows
        for row in data:
            writer.writerow(row)  
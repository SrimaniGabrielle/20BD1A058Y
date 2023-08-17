from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def fetch_numbers(url):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=0.5)
        data = response.json()
        if "numbers" in data:
            return data["numbers"]
        else:
            return []
    except (requests.exceptions.RequestException, asyncio.TimeoutError):
        return []

async def get_unique_sorted_numbers(urls):
    tasks = [fetch_numbers(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    merged_numbers = set()
    for nums in results:
        merged_numbers.update(nums)
    
    return sorted(list(merged_numbers))

@app.route('/numbers', methods=['GET'])
def numbers():
    urls = request.args.getlist('url')
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    unique_sorted_numbers = loop.run_until_complete(get_unique_sorted_numbers(urls))
    loop.close()
    
    return jsonify({"numbers": unique_sorted_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)

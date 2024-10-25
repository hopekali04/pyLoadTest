import asyncio
import aiohttp
import time

# Function to send a single request asynchronously
async def send_request(session, url, method, payload=None, headers=None):
    try:
        async with session.request(method, url, json=payload, headers=headers) as response:
            status = response.status
            data = await response.text()
            return status, data
    except Exception as e:
        return None, str(e)

# Main function to run the load test
async def run_load_test(url, num_requests, method, payload=None, headers=None, delay_between_batches=None):
    async with aiohttp.ClientSession() as session:
        tasks = []
        start_time = time.time()

        for i in range(num_requests):
            # Create an async task to send the request
            task = asyncio.create_task(send_request(session, url, method, payload, headers))
            tasks.append(task)

            # If a delay between batches is specified, wait before sending the next request
            if delay_between_batches and (i + 1) % delay_between_batches == 0:
                await asyncio.sleep(1)  # Sleep for 1 second between batches

        # Wait for all tasks (requests) to complete
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Analyze results
        successful_requests = [res for res in results if res[0] == 200]
        failed_requests = [res for res in results if res[0] != 200]
        total_time = end_time - start_time

        # Report results
        print(f"Total Requests: {num_requests}")
        print(f"Successful Requests: {len(successful_requests)}")
        print(f"Failed Requests: {len(failed_requests)}")
        print(f"Total Time: {total_time:.2f} seconds")
        if successful_requests:
            print(f"Average Time per Request: {total_time / num_requests:.2f} seconds")

# Collect user inputs
url = input("Enter the API endpoint URL: ")
num_requests = int(input("Enter the number of requests to send: "))
method = input("Enter the HTTP method (GET, POST, etc.): ").upper()
payload = input("Enter the request payload (optional, leave blank if none): ") or None
headers_input = input("Enter any headers as a JSON string (optional, leave blank if none): ") or None
headers = eval(headers_input) if headers_input else None
delay_between_batches = int(input("Enter delay after how many requests (optional, leave blank if none): ") or 0)


asyncio.run(run_load_test(url, num_requests, method, payload, headers, delay_between_batches))

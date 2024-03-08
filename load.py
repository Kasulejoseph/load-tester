import argparse
import math

import requests
import time
import threading
import concurrent.futures

status_code_1xx = 0
status_code_2xx = 0
status_code_3xx = 0
status_code_4xx = 0
status_code_5xx = 0
exception_errors = 0
start_time = time.perf_counter()


def make_requests(url, no_requests):
    global status_code_2xx, status_code_3xx, status_code_4xx, status_code_5xx, status_code_1xx
    for _ in range(int(no_requests)):
        res = requests.get(url)
        # time.sleep(1)
        if res.status_code in range(100, 200):
            status_code_1xx += 1

        if res.status_code in range(200, 300):
            status_code_2xx += 1

        if res.status_code in range(300, 400):
            status_code_3xx += 1

        if res.status_code in range(400, 500):
            status_code_4xx += 1

        if res.status_code in range(500, 600):
            status_code_5xx += 1


# def make_requests(url):
#     global status_code_count
#     res = requests.get(url)
#     # time.sleep(1)
#     if res.status_code == 200:
#         status_code_count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--U', dest='URL', help='provide URL')

    parser.add_argument(
        '--n', dest='number_of_requests', help='Number of requests to make')

    parser.add_argument(
        '--c', dest='number_of_concurrency', help='Number of requests running concurrently')

    args = parser.parse_args()

    threads = []
    requests_per_user = int(args.number_of_requests) / int(args.number_of_concurrency)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(make_requests, args.URL, requests_per_user) for _ in
                   range(int(args.number_of_concurrency))]

        for future in concurrent.futures.as_completed(results):
            try:
                data = future.result()
            except Exception as exc:
                exception_errors += 1
                print("generated an exception: ", exc)

    # for _ in range(int(args.number_of_requests)):
    #     t = threading.Thread(target=make_requests, args=[args.URL])
    #     t.start()
    #     threads.append(t)
    #
    # for thread in threads:
    #     thread.join()

    # make_requests(args.URL, args.number_of_requests)
    finish_time = time.perf_counter()
    print("Total Requests (1XX).......................:", status_code_1xx)
    print("Total Requests (2XX).......................:", status_code_2xx)
    print("Total Requests (3XX).......................:", status_code_3xx)
    print("Total Requests (4XX).......................:", status_code_4xx)
    print("Total Requests (5XX).......................:", status_code_5xx)
    print("Total Exception Errors.......................:", exception_errors)
    print()
    print(f"finished in {round(finish_time - start_time, 2)} seconds")

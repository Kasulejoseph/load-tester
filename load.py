import argparse
import requests
import time
import threading

status_code_count = 0
start_time = time.perf_counter()


# def make_requests(url, no_requests):
#     global status_code_count
#     for _ in range(int(no_requests)):
#         res = requests.get(url)
#         time.sleep(1)
#         if res.status_code == 200:
#             status_code_count += 1


def make_requests(url):
    global status_code_count
    res = requests.get(url)
    # time.sleep(1)
    if res.status_code == 200:
        status_code_count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--U', dest='URL', help='provide URL')

    parser.add_argument(
        '--n', dest='number_of_requests', help='Number of requests to make')

    args = parser.parse_args()

    threads = []

    for _ in range(int(args.number_of_requests)):
        t = threading.Thread(target=make_requests, args=[args.URL])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # make_requests(args.URL, args.number_of_requests)
    finish_time = time.perf_counter()
    print("successes: ", status_code_count)
    print(f"finished in {round(finish_time - start_time, 2)} seconds")


import threading
import time
import random

def threadPrint(thread_id):
    print(f"Hi, i'm thread {thread_id}")
    
    sleep_time = random.randint(1, 10)
    time.sleep(sleep_time)
    
    print(f"Bye, Bye! From the thread {thread_id} my sleep was: {sleep_time} seconds!")

def main():
    threads = []

    for i in range(0, 3): 
        thread = threading.Thread(target=threadPrint, args=(i,))
        thread.start()
        threads.append(thread)

    # Wait end computation of all threads
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

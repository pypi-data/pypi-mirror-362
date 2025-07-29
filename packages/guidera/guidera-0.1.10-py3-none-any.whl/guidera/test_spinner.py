import sys
import time

spinner = ['|', '/', '-', '\\']
for i in range(20):
    text = f'Fetching response {spinner[i % len(spinner)]}\r'
    sys.stdout.write('\r' + text.strip('\r'))
    sys.stdout.flush()
    time.sleep(0.1)
sys.stdout.write('\n')  # Move to the next line after done
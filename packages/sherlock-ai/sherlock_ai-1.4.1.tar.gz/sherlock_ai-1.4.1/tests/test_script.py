from constants import HELLO_WORLD, KUNAL_AGGARWAL, NUM_CONST_30, NUM_CONST_42, NUM_CONST_70, URL_HTTPSEXAMPLE_COM
from src.sherlock_ai import hardcoded_value_detector


@hardcoded_value_detector
def first_function():
    message = HELLO_WORLD
    number = NUM_CONST_42
    print(message)
    print(f'Value: {number}')


@hardcoded_value_detector
def second_function():
    url = URL_HTTPSEXAMPLE_COM
    timeout = NUM_CONST_30
    print(f'Connecting to {url} with timeout {timeout}')


@hardcoded_value_detector
def third_function():
    s = KUNAL_AGGARWAL
    num = NUM_CONST_70
    print(f'Connecting to {s} with timeout {num}')


if __name__ == '__main__':
    first_function()
    second_function()
    third_function()

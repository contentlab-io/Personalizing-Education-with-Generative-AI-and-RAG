## Decorators

Decorators allow you to modify the behavior of a function or class. They are a powerful tool for extending and modifying the behavior of callable objects (functions, methods) without permanently modifying the callable itself.

### Example:

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

## Generators
Generators provide a way for generating iterables in a lazy fashion, meaning they generate items only one at a time and only when asked, thus being more memory efficient.

### Example:
```python
def countdown(num):
    print('Starting')
    while num > 0:
        yield num
        num -= 1

for x in countdown(5):
    print(x)
```

## Context Managers
Context managers are a great feature for resource management, such as file operations or network connections, ensuring that resources are properly managed and cleaned up after use.

### Example:
```python
with open('file.txt', 'r') as f:
    file_contents = f.read()

``` 

## Multithreading
Multithreading is a way to achieve multitasking by running multiple threads (lighter-weight processes) concurrently, making efficient use of CPU.

### Example:
```python
import threading

def print_numbers():
    for i in range(5):
        print(i)

def print_letters():
    for letter in 'abcde':
        print(letter)

t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

t1.start()
t2.start()

t1.join()
t2.join()
```


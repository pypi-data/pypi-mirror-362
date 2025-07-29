from src.kamalfirstpackage.core import say_hello
from src.kamalfirstpackage.core2 import say_hello2

def main():
    name = "Kamal"
    greeting = say_hello(name)
    print(greeting)
    
    another_greeting = say_hello2("Kamal")
    print(another_greeting)
    
if __name__ == "__main__":
    main()
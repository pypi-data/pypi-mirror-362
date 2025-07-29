from src import say_hello, say_hello2

def main():
    name = "Kamal"
    greeting = say_hello(name)
    print(greeting)
    
    another_greeting = say_hello2("Shiva")
    print(another_greeting)
    
if __name__ == "__main__":
    main()
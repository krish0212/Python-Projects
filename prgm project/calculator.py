while True:
    print("\n===== Calculator =====")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    choice = input("Enter your choice: ")
    if choice == "5": 
        print("Thank You!") 
        break
        
    elif choice in ["1", "2", "3", "4"]:
        x = int(input("Enter first number: "))
        y = int(input("Enter second number: "))

        if choice == "1":
            z = x + y
            print("Addition value is:", z)

        elif choice == "2":
            z = x - y
            print("Subtraction value is:", z)

        elif choice == "3":
            z = x * y
            print("Multiplication value is:", z)
            
        elif choice == "4":
            if y == 0:
                print("Error: Cannot divide by zero!")
            else:
                z = x / y
                print("Division value is:", z)
                
    else:
        print("Invalid Choice!")
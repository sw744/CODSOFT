# Simple Calculator in Standard Form

def main():
    print("Welcome to the Simple Calculator!")

    # Prompt user for the first number
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Prompt user for the second number
    while True:
        try:
            num2 = float(input("Enter the second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Prompt user to choose an operation
    print("\nSelect an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    operation = input("Enter the operation symbol (+, -, *, /): ").strip()

    # Perform calculation based on user choice
    if operation == '+':
        result = num1 + num2
        op_symbol = '+'
    elif operation == '-':
        result = num1 - num2
        op_symbol = '-'
    elif operation == '*':
        result = num1 * num2
        op_symbol = '*'
    elif operation == '/':
        if num2 == 0:
            print("Error: Division by zero is undefined.")
            return
        result = num1 / num2
        op_symbol = '/'
    else:
        print("Invalid operation selected.")
        return

    # Display the result
    print(f"\nResult: {num1} {op_symbol} {num2} = {result}")

if __name__ == "__main__":
    main()
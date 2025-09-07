from functions.run_python_file import run_python_file

def main():
    print('run_python_file("calculator", "main.py"):')
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print()
    
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print()
    
    print('run_python_file("calculator", "tests.py"):')
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print()
    
    print('run_python_file("calculator", "../main.py"):')
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print()
    
    print('run_python_file("calculator", "nonexistent.py"):')
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)

if __name__ == "__main__":
    main()
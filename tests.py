from functions.write_file import write_file

def main():
    # Test 1: Write to lorem.txt (should succeed)
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)
    print()
    
    # Test 2: Write to pkg/morelorem.txt (should succeed and create directory if needed)
    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result2)
    print()
    
    # Test 3: Try to write outside working directory (should fail)
    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result3)

if __name__ == "__main__":
    main()
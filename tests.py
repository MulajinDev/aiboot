from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

def main():
    
    print("running tests:")

    info_tests = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../")
    ]

    #for test in info_tests:
    #    text = get_files_info(test[0], test[1])
    #    #print(f"test = {test[0]}, {test[1]}")
    #   print(text)

    read_tests = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py")
    ]

    #for test in read_tests:
    #    text = get_file_content(test[0], test[1])
    #    #print(f"test = {test[0]}, {test[1]}")
    #    print(text)

    write_tests = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    #for test in write_tests:
    #    text = write_file(test[0], test[1], test[2])
    #    #print(f"test = {test[0]}, {test[1]}, {test[2]}")
    #    print(text)

    run_tests = [
        ("calculator", "main.py"),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py"),
        ("calculator", "../main.py"),
        ("calculator", "nonexistent.py")
    ]

    for test in run_tests:
        if len(test) == 2:
            text = run_python_file(test[0], test[1])
            #print(f"test = {test[0]}, {test[1]}")
        elif len(test) == 3:
            text = run_python_file(test[0], test[1], test[2])
            #print(f"test = {test[0]}, {test[1]}, {test[2]}")
        print(text)

    exit(0)

main()
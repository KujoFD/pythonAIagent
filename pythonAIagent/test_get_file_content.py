from functions.get_file_content import get_file_content

print(get_file_content("calculator", "lorem.txt"))
print(f'Result for directory calculator and file main.py:\n{get_file_content("calculator", "main.py")}')
print(f'Result for directory calculator and file pkg/calculator:\n{get_file_content("calculator", "pkg/calculator.py")}')
print(f'Result for directory calculator and file /bin/cat:\n{get_file_content("calculator", "/bin/cat")}')
print(f'Result for directory calculator and file pkg/does_not_exist.py:\n{get_file_content("calculator", "pkg/does_not_exist.py")}')

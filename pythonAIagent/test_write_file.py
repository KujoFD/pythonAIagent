from functions.write_file import write_file

print(f'Result from directory calculator, file_path lorem.txt, and content "wait, this isnt lorem ipsum":\n{write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}')
print(f'Result from directory calculator, file_path pkg/morelorem.txt, and content "lorem ipsum dolor sit amet":\n{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}')
print(f'Result from directory calculator, file_path /tmp/temp.txt. and content "this should not be allowed":\n{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}')

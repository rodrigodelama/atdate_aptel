import sys

argv_str = " "
argv_str.join(sys.argv[index] for index in sys.argv)
print(argv_str)


argv_str = argv_str.join(str(index) for index in sys.argv)
print("argv_str: ", argv_str)

import os

# print(os.getcwd())
os.chdir('../01_Paramiko')
# print(os.getcwd())
# print(len(os.listdir()))
# print(f"Current working directory is {os.getcwd()}")
# print(os.system('ls -larth'))

files = (os.listdir())
files.sort()
for file in files:
    # print(file)
    with open(file) as file_data:
        if "paramiko" in file.casefold():
            #print(print(f"\n\n{'#'*10} {file} {'#'*10}"))
            print(type(file_data))
            print(dir(file_data))
            # print(file_data.read())


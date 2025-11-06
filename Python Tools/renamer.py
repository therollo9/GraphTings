import os


def main():
    # path = "Python Tools/in-ear/"
    path = "Python Tools/over-ear/"
    new_last = " L.txt"
    new_last_hp = " L1.txt"
    # print("Hello World")
    for file in os.listdir(path):
        file_name, file_extension = os.path.splitext(file)
        if file_extension == "":
            continue
        elif file_extension == ".csv":
            if path == "Python Tools/over-ear/":
                new_file = file_name + new_last_hp
            else:
                new_file = file_name + new_last
            os.rename(path + file, path + new_file)
        else:
            continue


if __name__ == '__main__':
    main()

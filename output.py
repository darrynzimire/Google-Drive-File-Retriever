import os


def output_dir():
    directory = './retrieved_raw_files'
    file_path = os.path.join(directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)

    return file_path


def search_files(file_list):
    with open(file_list) as handle:
        for i in handle:
            print(i)


def write_to_folder(file):
    pass


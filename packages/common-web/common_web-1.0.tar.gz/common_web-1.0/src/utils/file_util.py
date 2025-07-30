import json
import os


def read_files_in_folder(file_path):
    """
    read all file path in the folder
    :param file_path:
    :return: file path list
    """
    file_path_list = []
    for root, dirs, files in os.walk(file_path):
        # 平铺所有目录，每个根目录中是否存在目录，是否存在文件
        for file_name in files:
            file_path_list.append(os.path.join(root, file_name))
    return file_path_list


def write_json_to_file(file_path, data, encoding='UTF-8'):
    """
    write json data to file
    :param encoding: default 'UTF-8'
    :param file_path: root + file name
    :param data: json
    :return:
    """
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False)

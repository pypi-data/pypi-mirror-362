
import os
import zipfile

def zip_folder(folder_path, output_path):
    ''' 将文件夹压缩成一个ZIP文件'''
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 创建ZIP文件中的文件路径
                zip_path = os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..'))
                # 将文件添加到ZIP文件中
                zipf.write(os.path.join(root, file), zip_path)


def zip_files(file_paths:list, output_path=''):
    '''将多个文件压缩成一个ZIP文件'''
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            # 创建ZIP文件中的文件路径
            zip_path = os.path.relpath(file_path, os.path.dirname(file_paths[0]))
            # 将文件添加到ZIP文件中
            zipf.write(file_path, zip_path)
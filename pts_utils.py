from hmac import new
import os
import json
import pdb
from PIL import Image
from tqdm import tqdm
import random
import shutil



def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths

def read_file(file_path):
    file_extension = file_path.split(".")[-1].lower()

    if file_extension == "jsonl":
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            data = [json.loads(line.strip()) for line in lines]
            return data

    elif file_extension == "json":
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if type(data) == list else [data]

    elif file_extension == "txt":
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    elif file_extension == "csv":
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_str = file.read()
            return csv_str
    else:
        print("Unsupported file format")
        return None

def get_file_name(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name = os.path.splitext(file_name_with_extension)[0]
    return file_name

def save_list_to_file(data_list, file_path, indent = None):
    save_dir = os.path.dirname(file_path)
    if save_dir=="":
        save_dir="."
    create_folder_if_not_exists(save_dir)
    file_extension = file_path.split(".")[-1].lower()

    if file_extension == "json":
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent = indent)
        print(f"List saved to JSON file: {file_path}")
    elif file_extension == "jsonl":
        with open(file_path, "w", encoding="utf-8") as file:
            for item in data_list:
                json_str = json.dumps(item, indent=indent)
                file.write(json_str + '\n')
        print(f"List saved to JSONL file: {file_path}")
    elif file_extension == "txt":
        with open(file_path, "w", encoding="utf-8") as file:
            for item in data_list:
                file.write(str(item) + "\n")
        print(f"List saved to TXT file: {file_path}")
    else:
        print("Unsupported file format")

def save_dict_to_file(data_dict, file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
            print(f"Dictionary saved to {file_path}")
    elif file_path.endswith('.jsonl'):
        with open(file_path, 'w') as jsonl_file:
            jsonl_file.write(json.dumps(data_dict, indent=4))
            print(f"Dictionary saved to {file_path}")
    else:
        print("Unsupported file format. Please provide a .json or .jsonl file path.")

def reconstruct_sentence(word_list):
    punctuation_list=[".", ",", ":", ";", "!", "?"]
    sentence = ""
    for i, word in enumerate(word_list):
        if word in punctuation_list:
            sentence += word
        elif i > 0 :
            sentence += " "
            sentence += word
        else:
            sentence += word

    return sentence


def check_resolution(image_path, resolution=10):
    try:
        img = Image.open(image_path)
        width, height = img.size
        if width > resolution and height > resolution:
            return True  # 图片的水平和竖直分辨率均大于 resolution
        else:
            return False  # 图片的水平和/或竖直分辨率小于等于 resolution
    except Exception as e:
        print(f"Error: {e}")
        return False  # 处理图像时出现异常，返回 False

def split_list(lst, num_parts):
    avg = len(lst) // num_parts
    remainder = len(lst) % num_parts
    result = []
    start = 0
    for i in range(num_parts):
        end = start + avg + (1 if i < remainder else 0)
        result.append(lst[start:end])
        start = end
    return result


def random_sample(input_list, n):
   
    # 使用 random.choices 进行随机采样，允许 n 大于等于列表长度
    sampled_list = random.choices(input_list, k=n)
    return sampled_list


def copy_file(src, dst):
    """
    复制文件从路径a到路径b.

    参数:
    src (str): 源文件路径
    dst (str): 目标文件路径
    """
    try:
        shutil.copy(src, dst)
        print(f"文件已从 {src} 复制到 {dst}")
    except FileNotFoundError:
        print(f"错误: 文件 {src} 未找到")
    except PermissionError:
        print(f"错误: 无法访问 {dst}")
    except Exception as e:
        print(f"发生错误: {e}")



if __name__=="__main__":
 

    images = get_file_paths("/data/share/potato/data/LAION-Aesthetics/images")
    images = [x for x in images if x.endswith("jpg")]
    print(len(images))
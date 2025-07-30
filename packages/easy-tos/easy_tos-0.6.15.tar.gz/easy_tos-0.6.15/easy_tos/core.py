import tos 
import os
from typing import List, Dict
import io
from PIL import Image
import json 
import subprocess
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import pandas as pd
import shutil
import traceback

def print_cuda_memory(tag=""):
    import torch
    allocated = torch.cuda.memory_allocated() / 1024**2
    reserved = torch.cuda.memory_reserved() / 1024**2
    print(f"[{tag}] Allocated: {allocated:.2f} MB, Reserved: {reserved:.2f} MB")

class CropToForegroundSquare:
    def __init__(self, padding=0, threshold=10, target_size=None):
        """
        padding: Amount of padding to apply around the cropped square.
        threshold: Intensity threshold to consider a pixel as part of the foreground.
        target_size: Final output size (int or tuple). If int, output will be (target_size, target_size).
        """
        self.padding = padding
        self.threshold = threshold
        self.target_size = target_size if isinstance(target_size, tuple) else (target_size, target_size) if target_size else None

    def __call__(self, img):
        import numpy as np 
        import cv2 
        """
        img: PIL RGB Image (JPG-compatible)
        """
        # Convert to grayscale
        grayscale_image = img.convert("L")
        grayscale_image = np.array(grayscale_image)

        # Threshold and dilate to find foreground
        _, binary_image = cv2.threshold(grayscale_image, 254, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(binary_image, kernel, iterations=1)
        mask = np.where(mask < 255, 1, 0)

        # Find foreground bounds
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        if not np.any(rows) or not np.any(cols):
            result = img
        else:
            r_min, r_max = np.where(rows)[0][[0, -1]]
            c_min, c_max = np.where(cols)[0][[0, -1]]

            # Apply padding
            r_min = max(r_min - self.padding, 0)
            r_max = min(r_max + self.padding, img.height - 1)
            c_min = max(c_min - self.padding, 0)
            c_max = min(c_max + self.padding, img.width - 1)

            # Square bounding box
            square_size = max(r_max - r_min + 1, c_max - c_min + 1)
            center_h = (r_min + r_max) // 2
            center_w = (c_min + c_max) // 2
            left = max(center_w - square_size // 2, 0)
            top = max(center_h - square_size // 2, 0)
            right = min(left + square_size, img.width)
            bottom = min(top + square_size, img.height)

            # Crop
            square_img = img.crop((left, top, right, bottom))

            # Pad if needed
            if square_img.size != (square_size, square_size):
                padded_img = Image.new('RGB', (square_size, square_size), (0, 0, 0))
                paste_x = (square_size - square_img.width) // 2
                paste_y = (square_size - square_img.height) // 2
                padded_img.paste(square_img, (paste_x, paste_y))
                result = padded_img
            else:
                result = square_img

        # Resize if target_size is set
        if self.target_size:
            result = result.resize(self.target_size, Image.LANCZOS)

        return result

def clean_local_cache(paths_list, verbose=False):
    """
    Deletes files or directories specified in paths_list.

    :param paths_list: List of file or directory paths to delete.
    """
    for path in paths_list:
        try:
            if os.path.exists(path):
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)  # Remove file or symlink
                    if verbose:
                        print(f"Deleted file: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)  # Remove directory and its contents
                    if verbose:
                        print(f"Deleted directory: {path}")
            else:
                if verbose:
                    print(f"Path does not exist: {path}")
        except Exception as e:
            if verbose:
                print(f"Error deleting {path}: {e}")
    

def multi_process_tasks(data_list, 
                       func,
                       map_func = None,
                       max_workers=os.cpu_count(),
                       desc='Processing objects',
                       verbose=False
    ):
    results = []
    def _id(input):
        return input
    
    if map_func is None:
        map_func = _id
        
    with tqdm(total=len(data_list)) as pbar:
        future_to_path = {}
        success_count = 0
        fail_count = 0 
        pbar.set_description(desc)
        pbar.set_postfix({'✅ Success': success_count, '❌ Fail': fail_count})
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for data in data_list:
                future_to_path[executor.submit(func, data)] = map_func(data)
            for future in as_completed(future_to_path):
                taskID = future_to_path[future]
                try:
                    result = future.result()
                    success_count += 1
                    if result is not None:
                        results.append(f"{taskID}:{result}")
                except Exception as exc:
                    fail_count += 1
                    print(f'{taskID} generated an exception: {exc}')
                    if verbose:
                        traceback.print_exc()
                finally:
                    pbar.update(1)
                    pbar.set_postfix({'✅ Success': success_count, '❌ Fail': fail_count})
    print(f"\nAll Done! ✅ Success: {success_count} | ❌ Fail: {fail_count}")
    return results


def multi_thread_tasks(data_list, 
                       func,
                       map_func = None,
                       max_workers=os.cpu_count(),
                       desc='Processing objects',
                       verbose=False
    ):
    results = []
    def _id(input):
        return input
    
    if map_func is None:
        map_func = _id
        
    with tqdm(total=len(data_list)) as pbar:
        future_to_path = {}
        success_count = 0
        fail_count = 0 
        pbar.set_postfix({'✅ Success': success_count, '❌ Fail': fail_count})
        pbar.set_description(desc)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for data in data_list:
                future_to_path[executor.submit(func, data)] = map_func(data)
            for future in as_completed(future_to_path):
                taskID = future_to_path[future]
                try:
                    result = future.result()
                    success_count += 1
                    if result is not None:
                        results.append(f"{taskID}:{result}")
                except Exception as exc:
                    fail_count += 1
                    print(f'{taskID} generated an exception: {exc}')
                    if verbose:
                        traceback.print_exc()
                finally:
                    pbar.update(1)
                    pbar.set_postfix({'✅ Success': success_count, '❌ Fail': fail_count})
    print(f"\nAll Done! ✅ Success: {success_count} | ❌ Fail: {fail_count}")
    return results

def split_task_to_nodes(all_uids, nodes, gpus, verbose=False):
    # Split UIDs among nodes
    node_uid_list = []
    chunk_size = len(all_uids) // nodes
    remainder = len(all_uids) % nodes

    start = 0
    for i in range(nodes):
        extra = 1 if i < remainder else 0  # Distribute remainder across first few nodes
        end = start + chunk_size + extra
        node_uid_list.append(all_uids[start:end])
        if verbose:
            print(f"Node {i}: {start} - {end-1} UIDs assigned.")
        start = end

    # Split UIDs among GPUs within each node
    gpu_uid_list_per_node = []
    for i, node_uids in enumerate(node_uid_list):
        gpu_uid_list = []
        chunk_size_gpu = len(node_uids) // gpus
        remainder_gpu = len(node_uids) % gpus

        start = 0
        for j in range(gpus):
            extra_gpu = 1 if j < remainder_gpu else 0  # Distribute remainder across GPUs
            end = start + chunk_size_gpu + extra_gpu
            gpu_uid_list.append(node_uids[start:end])
            if verbose:
                print(f"Node {i} GPU {j}: {start} - {end-1} UIDs assigned.")
            start = end
        gpu_uid_list_per_node.append(gpu_uid_list)

    # Return the list for the specified node and GPU
    return gpu_uid_list_per_node


def get_gpu_memory_info():
    """
    Print total, used, and free memory for each GPU.
    """
    try:
        output = subprocess.check_output([
            'nvidia-smi',
            '--query-gpu=index,name,memory.total,memory.used,memory.free',
            '--format=csv,noheader,nounits'
        ], encoding='utf-8')
        
        print("Available GPU memory per device:")
        print("-------------------------------")
        for line in output.strip().split('\n'):
            index, name, total, used, free = [x.strip() for x in line.split(',')]
            print(f"GPU {index} ({name}):")
            print(f"  Total Memory: {total} MiB")
            print(f"  Used Memory : {used} MiB")
            print(f"  Free Memory : {free} MiB\n")
    except subprocess.CalledProcessError as e:
        print("Error running nvidia-smi:", e)

def show_gpu_with_free_memory(threshold):
    """
    Print indices of GPUs with free memory >= threshold.
    """
    try:
        output = subprocess.check_output([
            'nvidia-smi',
            '--query-gpu=index,memory.free',
            '--format=csv,noheader,nounits'
        ], encoding='utf-8')

        for line in output.strip().split('\n'):
            index, free = [x.strip() for x in line.split(',')]
            if int(free) >= threshold:
                print(f"GPU {index} has {free} MiB free")
    except subprocess.CalledProcessError as e:
        print("Error running nvidia-smi:", e)

def get_gpu_id_list_with_free_memory(threshold):
    """
    Return a list of GPU indices with free memory >= threshold.
    """
    gpu_ids = []
    try:
        output = subprocess.check_output([
            'nvidia-smi',
            '--query-gpu=index,memory.free',
            '--format=csv,noheader,nounits'
        ], encoding='utf-8')

        for line in output.strip().split('\n'):
            index, free = [x.strip() for x in line.split(',')]
            if int(free) >= threshold:
                gpu_ids.append(int(index))
    except subprocess.CalledProcessError as e:
        print("Error running nvidia-smi:", e)
    return gpu_ids


def foreach_instance(data_list,
                     func,
                     max_workers=None,
                     desc='Processing objects') -> pd.DataFrame:
    import os
    from concurrent.futures import ThreadPoolExecutor

    from tqdm import tqdm

    # processing objects
    records = []
    max_workers = max_workers or os.cpu_count()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor, \
            tqdm(total=len(data_list), desc=desc) as pbar:

            def worker(data):
                try:
                    record = func(data)
                    if record is not None:
                        records.append(record)
                    pbar.update()
                except Exception as e:
                    print(f"Error processing object {data}: {e}")
                    pbar.update()

            executor.map(worker, data_list)
            executor.shutdown(wait=True)
    except:
        print("Error happened during processing.")

    return records


def _valid_tos_path(path):
    """
    Check if the given path is a valid Terms of Service (TOS) file path.

    Args:
    path (str): The path to be checked.

    Returns:
    bool: True if the path is a valid TOS file path, False otherwise.
    """
    if not path.startswith("tos://"):
        raise ValueError(f"tos path should start with 'tos://'")
        
    if path.endswith("/"):
        raise ValueError(f"tos path should not end with '/'")
    return True

def _split_tospath(path):
    """
    Split the given TOS file path into its components.

    Args:
    path (str): The TOS file path to be split.

    Returns:
    tuple: A tuple containing the bucket name, prefix, and file name.
    """
    path = path.replace("tos://", "")
    path = path.split("/")
    bucket_name = path[0]
    prefix = "/".join(path[1:-1])
    file_name = path[-1]
    return bucket_name, prefix, file_name
    
    
def check_tos_file_exists(tos_filepath, config):
    """
    Check if the Terms of Service (TOS) file exists at the specified filepath.

    Args:
    tos_filepath (str): The filepath of the TOS file. Example: tos://bucket_name/prefix/file_name/
    config (dict): A dictionary containing configuration settings.

    Returns:
    bool: True if the file exists, False otherwise.

    Raises:
    ValueError: If the tos_filepath is empty or None.
    """
    _valid_tos_path(tos_filepath)
    bucket_name, prefix, file_name = _split_tospath(tos_filepath)
    client = tos.TosClientV2(config['ak'], config['sk'], config['endpoint'], config['region'])
    
    truncated = True
    continuation_token = ''
    while truncated:
        try:
            result = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=continuation_token, max_keys=1000)
        except tos.exceptions.TosServerError as e:
            print(f"Error listing objects: {e}")
            return False
        for item in result.contents:
            if item.key.endswith(file_name):
                return True
        truncated = result.is_truncated
        continuation_token = result.next_continuation_token
    return False
    # Check if the file exists
    
def list_all_files_under_tos_dir(tos_dir, config, save2txt = False, custom_save_path = None):
    """
    List all files under the given prefix in the specified bucket.

    Args:
    tos_dir (str): The directory path in the
    """
    output_list = []
    if not tos_dir.startswith("tos://"):
        raise ValueError(f"tos dir should start with 'tos://'")
    if not tos_dir.endswith("/"):
        raise ValueError(f"tos dir should end with '/'")
    bucket_name, prefix, _ = _split_tospath(tos_dir)
    prefix = f"{prefix}/"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        # 1. 列举根目录下文件和子目录
        is_truncated = True
        count = 0
        next_continuation_token = ''
        while is_truncated:
            count += 1
            print(f"{count * 1000} objects have been found!", end="\r")
            out = client.list_objects_type2(bucket_name, prefix=prefix, continuation_token=next_continuation_token)
            # print(out, out.__dict__)
            is_truncated = out.is_truncated
            next_continuation_token = out.next_continuation_token

            # contents中返回了根目录下的对象
            for content in out.contents:
                output_list.append(content.key)
        print()
        print("All files have been listed!")
        
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
        print('fail with server error, code: {}'.format(e.code))
        # request id 可定位具体问题，强烈建议日志中保存
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
        
    out = list(filter(lambda x: not x.endswith("/"), output_list))
    print(f"Total number of files: {len(out)}")
    if save2txt:
        if custom_save_path is None:
            save_path = "all_files.txt"
        else:
            save_path = custom_save_path
        write_list_to_txt(out, save_path)
    return out


def list_all_subdirs_under_prefix(tos_dir, config, save2txt = False, custom_save_path = None):
    """
    List all subdirectories under the given prefix in the specified bucket.

    Args:
    tos_dir (str): The directory path in the bucket. Example: tos://bucket_name/prefix/
    config (dict): A dictionary containing configuration settings.
    save2txt (bool, optional): Whether to save the subdirectories to a text file. Defaults to False.
    custom_save_path (str, optional): The custom path to save the text file. Defaults to None.

    Returns:
    list: A list of subdirectories under the given prefix.

    Raises:
    ValueError: If the tos_dir is empty or None.
    """
    if not tos_dir.startswith("tos://"):
        raise ValueError(f"tos dir should start with 'tos://'")
    if not tos_dir.endswith("/"):
        raise ValueError(f"tos dir should end with '/'")
    output_list = []
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        bucket_name, prefix, file_name = _split_tospath(tos_dir)
        prefix = f"{prefix}/"
        # 1. 列举根目录下文件和子目录
        is_truncated = True
        count = 0
        next_continuation_token = ''
        while is_truncated:
            count += 1
            print(f"{count * 1000} objects have been found!", end="\r")
            out = client.list_objects_type2(bucket_name, delimiter="/", prefix=prefix, continuation_token=next_continuation_token)
            # print(out, out.__dict__)
            is_truncated = out.is_truncated
            next_continuation_token = out.next_continuation_token

            for file_prefix in out.common_prefixes:
                output_list.append(file_prefix.prefix)
        print()
        print("All subdirs have been listed!")
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
        print('fail with server error, code: {}'.format(e.code))
        # request id 可定位具体问题，强烈建议日志中保存
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))
    print(f"Total number of subdirs: {len(output_list)}")
    
    if save2txt:
        if custom_save_path is None:
            save_path = "all_dirs.txt"
        else:
            save_path = custom_save_path
        write_list_to_txt(output_list, save_path)
    
    return output_list


def uid2pil_img(bucket_name, uid, viewIdx, img_format, config, specified_tos_img_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    PIL.Image: The image fetched from the TOS storage.

    Raises:
    ValueError: If the img does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_img_dir is None:
        if bucket in ["v1", "v3"]:
            tos_img_prefix = "rendering/cam72"
        else:
            tos_img_prefix = "data/rendering/cam72"
    else:
        if not specified_tos_img_dir.endswith("/"):
            raise ValueError(f"specified_tos_img_dir should end with '/'")
        if not specified_tos_img_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_img_dir should start with 'tos://'")
        bucket_name, tos_img_prefix, _ = _split_tospath(specified_tos_img_dir)


    object_key = f"{tos_img_prefix}/{uid}/View{viewIdx}_FinalColor.{img_format}"
    full_img_path = f"tos://{bucket_name}/{object_key}"
    # if not check_tos_file_exists(full_img_path, config):
    #     raise ValueError(f"Image does not exist in TOS storage: {full_img_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    if not data:  # Check if data is empty
        raise ValueError(f"Empty data fetched for UID: {uid}, Object Key: {object_key}")
    bytes_io = io.BytesIO(data)
    image = Image.open(bytes_io)
    return image


def uid2camera_info(bucket_name, uid, config, specified_tos_img_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    str : camera info

    Raises:
    ValueError: If the camerainfo txt does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_img_dir is None:
        if bucket in ["v1", "v3"]:
            tos_img_prefix = "rendering/cam72"
        else:
            tos_img_prefix = "data/rendering/cam72"
    else:
        if not specified_tos_img_dir.endswith("/"):
            raise ValueError(f"specified_tos_img_dir should end with '/'")
        if not specified_tos_img_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_img_dir should start with 'tos://'")
        bucket_name, tos_img_prefix, _ = _split_tospath(specified_tos_img_dir)
        
    object_key = f"{tos_img_prefix}/{uid}/camera_info.txt"
    full_txt_path = f"tos://{bucket_name}/{object_key}"
    full_txt_path = f"tos://{bucket_name}/{object_key}"
    # if not check_tos_file_exists(full_txt_path, config):
    #     raise ValueError(f"Camera info does not exist in TOS storage: {full_txt_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    if not data:  # Check if data is empty
        raise ValueError(f"Empty data fetched for UID: {uid}, Object Key: {object_key}")
    bytes_io = io.BytesIO(data)
    camera_info = bytes_io.read().decode('utf-8')
    return camera_info

def multi_thread_check_tos_file_exists(tos_filepaths, config):
    """
    Check if the Terms of Service (TOS) file exists at the specified filepath.

    Args:
    tos_filepaths (list): A list of TOS filepaths to be checked.
    config (dict): A dictionary containing configuration settings.

    Returns:
    dict: A dictionary containing the filepaths and their existence status.

    Raises:
    ValueError: If the tos_filepath is empty or None.
    """
    results = {}
    print(f"Checking {len(tos_filepaths)} files...")
    success_count = 0
    fail_count = 0 
    with tqdm(total=len(tos_filepaths)) as pbar:
        with ThreadPoolExecutor() as executor:
            future_to_path = {}
            for tos_filepath in tos_filepaths:
                future_to_path[executor.submit(check_tos_file_exists, tos_filepath, config)] = tos_filepath
                
            for future in as_completed(future_to_path):
                tos_filepath = future_to_path[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'{tos_filepath} generated an exception: {exc}')
                else:
                    if result:
                        success_count += 1
                    else:
                        fail_count += 1
                    results[tos_filepath] = result
                pbar.update(1)
                pbar.set_postfix_str(f"Exists: {success_count}, Missing: {fail_count}")
    return results

def read_tensor_from_tos(tos_path, config):
    if not tos_path.startswith("tos://"):
        raise ValueError("tos_path should start with 'tos://'")

    bucket_name, prefix, filename = _split_tospath(tos_path)
    object_key = f"{prefix}/{filename}" if prefix else filename

    try:
        client = tos.TosClientV2(
            config["ak"], config["sk"], config["endpoint"], config["region"]
        )
        response = client.get_object(bucket_name, object_key)
        buffer = io.BytesIO(response.read())
        # tensor = torch.load(buffer, map_location='cpu')  # change map_location if needed
        return buffer
    except Exception as e:
        print(f"Error reading tensor from TOS: {e}")
        return None
    
    
def read_tos_csv(tos_path, config):
    # need testing!
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_path should start with 'tos://'")
    
    if not tos_path.endswith(".csv"):
        raise ValueError(f"tos_path should end with '.csv'")
    
    # if not check_tos_file_exists(tos_path, config):
    #     raise ValueError(f"File does not exist in TOS storage: {tos_path}")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    object_key = f"{prefix}/{filename}" if prefix else filename
    
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        object_stream = client.get_object(bucket_name, object_key)
        data = object_stream.read()
        
        if not data:  # Check if data is empty
            raise ValueError(f"Empty data fetched for Object Key: {object_key}")

        bytes_io = io.BytesIO(data)
        df = pd.read_csv(bytes_io)  # Read CSV using pandas
        
        return df  # Return the dataframe
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


def read_tos_txt(tos_path, config):
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    
    if not tos_path.endswith(".txt"):
        raise ValueError(f"tos_save_path should end with '.txt'")
    
    # if not check_tos_file_exists(tos_path, config):
    #     raise ValueError(f"File does not exist in TOS storage: {tos_path}")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        object_stream = client.get_object(bucket_name, object_key)
        data = object_stream.read()
        if not data:  # Check if data is empty
            raise ValueError(f"Empty data fetched for UID: {uid}, Object Key: {object_key}")
        bytes_io = io.BytesIO(data)
        txt = bytes_io.read().decode('utf-8')
        return txt    
    except Exception as e:
        print(f"Error reading txt: {e}")


def read_tos_mesh(tos_path, config):
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    
    if not tos_path.endswith(".glb"):
        raise ValueError(f"tos_save_path should end with '.glb'")
    
    # if not check_tos_file_exists(tos_path, config):
    #     raise ValueError(f"Mesh does not exist in TOS storage: {tos_path}")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        object_stream = client.get_object(bucket_name, object_key)
        data = object_stream.read()
        bytes_io = io.BytesIO(data)
        # mesh = trimesh.load(bytes_io, file_type='glb', force='scene')
        return bytes_io
    except Exception as e:
        print(f"Error reading mesh: {e}")
        
        
def read_tos_json(tos_path, config):
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    
    if not tos_path.endswith(".json"):
        raise ValueError(f"tos_save_path should end with '.json'")
    
    # if not check_tos_file_exists(tos_path, config):
    #     raise ValueError(f"Json does not exist in TOS storage: {tos_path}")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
        
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        object_stream = client.get_object(bucket_name, object_key)
        data = object_stream.read()
        bytes_io = io.BytesIO(data)
        json_data = json.load(bytes_io)
        return json_data
    except Exception as e:
        print(f"Error reading json: {e}")
        
        
def read_tos_img(tos_path, config):
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    
    # if not tos_path.endswith(".jpg") and not tos_path.endswith(".png"):
    #     raise ValueError(f"tos_save_path should end with '.jpg' or '.png'")
    
    # if not check_tos_file_exists(tos_path, config):
    #     raise ValueError(f"Image does not exist in TOS storage: {tos_path}")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        object_stream = client.get_object(bucket_name, object_key)
        data = object_stream.read()
        bytes_io = io.BytesIO(data)
        image = Image.open(bytes_io)
        return image
    except Exception as e:
        print(f"Error reading image: {e}")
    

def uid2mesh(bucket_name, uid, file_type, config, specified_tos_glb_dir = None):
    """ 
    Fetch image from TOS storage based on UID.
    Args:
    bucket_name (str): The name of the bucket. Example: "[v1, v2, v3]"
    uid (str): The unique identifier of the image.
    viewIdx (int): The index of the view.
    config (dict): A dictionary containing configuration settings.
    
    Returns:
    PIL.Image: The image fetched from the TOS storage.

    Raises:
    ValueError: If the img does not exist in the TOS storage.
    
    """
    client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
    bucket = bucket_name.lower().replace("mm-data-general-model-", "")
    if not bucket in ["v1", "v2", "v3"]:
        raise ValueError(f"Invalid bucket name: {bucket_name}")
    bucket_name = f"mm-data-general-model-{bucket}"
    if specified_tos_glb_dir is None:
        if bucket in ["v1", "v3"]:
            tos_glb_prefix = "glb_models"
        else:
            tos_glb_prefix = "data/glb_models"
    else:
        if not specified_tos_glb_dir.endswith("/"):
            raise ValueError(f"specified_tos_glb_dir should end with '/'")
        if not specified_tos_glb_dir.startswith("tos://"):
            raise ValueError(f"specified_tos_glb_dir should start with 'tos://'")
        bucket_name, tos_glb_prefix, _ = _split_tospath(specified_tos_glb_dir)

    object_key = f"{tos_glb_prefix}/{uid}.{file_type}"
    full_glb_path = f"tos://{bucket_name}/{object_key}"
    # if not check_tos_file_exists(full_glb_path, config):
    #     raise ValueError(f"Mesh does not exist in TOS storage: {full_glb_path}")
    
    object_stream = client.get_object(bucket_name, object_key)
    data = object_stream.read()
    bytes_io = io.BytesIO(data)
    # mesh = trimesh.load(bytes_io, file_type='glb', force='scene')
    return bytes_io


def save_tensor(tensor_buffer, tos_save_path, config):
    # buffer = io.BytesIO()
    # torch.save(feature, buffer)
    tensor_buffer.seek(0)
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=tensor_buffer)
        # print(f"Tensor embedding for UID {uid} successfully uploaded to {self.bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading tensor embedding: {e}")


def save_dict2tos_json(data_dict, tos_save_path, config):
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"
    # Convert dictionary to JSON string
    json_data = json.dumps(data_dict)
    
    # Create a BytesIO buffer to hold the JSON content
    buffer = io.BytesIO()
    buffer.write(json_data.encode())  # Write the JSON string as bytes to the buffer
    
    # Seek to the beginning of the buffer before uploading
    buffer.seek(0)
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=buffer)
    except Exception as e:
        print(f"Error uploading json: {e}")


def save_pil_img2tos(image, tos_path, config, quality=85, optimize=False):
    if not tos_path.startswith("tos://"):
        raise ValueError(f"tos_path should start with 'tos://'")
    
    if not tos_path.endswith(".jpg") and not tos_path.endswith(".png"):
        raise ValueError(f"tos_path should end with '.jpg' or '.png'")
    
    bucket_name, prefix, filename = _split_tospath(tos_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"

    try:
        # Convert the PIL image to a byte stream
        img_byte_arr = io.BytesIO()
        if tos_path.endswith(".png"):
            image.save(img_byte_arr, format="PNG")
        elif tos_path.endswith(".jpg"):
            image.save(img_byte_arr, format="JPEG", quality=quality, optimize=optimize)
        else:
            raise ValueError(f"tos_path should end with '.jpg' or '.png'")
        img_byte_arr.seek(0)  # Reset the pointer to the start of the stream
        
        # Initialize the TOS client
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        
        # Upload the image to TOS
        client.put_object(bucket_name, object_key, content = img_byte_arr.read())
        # print(f"Image saved successfully to TOS: {tos_path}")
    
    except Exception as e:
        print(f"Error saving image to TOS: {e}")

def save_string(str_data, tos_save_path, config):
    if not tos_save_path.startswith("tos://"):
        raise ValueError(f"tos_save_path should start with 'tos://'")
    bucket_name, prefix, filename = _split_tospath(tos_save_path)
    if prefix == "":
        object_key = filename
    else:
        object_key = f"{prefix}/{filename}"

    # Use StringIO to hold the string data
    stream = io.StringIO()
    
    # Write the string data to the in-memory stream
    stream.write(str_data)
    
    # Get the string content of the stream (although it's already in memory)
    string_data = stream.getvalue()

    # Upload the string data as content to the cloud storage
    try:
        client = tos.TosClientV2(config["ak"], config["sk"], config["endpoint"], config["region"])
        client.put_object(bucket_name, object_key, content=string_data)
    except Exception as e:
        print(f"Error uploading str: {e}")
    stream.close()

def _set_tosutil_config(config):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")

    if not os.path.exists("~/.tosutilconfig"):
        print("tosutil has not been set!")
        config_set_command_str = f"{config['tosutil_path']} config \
                                    -i {config['ak']} \
                                    -k {config['sk']} \
                                    -e {config['endpoint']} \
                                    -re {config['region']}"
        config_result = subprocess.run(config_set_command_str, shell=True, capture_output=True, text=True)
        print(config_result)
        print("-----------------------------------------------")

def download_dir_from_tos(tos_dir, local_dir, config, jobs=96, chunk_jobs=96):
    transfer_command_str = f'{config["tosutil_path"]} cp \
                        -r -flat -u -p {jobs} -j {chunk_jobs} \
                        "{tos_dir}" "{local_dir}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error downloading {tos_dir} to {local_dir}: {result.stderr}")
    return result.returncode


def download_file_via_tosutil(tos_path, local_path, config, jobs=96, chunk_jobs=96, verbose=True):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    
    transfer_command_str = f'{config["tosutil_path"]} cp \
                            -u -p {jobs} -j {chunk_jobs} \
                            "{tos_path}" "{local_path}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)   
    if os.path.exists(local_path):
        return 0
    else:
        print(f"Error downloading {tos_path} to {local_path}: {result.stderr}")
        if verbose:
            print(result)
        return -1

def upload_dir_via_tosutil(local_dir, tos_dir, config, flat=False, jobs=96, chunk_jobs=96, verbose=True):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    if not os.path.exists(local_dir):
        raise ValueError(f"local_path does not exist: {local_dir}")
    if flat:
        transfer_command_str = f'{config["tosutil_path"]} cp \
                                -flat -r -u -p {jobs} -j {chunk_jobs} \
                                "{local_dir}" "{tos_dir}"'
    else:
        transfer_command_str = f'{config["tosutil_path"]} cp \
                                -r -u -p {jobs} -j {chunk_jobs} \
                                "{local_dir}" "{tos_dir}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error uploading {local_dir} to {tos_dir}: {result.stderr}")
        if verbose:
            print(result)
    return result.returncode


def upload_file2tos(local_path, tos_path, config, jobs=96, chunk_jobs=96):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    if not os.path.exists(local_path):
        raise ValueError(f"local_path does not exist: {local_path}")
    
    transfer_command_str = f'{config["tosutil_path"]} cp \
                            -u -p {jobs} -j {chunk_jobs} \
                            "{local_path}" "{tos_path}"'
    result = subprocess.run(transfer_command_str, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error uploading {local_path} to {tos_path}: {result.stderr}")
    return result.returncode


def download_file_from_tos2local(tos_parent_dir, uids, file_type, local_dir, config, jobs=96, chunk_jobs=96):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    _set_tosutil_config(config)
    tos_parent_dir = tos_parent_dir.strip("/")
    results = []
    with tqdm(total=len(uids)) as pbar:
        with ThreadPoolExecutor() as executor:
            future_to_path = {}
            for uid in uids:
                tos_path = f"{tos_parent_dir}/{uid}.{file_type}"
                save_path = f"{local_dir}/{uid}.{file_type}"
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                future_to_path[executor.submit(download_file_from_tos, tos_path, save_path, config, jobs=jobs, chunk_jobs=chunk_jobs)] = uid
            # future_to_path = {executor.submit(download_file_from_tos2local, bucket_name, tos_path): tos_path for tos_path in paths}
            for future in as_completed(future_to_path):
                uid = future_to_path[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'{uid} generated an exception: {exc}')
                else:
                    results.append((uid, result))
                pbar.update(1)

    fail_list = []
    for result in results:
        if result[1] != 0:
            fail_list.append(result[0])
    print(f"{len(fail_list)} download are unsuccessful!")
    if fail_list:
        write_list_to_txt(fail_list, "fail_download.txt")
    return results


def download_dirs_from_tos2local(tos_parent_dir, uids, local_dir, config, jobs=96, chunk_jobs=96):
    if not os.path.exists(config['tosutil_path']):
        raise ValueError(f"tosutil_path does not exist: {config['tosutil_path']}")
    _set_tosutil_config(config)
    tos_parent_dir = tos_parent_dir.strip("/")
    results = []
    with tqdm(total=len(uids)) as pbar:
        with ThreadPoolExecutor() as executor:
            future_to_path = {}
            for uid in uids:
                save_dir = f"{os.path.join(local_dir, uid)}/"
                tos_target_dir = f"{tos_parent_dir}/{uid}/"
                os.makedirs(local_dir, exist_ok=True)
                future_to_path[executor.submit(download_dir_from_tos, tos_target_dir, save_dir, config, jobs=jobs, chunk_jobs=chunk_jobs)] = uid           
            # future_to_path = {executor.submit(download_file_from_tos2local, bucket_name, tos_path): tos_path for tos_path in paths}
            for future in as_completed(future_to_path):
                uid = future_to_path[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print(f'{uid} generated an exception: {exc}')
                else:
                    results.append((uid, result))
                pbar.update(1)
                
    fail_list = []
    for result in results:
        if result[1] != 0:
            fail_list.append(result[0])
    print(f"{len(fail_list)} download are unsuccessful!")
    if fail_list:
        write_list_to_txt(fail_list, "fail_download.txt")
    return results
    
    

def save_dict_to_json(data: Dict, file_path: str):
    import json
    with open(file_path, 'w') as json_file:
        # Write the dictionary to the file as JSON
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Dict has been successfully saved to {file_path}")

def write_list_to_txt(uid_list: List, file_path: str, verbose: bool = False):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(uid_list))
    if verbose:
        print(f"List has been successfully saved to {file_path}")
    

    
    
# easy_tos

让数据流动变得简单！Make data flow!

```
pip install easy_tos==0.5 --index-url https://pypi.org/simple #清华等其他镜像源可能同步慢
```

这个库的开发是包含了大部分常用的 tos脚本操作，避免许多重复代码。以及让很多新入职的同事能够快速用起来我们的数据。

# 准备工作

准备 tosutil config

```
config = {
    "ak": "YOUR TOS ACESS KEY",
    "sk": "YOUR TOS SECRET KEY",
    "endpoint": "https://tos-cn-beijing.ivolces.com", 
    # 如果是火山引擎内网用 "https://tos-cn-beijing.ivolces.com",
    # 如果是本地网用 "https://tos-cn-beijing.volces.com",
    "region": "cn-beijing",
    "tosutil_path": "absolute path to tosutil"
}
```

## 场景一：tos 桶内，桶与桶之间，桶和本地之间的数据传输

```
# 传输文件夹
tosutil cp -r -u -j 96 -p 96 {tos_dir} {local_dir}
tosutil cp -r -u -j 96 -p 96 {local_dir} {tos_dir}
tosutil cp -r -u -j 96 -p 96 {tos_dir} {tos_dir}

# -r : 批量传输文件夹内容
# -u : 表示增量传输，中间中断，下次跑同样命令会在之前的结果上继续传输，而不是从头开始。但是会要先对比一下两方文件，要耗时一段时间
# -j : jobs 并发数 本地一般设置在 8～32，服务器上在 96～192
# -p : 分块的每块并发数 本地一般设置在 8～32，服务器上在 96～192
# example
tosutil cp -r -u -j 96 -p 96 /Users/jiaqiwu/Desktop/Project tos://mm-jiaqi-test/Code
# 则会把本地 Project 文件夹传输到桶 mm-jiaqi-test 的 Code 文件夹下。形成Code/Project/

# python 上传和下载文件夹
upload_dir(local_dir, tos_dir, config, jobs=96, chunk_jobs=96)
download_dir(tos_dir, local_dir, config）注：不包含 tos 父文件夹本省


# 传输文件（把 -r 去掉）
tosutil cp -u -j 96 -p 96 {tos_path} {local_dir}/ #结果：{local_dir}/tos_file
tosutil cp -u -j 96 -p 96 {local_path} {tos_dir}/ #结果：{tos_dir}/local_file
tosutil cp -u -j 96 -p 96 {tos_path} {tos_dir}/   #结果：{local_dir}/tos_file

# 注意！！！目标路径一定是以/结尾的文件夹路径。不然就会把该文件传输到 target_dir的父目录下，名字为target_dir

# python 
upload_file(local_path, tos_path, config, jobs=96, chunk_jobs=96)
download_file(tos_path, local_path, config)

```

## 场景二：得到 tos 某个文件夹下的所有文件路径或者子文件夹路径

```
from easy_tos.core import *

# 得到桶 mm-data-general-model-v1 下面 rendering/nvdiffrast_render_v1_diffuse/ 的所有子文件夹。并把结果存到指定的 txt 路径。
tos_dir = "tos://mm-data-general-model-v1/rendering/nvdiffrast_render_v1_diffuse/"
res = list_all_subdirs_under_prefix(tos_dir, config, save2txt=True, custom_save_path="v1_diffuse_rendering.txt")

# 得到桶 mm-data-general-model-v1 下面 glb_models/ 所有的文件路径。 并把结果存到指定的 txt 路径。
tos_dir = "tos://mm-data-general-model-v1/glb_models/"
res = list_all_files_under_tos_dir(tos_dir, config, save2txt=True, custom_save_path="v1_glbs.txt")


```

## 场景三：tos上某个文件路径是否存在

```
from easy_tos.core import *
tos_path = "tos://mm-data-general-model-v1/glb_models/000-steel-stairs-fire-escapes-100465bd4888438aae77e058ef071940.glb"
print(check_tos_file_exists(tos_filepath=tos_path, config=config))
# return True if exists
# return False if not 
```

## 场景四：下载tos文件夹子集

```
# 有时候我们不想下载整个文件夹，只想要这个文件夹下的一部分文件或文件夹，我们有我们要的文件的信息，通常是 uid

from easy_tos.core import *
# 多线程下载 tos 目标文件夹下的 部分子文件
uids = [uid.strip() for uid in open("/home/jiaqi/Data_Engine/v1_all_uid.txt").readlines()]
tos_parent_dir = "tos://mm-data-general-model-v1/glb_models/"
file_type = "glb"
local_dir = "/home/jiaqi/Data_Engine/v1_glb"
download_file_from_tos2local(tos_parent_dir, uids, file_type, local_dir, config, jobs=96, chunk_jobs=96)


# 多线程下载 tos 目标文件夹下的 部分子文件夹
uids = [uid.strip() for uid in open("/home/jiaqi/Data_Engine/v1_all_uid.txt").readlines()]
tos_parent_dir = "tos://mm-data-general-model-v1/rendering/"
local_dir = "/home/jiaqi/Data_Engine/v1_glb"
download_dirs_from_tos2local(tos_parent_dir, uids, local_dir, config, jobs=96, chunk_jobs=96)
```

## 场景五：流式下载和上传

```
## 流式下载
from easy_tos.core import *
# 根据桶 和 uid 得到 mesh
bucket_name = "v1"
uid = "000-steel-stairs-fire-escapes-100465bd4888438aae77e058ef071940"
filetype = "glb"
bytes_io = uid2mesh(bucket_name, uid, file_type)
mesh = trimesh.load(bytes_io, file_type='glb', force='scene')
或者
read_tos_mesh(tos_path, config)

# 根据桶，uid，viewIdx 得到对应渲染图的 pillow image
bucket_name = "v1"
uid = "000-steel-stairs-fire-escapes-100465bd4888438aae77e058ef071940"
viewIdx = "0"
img_format = "png"
uid2pil_img(bucket_name, uid, viewIdx, img_format, config)
或者
read_tos_img(tos_path, config)

# 读tos json
read_tos_json(tos_path, config)


# 根据桶，uid，得到对应渲染的 camera_info
bucket_name = "v1"
uid = "000-steel-stairs-fire-escapes-100465bd4888438aae77e058ef071940"
uid2camera_info(bucket_name, uid, config)
# 或者
read_tos_txt(tos_path, config)


## 流式上传
# 保存 tensor 至 tos
feature = torch.rand(100, 100)
buffer = io.BytesIO()
tos_save_path = "tos://mm-jiaqi-test/test.pt"
torch.save(feature, buffer)
print("uploading tensor")
save_tensor(buffer, tos_save_path, config=config)

# 保存 dict 至 tos，以 json 格式存储
toy_dict = {"test": 1}
tos_save_path = "tos://mm-jiaqi-test/test.pt"
save_dict_to_tos_json(toy_dict, tos_save_path)

# 保存 str 至 tos， 以 txt 格式存储
toy_str = "test"
tos_save_path = "tos://mm-jiaqi-test/test.txt"
save_string(toy_str, tos_save_path)



```

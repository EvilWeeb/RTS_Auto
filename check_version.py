import requests
import zipfile
import io
import os
import shutil

# GitHub 版本号地址（raw 文件）
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/EvilWeeb/RTS_Auto/refs/heads/main/VERSION"

# GitHub 项目 ZIP 包下载地址（main 分支）
REMOTE_ZIP_URL = "https://github.com/EvilWeeb/RTS_Auto/archive/refs/heads/main.zip"

# GitHub 代理
GITHUB_PROXY = {
    "http": "http://127.0.0.1:10808",
    "https": "http://127.0.0.1:10808"
}

LOCAL_VERSION_FILE = "VERSION"

def read_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️ 无法读取本地版本号：{e}")
        return None

def read_remote_version():
    try:
        print(f"🌐 正在尝试获取远程版本：{REMOTE_VERSION_URL}")
        r = requests.get(REMOTE_VERSION_URL, timeout=5, proxies=GITHUB_PROXY)
        if r.status_code == 200:
            version = r.text.strip()
            print(f"✅ 获取成功：{version}")
            return version
        else:
            print(f"⚠️ 状态码 {r.status_code}")
    except Exception as e:
        print(f"❌ 获取失败：{e}")
    return None

def copy_contents(src, dst, skip_files=None):
    if skip_files is None:
        skip_files = []
    for item in os.listdir(src):
        if item in skip_files:
            continue
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print(f"✅ 已将新版本内容覆盖到当前目录")

def download_and_extract_zip(zip_url, extract_to="__temp_download__"):
    try:
        print(f"⬇️ 正在下载 ZIP 包：{zip_url}")
        r = requests.get(zip_url, stream=True, proxies=GITHUB_PROXY, timeout=10)
        if r.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"✅ 下载完成，解压至：{extract_to}")
            return True
    except Exception as e:
        print(f"❌ 下载失败：{e}")
    return False

def main():
    local = read_local_version()
    remote = read_remote_version()

    if not local:
        print("⚠️ 无法读取本地版本号")
        return
    if not remote:
        print("⚠️ 无法获取远程版本号")
        return

    if local == remote:
        print(f"✅ 当前版本已是最新（{local}）")
    else:
        print(f"🔔 发现新版本：{remote}（当前为 {local}）")
        answer = input("是否立即下载并替换当前项目？(y/n)：").strip().lower()
        if answer == "y":
            temp_dir = "__temp_download__"
            success = download_and_extract_zip(REMOTE_ZIP_URL, extract_to=temp_dir)
            if success:
                subfolders = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
                if subfolders:
                    source_path = os.path.join(temp_dir, subfolders[0])
                    copy_contents(source_path, ".", skip_files=["check_version.py"])
                    with open(LOCAL_VERSION_FILE, "w", encoding="utf-8") as f:
                        f.write(remote)
                    print(f"📌 VERSION 文件已更新为：{remote}")
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()

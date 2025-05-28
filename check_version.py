import requests

REMOTE_VERSION_URL = "https://gitee.com/Helesta/RTS_Auto/raw/main/VERSION.txt"
LOCAL_VERSION_FILE = "VERSION.txt"

def read_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    except:
        return None

def read_remote_version():
    try:
        r = requests.get(REMOTE_VERSION_URL, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    return None

def main():
    local = read_local_version()
    remote = read_remote_version()

    if not local or not remote:
        print("⚠️ 无法读取版本信息")
        return

    if local == remote:
        print(f"✅ 当前为最新版：{local}")
    else:
        print(f"🔔 检测到新版本：{remote}（当前为 {local}）")
        print("👉 请前往项目主页获取最新版本")

if __name__ == "__main__":
    main()

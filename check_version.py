# check_version.py
import subprocess
import os

def is_git_repo():
    return os.path.exists(".git")

def get_remote_url():
    try:
        return subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    except:
        return None

def get_remote_commit():
    try:
        output = subprocess.check_output(["git", "ls-remote", "origin", "HEAD"]).decode().strip()
        return output.split()[0][:7]
    except:
        return None

def get_local_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    except:
        return "unknown"

def pull_updates():
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        return "updated"
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 拉取失败：{e}")

def check_for_update(interactive=True):
    if not is_git_repo():
        print("⚠️ 当前目录不是 Git 仓库，跳过版本检查")
        return

    remote_url = get_remote_url()
    local_commit = get_local_commit()
    remote_commit = get_remote_commit()

    print(f"🧾 当前版本：{local_commit}")
    print(f"🌐 远程版本：{remote_commit or '无法获取'}")
    if remote_url:
        print(f"🔗 仓库地址：{remote_url}")

    if not remote_commit:
        print("⚠️ 无法获取远程版本，可能网络不通")
        return

    if local_commit != remote_commit:
        print("🔔 检测到新版本")
        if interactive:
            choice = input("是否拉取更新？(y/n)：").strip().lower()
            if choice == "y":
                pull_updates()
        else:
            print("📌 请使用 git pull 更新")
    else:
        print("✅ 当前版本已是最新")

# ✅ 支持独立运行
if __name__ == "__main__":
    check_for_update(interactive=True)

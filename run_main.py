# run_main.py
import os, sys, time
import pandas as pd
import importlib
from playwright.sync_api import sync_playwright
from logger import Logger
from proxy_page import ProxyPage
from task_registry import TASKS
from check_version import check_for_update
from datetime import datetime

check_for_update()  # 更新检查

def get_today_cookie_path(task_key):
    date_str = datetime.now().strftime("%Y%m%d")
    os.makedirs("cookies", exist_ok=True)
    return os.path.join("cookies", f"{task_key}_{date_str}.json")

def choose_import_file():
    files = [f for f in os.listdir("import") if f.endswith(".xlsx")]
    if not files:
        print("❌ import 文件夹中没有 .xlsx 文件")
        sys.exit(1)

    print("\n\033[1;35m📂 可用配置文件：\033[0m")
    print("─────────────────────────────")
    for i, f in enumerate(files, 1):
        print(f" {i}. {f}")
    print("─────────────────────────────")
    idx = input("\n📄 请选择文件编号：").strip()
    try:
        path = os.path.join("import", files[int(idx) - 1])
        print(f"\n✅ 你选择的文件是：\033[1m{files[int(idx) - 1]}\033[0m\n")
        return path
    except:
        print("❌ 选择无效")
        sys.exit(1)

def save_result_excel(logger,input_path):
    # input_path = f"import/{logger.task_key}.xlsx"
    os.makedirs("result", exist_ok=True)

    output_path = os.path.join(
        "result",
        f"{logger.task_key}_result_{logger.timestamp}.xlsx"
    )

    if not os.path.exists(input_path):
        print("❌ 原始配置文件不存在，无法生成结果文件")
        return

    df = pd.read_excel(input_path)
    df["运行结果"] = df["store_code"].astype(str).map(logger.result_map).fillna("未执行")
    df.to_excel(output_path, index=False)
    print(f"✅ 执行结果文件已保存：{output_path}")

def choose_task():
    print("\n\033[1;36m📋 可选任务列表：\033[0m")
    print("─────────────────────────────")
    for i, (key, meta) in enumerate(TASKS.items(), 1):
        print(f" {i}. {meta['name']}   ({key})")
    print("─────────────────────────────")
    idx = input("\n🔢 请输入任务编号：").strip()
    try:
        key = list(TASKS.keys())[int(idx) - 1]
        print(f"\n✅ 你选择的是：\033[1m{TASKS[key]['name']}\033[0m\n")
        return key
    except:
        print("❌ 选择无效")
        sys.exit(1)


def read_store_list(task_key, import_path):
    config = TASKS[task_key]
    if not os.path.exists(import_path):
        print(f"❌ 找不到文件：{import_path}")
        sys.exit(1)

    df = pd.read_excel(import_path)
    required = config.get("required_columns", [])
    actual = list(df.columns)

    if actual != required:
        print("❌ 配置文件列不符合要求")
        print(f"  👉 实际列：{actual}")
        print(f"  👉 要求列：{required}")
        sys.exit(1)

    return ["__init__"] + df["store_code"].dropna().astype(str).tolist()


def load_task(task_key):
    mod = importlib.import_module(f"tasks.{task_key}")
    return getattr(mod, task_key)

def process_store_codes(store_codes, task_runner, task_key,import_path):
    logger = Logger(task_key)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=500)
        cookie_path = get_today_cookie_path(task_key)
        if os.path.exists(cookie_path):
            context = browser.new_context(storage_state=cookie_path)
            print(f"✅ 已自动登录：{cookie_path}")
        else:
            context = browser.new_context()
            page = context.new_page()
            page.goto(TASKS[task_key]["url"])
            input("🟡 请手动登录后按回车继续...")
            context.storage_state(path=cookie_path)
            print(f"✅ 已保存 cookie：{cookie_path}")

        for code in store_codes:
            if code != "__init__":
                print(f"\n📍 正在处理门店: {code}")
            try:
                proxy = ProxyPage(page, logger, code)
                task_runner(proxy, code)
            except Exception as e:
                if code != "__init__":
                    logger.log_failure(code, "任务函数异常", e)

        logger.save()
        save_result_excel(logger,import_path)
        context.close()
        browser.close()

if __name__ == "__main__":
    task_key = choose_task()
    import_path = choose_import_file()
    task_func = load_task(task_key)
    stores = read_store_list(task_key, import_path)
    process_store_codes(stores, task_func, task_key,import_path)
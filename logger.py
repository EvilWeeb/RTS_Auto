import datetime, csv, os
from collections import defaultdict

class Logger:
    def __init__(self, task_key):
        self.task_key = task_key  # ✅ 保存任务名
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # ✅ 保存时间戳
        self.run_dir = os.path.join("logs", f"{task_key}_{self.timestamp}")
        self.screenshot_dir = os.path.join(self.run_dir, "screenshots")
        os.makedirs(self.run_dir, exist_ok=True)
        self.logs = []
        self.result_map = defaultdict(str)  # ✅ 存每个门店的运行结果

    def log(self, store_code, status, message, exception=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append({
            "time": timestamp,
            "store": store_code,
            "status": status,
            "message": message,
            "exception": str(exception) if exception else ""
        })

    def log_success(self, store_code, message):
        self.log(store_code, "SUCCESS", message)
        self.result_map[store_code] = "成功"

    def log_failure(self, store_code, message, exception=None):
        self.log(store_code, "FAILURE", message, exception)
        msg = str(exception) if exception else "失败"
        self.result_map[store_code] = f"失败：{msg}"

    def save(self):
        path = os.path.join(self.run_dir, "automation_log.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["time", "store", "status", "message", "exception"])
            writer.writeheader()
            writer.writerows(self.logs)
        print(f"\n📄 日志已保存：{path}")

    def get_screenshot_path(self, store_code, action):
        os.makedirs(self.screenshot_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.screenshot_dir, f"{store_code}_{action}_{timestamp}.png")

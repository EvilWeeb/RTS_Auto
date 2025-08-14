# 自动化任务执行系统

本项目用于自动化执行配置任务，基于 [Playwright](https://playwright.dev/python/) 实现网页自动化，支持任务选择、运行日志记录、失败截图、结果导出等功能。

---

## 🧩 项目结构

```
.
├── import/              # 存放 Excel 配置文件 (.xlsx)
├── logs/                # 自动生成日志与截图
├── result/              # 自动导出的任务执行结果
├── tasks/               # 各个任务模块，命名为 task_key.py
├── run_main.py          # 主程序入口
├── logger.py            # 日志记录模块
├── proxy_page.py        # 增强页面操作类，支持日志 + 截图
├── task_registry.py     # 注册所有支持的任务
├── mcd_cookies.json     # 登录态 Cookie（自动保存）
```

---

## 🚀 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

> 建议使用 Python 3.10+，并将 pip 源切换为清华源以加快安装速度。

### 2. 运行主程序

```bash
python run_main.py
```

你将被提示：

* 选择一个任务类型（如 `np_transform`）
* 选择一个 Excel 文件（存放于 `import/`，并包含 `store_code` 列）

### 3. 登录验证

首次运行时会要求你在浏览器手动登录 BOSS 系统。登录完成后自动保存 cookie，以便下次复用。

---

## 📄 Excel 配置要求

放入 `import/` 文件夹

| store\_code |
| ----------- |
| 123456      |
| 234567      |

---

## 📊 运行结果与日志

* 所有运行日志保存在 `logs/` 目录中，包含：

  * 任务执行明细 CSV（含时间、状态、异常信息）
  * 每个失败步骤截图
* 执行完成后会导出一个 Excel 文件到 `result/`，包含每个门店的运行结果。

---

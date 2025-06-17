def pull_history_acc(page, row:dict):
    store_code = str(row["store_code"])

    if store_code == "__init__":
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅配置发布管理").click()
        return

    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_placeholder("请输入餐厅号/餐厅名").fill(store_code)
    page.get_by_role("button", name="查询", exact=True).click()
    # page.locator("span.anticon.font-icon[role='img']").hover()
    page.locator(f'tr:has(td:text-is("{store_code}")) span.anticon.font-icon[role="img"]').hover()
    page.wait_for_selector("text=账号管理", timeout=3000)
    page.get_by_text("账号管理").click()
    page.get_by_role("button", name="拉取历史账号").click()



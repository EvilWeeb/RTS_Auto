def pull_history_acc(page, row:dict):
    
    if row.get("__init__"):
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅配置发布管理").click()
        return
    
    store_code = str(row["store_code"])

    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_placeholder("请输入餐厅号/餐厅名").fill(store_code)
    page.get_by_role("button", name="查询", exact=True).click()
    page.locator(f'//tr[td[normalize-space(text())="{store_code}"]]//span[@class="anticon font-icon" and @role="img"]').hover()
    # 查找 store_code 在第几行（从 2 开始，td[2] 是编号列）
    for i in range(2, 52):
        if page.locator(f'xpath=//*[@id="container"]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[{i}]/td[2]').inner_text() == store_code:
            index = i - 2
            break
    # 构造 XPath 点击账号管理
    page.wait_for_selector(f'xpath=//*[@id="root-web-boss"]/div[{index + 7}]/div/div/ul/li[4]/span/a[text()="账号管理"]', timeout=3000)
    page.locator(f'xpath=//*[@id="root-web-boss"]/div[{index + 7}]/div/div/ul/li[4]/span/a[text()="账号管理"]').click()
    page.get_by_role("button", name="拉取历史账号").click()



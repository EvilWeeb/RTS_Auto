def set_DBM_Merchantid(page, row:dict):
    
    if row.get("__init__"):
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅配置发布管理").click()
        return
    
    uscode = str(row["uscode"])
    Merchantid = str(row["银联商户号"])
    dbmip = str(row["DMB IP地址"])

    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_placeholder("请输入餐厅号/餐厅名").fill(uscode)
    page.get_by_role("button", name="查询", exact=True).click()
    page.locator(f'//tr[td[normalize-space(text())="{uscode}"]]//span[@class="anticon font-icon" and @role="img"]').hover()
    # 查找 store_code 在第几行（从 2 开始，td[2] 是编号列）
    for i in range(2, 52):
        if page.locator(f'xpath=//*[@id="container"]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[{i}]/td[2]').inner_text() == uscode:
            index = i - 2
            break
    # 构造 XPath 点击账号管理
    page.wait_for_selector(f'xpath=//*[@id="root-web-boss"]/div[{index + 7}]/div/div/ul/li[5]/span/a', timeout=3000)
    page.locator(f'xpath=//*[@id="root-web-boss"]/div[{index + 7}]/div/div/ul/li[5]/span/a').click()
                        #  //*[@id="root-web-boss"]/div[8]/div/div/ul/li[5]/span/a
    page.locator("#list_0_unionPayDealerCode").fill(Merchantid)
    if dbmip != "nan":  # 只有不是 NaN 时才执行填充
        page.locator("#list_0_dmbDeviceIp").fill(dbmip)
    page.get_by_role("button", name="保存").click()
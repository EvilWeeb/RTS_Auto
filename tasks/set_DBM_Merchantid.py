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
    page.locator(f'tr:has(td:text-is("{uscode}")) span.anticon.font-icon[role="img"]').hover()
    page.wait_for_selector("text=DMB及商户号设置", timeout=3000)
    page.get_by_text("DMB及商户号设置").last.click()
    page.locator("#list_0_unionPayDealerCode").fill(Merchantid)
    if dbmip != "nan":  # 只有不是 NaN 时才执行填充
        page.locator("#list_0_dmbDeviceIp").fill(dbmip)
    page.get_by_role("button", name="保存").click()
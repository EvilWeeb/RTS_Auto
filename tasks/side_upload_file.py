def side_upload_file(page, row:dict):

    if row.get("__init__"):
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅配置发布管理").click()
        return
    
    store_code = str(row["store_code"])

    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_placeholder("请输入餐厅号/餐厅名").fill(store_code)
    page.get_by_role("button", name="查询", exact=True).click()
    page.locator(
    f"//tr[contains(@class,'sct-table-row')]"
    f"[td[normalize-space(text())='{store_code}']]"
    "//a[normalize-space(text())='KVS设置']").click()

    section = page.locator(":text-is('MFY SIDE1(生产)')").locator("xpath=ancestor::div[contains(@class,'module-part')]")
    if section.locator("a.close", has_text="清除").count() > 0:
        section.locator("a.close", has_text="清除").click()

    file_input = section.locator("input[type=file]")
    file_input.set_input_files("uploadfile/产区+20.mp3")
    page.get_by_role("button", name="保存").click()
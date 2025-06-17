def NP_WK_tag(page, row:dict):
    store_code = str(row["store_code"])

    if store_code == "__init__":
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅配置发布管理").click()
        return
    
    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_role("button", name="关联餐厅标签").click()
    page.get_by_role("textbox", name="请输入餐厅号/餐厅名").fill(store_code)
    page.get_by_role("button", name="查询").click()
    # page.get_by_role("checkbox", name="Select all").check()
    page.locator(f'tr[data-row-key="{store_code}"] input[type="checkbox"]').check()
    page.get_by_role("button", name="批量配置").click()
    page.locator(".sct-modal-body > .sct-form > div > div > div > .sct-form-item > .sct-row > div:nth-child(2) > .sct-form-item-control-input > .sct-form-item-control-input-content > .sct-select > .sct-select-selector > .sct-select-selection-overflow").click()
    page.locator("div.sct-select-item-option-content", has_text="NP老店切换到WK").click()
    page.locator(".sct-modal-body > .sct-form > div > div > div > .sct-form-item > .sct-row > div:nth-child(2) > .sct-form-item-control-input > .sct-form-item-control-input-content > .sct-select > .sct-select-selector > .sct-select-selection-overflow").click()
    page.get_by_role("button", name="保存").click()
    page.wait_for_selector("text=保存成功！", timeout=3000)
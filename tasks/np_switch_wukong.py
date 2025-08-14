def np_switch_wukong(page, row:dict):
    
    # # 正式环境
    # if row.get("__init__"):
    #     page.get_by_text("门店中心").click()
    #     page.get_by_text("基础信息配置").click()
    #     page.get_by_text("母店管理").click()
    #     return

    # UAT环境
    if row.get("__init__"):
        page.get_by_text("门店中心").click()
        page.get_by_text("餐厅管理").click()
        page.get_by_text("线上点餐配置").click()
        page.get_by_text("餐厅POS配置").click()
        return
    
    store_code = str(row["store_code"])

    page.get_by_role("menuitem", name="餐厅列表").click()
    page.get_by_placeholder("请输入餐厅号/餐厅名").fill(store_code)
    page.get_by_role("button", name="查询", exact=True).click()
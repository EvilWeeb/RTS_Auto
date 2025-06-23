def sunflowerGrayscale(page, row:dict):

    uscode = str(row["uscode"])
    uscode_list = uscode.split(",")
    input("🟡 请等待灰度餐厅列表刷新后按回车继续...")
    # 在任务函数中执行
    buttons = page.locator('svg.aurum-icon-delete-red-circle-color-fill')
    count = buttons.count()

    for i in reversed(range(count)):
        try:
            buttons.nth(i).click()
            print(f"✅ 删除 {i+1} 家餐厅成功")
        except Exception as e:
            print(f"❌ 第 {i+1} 家餐厅删除失败：{e}")

    for uscode in uscode_list:
        uscode = uscode.strip()
        page.get_by_placeholder("请输入餐厅code").fill(uscode)
        page.locator('button.pfe-input-search-button').click()
        # 找到包含该餐厅号的最外层 div（class=pfe-row）
        container = page.locator(f'div.pfe-row:has-text("餐厅号： {uscode}")')
        # 从 container 中找 checkbox
        checkbox = container.locator('input.pfe-checkbox-input[type="checkbox"]')
        checkbox.first.click()
        button = container.locator('button.pfe-btn')
        button.click()
        print(f"✅ 添加 {uscode} 餐厅成功")

    input("\n🛑 敏感操作提醒：所有门店操作已完成，请核对后手动点击【保存】按钮提交更改。保存后回车关闭软件。")
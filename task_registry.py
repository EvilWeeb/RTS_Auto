TASKS = {
    "pull_history_acc": {
        "name": "COC账号管理配置",
        "required_columns": ["store_code"],
        "url": "https://boss.uat.mcdonalds.cn/"
    },
        "NP_WK_tag": {
        "name": "关联门店标签",
        "required_columns": ["store_code"],
        "url": "https://boss.uat.mcdonalds.cn/"
    },
        "set_DBM_Merchantid": {
        "name": "DMB及商户号配置",
        "required_columns": ["uscode", "银联商户号","DMB IP地址"],
        "url": "https://boss.uat.mcdonalds.cn/"
    },
        "sunflowerGrayscale": {
        "name": "向日葵应用灰度配置",
        "required_columns": ["uscode"],
        "url": "https://boss.mcdonalds.cn/cms/sunflowerGrayscale/grayReleasePublic"
    },
}

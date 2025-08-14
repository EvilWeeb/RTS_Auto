TASKS = {
    "pull_history_acc": {
        "name": "COC账号管理配置",
        "required_columns": ["store_code"],
        "url": "https://boss.mcdonalds.cn/"
    },
        "NP_WK_tag": {
        "name": "关联门店标签",
        "required_columns": ["store_code"],
        "url": "https://boss.mcdonalds.cn/"
    },
        "set_DBM_Merchantid": {
        "name": "DMB及商户号配置",
        "required_columns": ["uscode", "银联商户号","DMB IP地址"],
        "url": "https://boss.mcdonalds.cn/"
    },
        "sunflowerGrayscale": {
        "name": "向日葵应用灰度配置",
        "required_columns": ["uscode"],
        "url": "https://boss.mcdonalds.cn/cms/sunflowerGrayscale/grayReleasePublic"
    },
    #     "np_switch_wukong": {
    #     "name": "NP切换WuKong",
    #     "required_columns": ["store_code"],
    #     "url": "https://boss.uat.mcdonalds.cn/"
    # },
        "side_upload_file": {
        "name": "产区上传声音文件",
        "required_columns": ["store_code"],
        "url": "https://boss.uat.mcdonalds.cn/"
    },
}

from typing import Final
from instaui import ui
import instaui_tdesign as td

url: Final = "/cell-slot"


def index():
    province_data, city_data = build_df()

    # ui
    table = td.table(
        province_data,
        columns=[
            {"colKey": "省份"},
            {"colKey": "人口", "align": "right"},
        ],
    )

    with table.add_cell_slot("省份") as province:
        current_province = province.param("row")["省份"]

        with td.popup(
            overlay_inner_style={"padding": 0},
            overlay_style={"min-width": "120px", "width": "30vw"},
        ) as popup:
            with ui.box(width="100%"):
                ui.text(current_province)

        with popup.add_slot("content"):
            detail_table(city_data, current_province)


def build_df():
    import pandas as pd
    import numpy as np

    # 设置随机种子以便结果可重现（可选）
    np.random.seed(42)

    # 定义省份和对应的城市
    data = {
        "广东省": ["广州市", "深圳市", "东莞市", "佛山市", "珠海市"],
        "四川省": ["成都市", "绵阳市", "宜宾市"],
        "浙江省": ["杭州市", "宁波市", "温州市", "嘉兴市"],
    }

    # 构建DataFrame数据
    rows = []
    for province, cities in data.items():
        for city in cities:
            population = np.random.randint(
                500_000, 20_000_000
            )  # 人口在50万到2000万之间随机
            rows.append([province, city, population])

    # 创建DataFrame
    df = pd.DataFrame(rows, columns=["省份", "城市", "人口"])

    province_df = df.groupby("省份").agg({"人口": sum}).reset_index()
    city_df = df
    return province_df.to_dict("records"), city_df.to_dict("records")


def detail_table(city_data: list, province: str):
    city_table_data = ui.js_computed(
        inputs=[province, city_data],
        code="""(provinceName, cityData) => {
            const filtered = cityData.filter(d => d["省份"] === provinceName);
            return {
                data: filtered,
                columns: [
                    {colKey: "城市", title: "城市"},
                    {colKey: "人口", title: "人口", align: "right", width: 100}
                ]
            };
        }""",
    )

    # ui
    with td.card(title=province):
        td.table(data=city_table_data["data"], columns=city_table_data["columns"])

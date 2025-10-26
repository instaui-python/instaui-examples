import polars as pl
from instaui import ui
from instaui_tdesign import td
from instaui_echarts import graphics as gh, echarts
from shared.example_extractor import use_example_infos
from utils import I18nState


m_tdesign_import = "from instaui_tdesign import td"
m_polars_import = "import polars as pl"
m_echarts_import = "from instaui_echarts import graphics as gh, echarts"

N_ = I18nState.get()
example, infos, _ = use_example_infos(require_imports=[m_echarts_import])


@example(N_("折线图"), "line chart")
def line_base():
    options = gh.option(
        gh.data(
            [
                {"week": "Mon", "temperature": 11},
                {"week": "Tue", "temperature": 12},
                {"week": "Wed", "temperature": 13},
                {"week": "Thu", "temperature": 10},
                {"week": "Fri", "temperature": 10},
                {"week": "Sat", "temperature": 13},
                {"week": "Sun", "temperature": 14},
            ]
        ),
        gh.line(x="week", y="temperature"),
    )

    echarts(options)


@example(N_("折线图（按颜色分组）"), "line chart by color")
def line_by_color():
    options = gh.option(
        gh.data(
            [
                {"x": "foo", "y": 11, "type": "t1"},
                {"x": "baz", "y": 12, "type": "t1"},
                {"x": "foo", "y": 13, "type": "t2"},
                {"x": "baz", "y": 10, "type": "t2"},
            ]
        ),
        # x field default 'x', y field default 'y'
        gh.line(color="type"),
    )

    echarts(options)


@example(N_("折线图（按分面分组）"), "line chart by facet")
def line_by_facet():
    options = gh.option(
        gh.data(
            [
                {"x": "foo", "y": 11, "type": "t1"},
                {"x": "baz", "y": 12, "type": "t1"},
                {"x": "foo", "y": 13, "type": "t2"},
                {"x": "baz", "y": 10, "type": "t2"},
            ]
        ),
        gh.line(facet=gh.facet(row="type")),
    )

    echarts(options)


@example(N_("柱状图"), "bar chart")
def bar_base():
    options = gh.option(
        gh.data(
            [
                {"week": "Mon", "temperature": 11},
                {"week": "Tue", "temperature": 12},
                {"week": "Wed", "temperature": 13},
                {"week": "Thu", "temperature": 10},
                {"week": "Fri", "temperature": 10},
                {"week": "Sat", "temperature": 13},
                {"week": "Sun", "temperature": 14},
            ]
        ),
        gh.bar_y(x="week", y="temperature"),
    )

    echarts(options)


@example(
    N_("联动"),
    "interactive",
    imports=[m_tdesign_import],
)
def reactive_anything():
    y_field = ui.state("temp1")

    options = gh.option(
        gh.data(
            [
                {"week": "Mon", "temp1": 11, "temp2": 55},
                {"week": "Tue", "temp1": 12, "temp2": 44},
                {"week": "Wed", "temp1": 13, "temp2": 66},
                {"week": "Thu", "temp1": 10, "temp2": 25},
                {"week": "Fri", "temp1": 10, "temp2": 35},
                {"week": "Sat", "temp1": 13, "temp2": 77},
                {"week": "Sun", "temp1": 14, "temp2": 88},
            ]
        ),
        gh.bar_y(x="week", y=y_field),
    )

    td.select(["temp1", "temp2"], value=y_field)
    echarts(options)


@example(
    N_("使用 polars 作为数据源"),
    "polars data source",
    imports=[m_tdesign_import, m_polars_import],
)
def data_with_polars():
    df = pl.DataFrame(
        [
            {"name": "foo", "value": 11},
            {"name": "bar", "value": 12},
            {"name": "baz", "value": 13},
        ]
    )

    options = gh.option(
        gh.data(df),
        gh.bar_y(x="name", y="value"),
    )

    echarts(options)


@example(
    N_("坐标轴排序-利用数据间接实现"),
    "axis sort by data",
    imports=[m_tdesign_import, m_polars_import],
)
def axis_sort_by_data():
    df = pl.DataFrame(
        [
            {"name": "foo", "value": 11},
            {"name": "bar", "value": 12},
            {"name": "baz", "value": 13},
        ]
    ).sort(pl.col("value"), descending=True)

    options = gh.option(
        gh.data(df),
        gh.bar_y(x="name", y="value"),
    )

    echarts(options)


@example(
    N_("坐标轴排序-axis api"),
    "axis sort by axis api",
    imports=[m_tdesign_import, m_polars_import],
)
def axis_sort_by_axis_api():
    df = pl.DataFrame(
        [
            {"name": "foo", "value": 11},
            {"name": "bar", "value": 12},
            {"name": "baz", "value": 13},
        ]
    )

    options = gh.option(
        gh.data(df),
        gh.bar_y(x="name", y="value"),
        gh.x_axis(
            options={
                "data": df.sort(pl.col("value"), descending=True)
                .select("name")
                .unique(maintain_order=True)
                .to_series()
                .to_list()
            }
        ),
    )

    echarts(options)

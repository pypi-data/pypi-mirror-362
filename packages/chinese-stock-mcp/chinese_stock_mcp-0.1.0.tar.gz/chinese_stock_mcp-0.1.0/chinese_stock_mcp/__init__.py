from typing import Any

import pysnowball as ball
from fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP(name="中国市场股票及基金数据")


# 设置 token 的工具函数
@mcp.tool
def set_token(token: str) -> str:
    """设置雪球API的访问token

    Args:
        token: 雪球API token，格式为"xq_a_token=xxx;u=xxx"

    Returns:
        返回设置成功的消息
    """
    ball.set_token(token)
    return "Token设置成功"


# 实时行情API
@mcp.tool
def get_quote(symbol: str) -> dict[str, Any]:
    """获取某支股票的实时行情数据

    Args:
        symbol: 股票代码，如'SZ002027'

    Returns:
        包含实时行情数据的字典
    """
    return ball.quotec(symbol)


@mcp.tool
def get_quote_detail(symbol: str) -> dict[str, Any]:
    """获取某支股票的详细行情数据

    Args:
        symbol: 股票代码，如'SH600104'

    Returns:
        包含详细行情数据的字典
    """
    return ball.quote_detail(symbol)


# 实时分笔数据
@mcp.tool
def get_pankou(symbol: str) -> dict[str, Any]:
    """获取实时分笔数据，可以实时取得股票当前报价和成交信息

    Args:
        symbol: 股票代码

    Returns:
        包含盘口数据的字典
    """
    return ball.pankou(symbol)


# K线数据
@mcp.tool
def get_kline(symbol: str, period: str = "day", count: int = 284) -> dict[str, Any]:
    """获取股票的K线数据

    Args:
        symbol: 股票代码
        period: K线周期，可选值: day/week/month/60m/30m/1m
        count: 返回的数据条数

    Returns:
        包含K线数据的字典
    """
    return ball.kline(symbol, period, count)


# 财务数据API
@mcp.tool
def get_earning_forecast(symbol: str) -> dict[str, Any]:
    """获取股票的业绩预告数据

    Args:
        symbol: 股票代码

    Returns:
        包含业绩预告数据的字典
    """
    return ball.earningforecast(symbol)


@mcp.tool
def get_report(symbol: str) -> dict[str, Any]:
    """获取股票的机构评级数据

    Args:
        symbol: 股票代码

    Returns:
        包含机构评级数据的字典
    """
    return ball.report(symbol)


# 资金流向API
@mcp.tool
def get_capital_flow(symbol: str) -> dict[str, Any]:
    """获取股票的资金流向数据(每分钟)

    Args:
        symbol: 股票代码

    Returns:
        包含资金流向数据的字典
    """
    return ball.capital_flow(symbol)


@mcp.tool
def get_capital_history(symbol: str) -> dict[str, Any]:
    """获取股票的历史资金流向数据(每日)

    Args:
        symbol: 股票代码

    Returns:
        包含历史资金流向数据的字典
    """
    return ball.capital_history(symbol)


@mcp.tool
def get_capital_assort(symbol: str) -> dict[str, Any]:
    """获取股票的资金成交分布数据

    Args:
        symbol: 股票代码

    Returns:
        包含资金成交分布数据的字典
    """
    return ball.capital_assort(symbol)


@mcp.tool
def get_blocktrans(symbol: str) -> dict[str, Any]:
    """获取股票的大宗交易数据

    Args:
        symbol: 股票代码

    Returns:
        包含大宗交易数据的字典
    """
    return ball.blocktrans(symbol)


@mcp.tool
def get_margin(symbol: str) -> dict[str, Any]:
    """获取股票的融资融券数据

    Args:
        symbol: 股票代码

    Returns:
        包含融资融券数据的字典
    """
    return ball.margin(symbol)


# 财务报表API
@mcp.tool
def get_indicator(symbol: str, is_annals: int = 1, count: int = 5) -> dict[str, Any]:
    """获取股票的业绩指标数据

    Args:
        symbol: 股票代码
        is_annals: 是否只获取年报(1是，0否)
        count: 返回的数据条数

    Returns:
        包含业绩指标数据的字典
    """
    return ball.indicator(symbol, is_annals, count)


@mcp.tool
def get_income(symbol: str, is_annals: int = 1, count: int = 5) -> dict[str, Any]:
    """获取股票的利润表数据

    Args:
        symbol: 股票代码
        is_annals: 是否只获取年报(1是，0否)
        count: 返回的数据条数

    Returns:
        包含利润表数据的字典
    """
    return ball.income(symbol, is_annals, count)


@mcp.tool
def get_balance(symbol: str, is_annals: int = 1, count: int = 5) -> dict[str, Any]:
    """获取股票的资产负债表数据

    Args:
        symbol: 股票代码
        is_annals: 是否只获取年报(1是，0否)
        count: 返回的数据条数

    Returns:
        包含资产负债表数据的字典
    """
    return ball.balance(symbol, is_annals, count)


@mcp.tool
def get_cash_flow(symbol: str, is_annals: int = 1, count: int = 5) -> dict[str, Any]:
    """获取股票的现金流量表数据

    Args:
        symbol: 股票代码
        is_annals: 是否只获取年报(1是，0否)
        count: 返回的数据条数

    Returns:
        包含现金流量表数据的字典
    """
    return ball.cash_flow(symbol, is_annals, count)


@mcp.tool
def get_business(symbol: str, count: int = 5) -> dict[str, Any]:
    """获取股票的主营业务构成数据

    Args:
        symbol: 股票代码
        count: 返回的数据条数

    Returns:
        包含主营业务构成数据的字典
    """
    return ball.business(symbol, count)


# F10数据API
@mcp.tool
def get_top_holders(symbol: str, circula: int = 1) -> dict[str, Any]:
    """获取股票的十大股东数据

    Args:
        symbol: 股票代码
        circula: 是否只获取流通股(1是，0否)

    Returns:
        包含十大股东数据的字典
    """
    return ball.top_holders(symbol, circula)


@mcp.tool
def get_main_indicator(symbol: str) -> dict[str, Any]:
    """获取股票的主要指标数据

    Args:
        symbol: 股票代码

    Returns:
        包含主要指标数据的字典
    """
    return ball.main_indicator(symbol)


@mcp.tool
def get_holders(symbol: str) -> dict[str, Any]:
    """获取股票的股东人数数据

    Args:
        symbol: 股票代码

    Returns:
        包含股东人数数据的字典
    """
    return ball.holders(symbol)


@mcp.tool
def get_org_holding_change(symbol: str) -> dict[str, Any]:
    """获取股票的机构持仓变动数据

    Args:
        symbol: 股票代码

    Returns:
        包含机构持仓变动数据的字典
    """
    return ball.org_holding_change(symbol)


@mcp.tool
def get_bonus(symbol: str, page: int = 1, size: int = 10) -> dict[str, Any]:
    """获取股票的分红融资数据

    Args:
        symbol: 股票代码
        page: 页码
        size: 每页数据条数

    Returns:
        包含分红融资数据的字典
    """
    return ball.bonus(symbol, page, size)


@mcp.tool
def get_industry_compare(symbol: str) -> dict[str, Any]:
    """获取股票的行业对比数据

    Args:
        symbol: 股票代码

    Returns:
        包含行业对比数据的字典
    """
    return ball.industry_compare(symbol)


# 用户数据API
@mcp.tool
def get_watch_list() -> dict[str, Any]:
    """获取用户的自选列表

    Returns:
        包含自选列表数据的字典
    """
    return ball.watch_list()


@mcp.tool
def get_watch_stock(pid: int = -1) -> dict[str, Any]:
    """获取用户自选列表的详情

    Args:
        pid: 列表ID，默认为-1(全部)

    Returns:
        包含自选股票数据的字典
    """
    return ball.watch_stock(pid)


# 组合数据API
@mcp.tool
def get_nav_daily(cube_symbol: str) -> list[dict[str, Any]]:
    """获取组合的每日净值数据

    Args:
        cube_symbol: 组合代码，如'ZH2567925'

    Returns:
        包含每日净值数据的列表
    """
    return ball.nav_daily(cube_symbol)


@mcp.tool
def get_rebalancing_history(cube_symbol: str) -> dict[str, Any]:
    """获取组合的历史调仓记录

    Args:
        cube_symbol: 组合代码

    Returns:
        包含历史调仓记录的字典
    """
    return ball.rebalancing_history(cube_symbol)


@mcp.tool
def get_rebalancing_current(cube_symbol: str) -> dict[str, Any]:
    """获取组合的当前持仓

    Args:
        cube_symbol: 组合代码

    Returns:
        包含当前持仓数据的字典
    """
    return ball.rebalancing_current(cube_symbol)


@mcp.tool
def get_quote_current(cube_symbol: str) -> dict[str, Any]:
    """获取组合的实时净值

    Args:
        cube_symbol: 组合代码

    Returns:
        包含实时净值数据的字典
    """
    return ball.quote_current(cube_symbol)


# 可转债数据API
@mcp.tool
def get_convertible_bond(page_size: int = 10, page_count: int = 1) -> dict[str, Any]:
    """获取可转债信息

    Args:
        page_size: 每页数据条数
        page_count: 页码

    Returns:
        包含可转债数据的字典
    """
    return ball.convertible_bond(page_size, page_count)


# 指数数据API
@mcp.tool
def get_index_basic_info(index_code: str) -> dict[str, Any]:
    """获取指数的基本信息

    Args:
        index_code: 指数代码，如'399967'(中证军工)

    Returns:
        包含指数基本信息的字典
    """
    return ball.index_basic_info(index_code)


@mcp.tool
def get_index_details(index_code: str) -> dict[str, Any]:
    """获取指数的详细信息

    Args:
        index_code: 指数代码

    Returns:
        包含指数详细信息的字典
    """
    return ball.index_details_data(index_code)


@mcp.tool
def get_index_weight_top10(index_code: str) -> dict[str, Any]:
    """获取指数前十大权重股

    Args:
        index_code: 指数代码

    Returns:
        包含前十大权重股数据的字典
    """
    return ball.index_weight_top10(index_code)


@mcp.tool
def get_index_perf(index_code: str, days: int = 7) -> dict[str, Any]:
    """获取指数的表现数据

    Args:
        index_code: 指数代码
        days: 天数(7/30/90)

    Returns:
        包含指数表现数据的字典
    """
    if days == 7:
        return ball.index_perf_7(index_code)
    if days == 30:
        return ball.index_perf_30(index_code)
    if days == 90:
        return ball.index_perf_90(index_code)
    return {"error": "Invalid days parameter, must be 7, 30 or 90"}


# 北向资金数据API
@mcp.tool
def get_northbound_sh(date: str | None = None) -> list[dict[str, Any]]:
    """获取沪股通北向资金持股数据

    Args:
        date: 日期，格式为'YYYY/MM/DD'，如不提供则使用当天

    Returns:
        包含北向资金持股数据的列表
    """
    if date:
        return ball.northbound_shareholding_sh(date)
    return ball.northbound_shareholding_sh()


@mcp.tool
def get_northbound_sz(date: str | None = None) -> list[dict[str, Any]]:
    """获取深股通北向资金持股数据

    Args:
        date: 日期，格式为'YYYY/MM/DD'，如不提供则使用当天

    Returns:
        包含北向资金持股数据的列表
    """
    if date:
        return ball.northbound_shareholding_sz(date)
    return ball.northbound_shareholding_sz()


# 基金数据API
@mcp.tool
def get_fund_detail(fund_code: str) -> dict[str, Any]:
    """获取基金详情数据

    Args:
        fund_code: 基金代码，如'008975'

    Returns:
        包含基金详情数据的字典
    """
    return ball.fund_detail(fund_code)


@mcp.tool
def get_fund_info(fund_code: str) -> dict[str, Any]:
    """获取基金基本信息

    Args:
        fund_code: 基金代码

    Returns:
        包含基金基本信息的字典
    """
    return ball.fund_info(fund_code)


@mcp.tool
def get_fund_growth(fund_code: str) -> dict[str, Any]:
    """获取基金成长数据

    Args:
        fund_code: 基金代码

    Returns:
        包含基金成长数据的字典
    """
    return ball.fund_growth(fund_code)


@mcp.tool
def get_fund_nav_history(fund_code: str) -> dict[str, Any]:
    """获取基金历史净值

    Args:
        fund_code: 基金代码

    Returns:
        包含基金历史净值数据的字典
    """
    return ball.fund_nav_history(fund_code)


@mcp.tool
def get_fund_achievement(fund_code: str) -> dict[str, Any]:
    """获取基金业绩数据

    Args:
        fund_code: 基金代码

    Returns:
        包含基金业绩数据的字典
    """
    return ball.fund_achievement(fund_code)


@mcp.tool
def get_fund_asset(fund_code: str) -> dict[str, Any]:
    """获取基金资产配置

    Args:
        fund_code: 基金代码

    Returns:
        包含基金资产配置数据的字典
    """
    return ball.fund_asset(fund_code)


@mcp.tool
def get_fund_manager(fund_code: str) -> dict[str, Any]:
    """获取基金经理信息

    Args:
        fund_code: 基金代码

    Returns:
        包含基金经理信息的字典
    """
    return ball.fund_manager(fund_code)


@mcp.tool
def get_fund_trade_date(fund_code: str) -> dict[str, Any]:
    """获取基金交易日期

    Args:
        fund_code: 基金代码

    Returns:
        包含基金交易日期数据的字典
    """
    return ball.fund_trade_date(fund_code)


@mcp.tool
def get_fund_derived(fund_code: str) -> dict[str, Any]:
    """获取基金衍生数据

    Args:
        fund_code: 基金代码

    Returns:
        包含基金衍生数据的字典
    """
    return ball.fund_derived(fund_code)


# 股票搜索API
@mcp.tool
def search_stock(keyword: str) -> dict[str, Any]:
    """根据关键词搜索股票

    Args:
        keyword: 搜索关键词

    Returns:
        包含搜索结果的数据字典
    """
    return ball.suggest_stock(keyword)

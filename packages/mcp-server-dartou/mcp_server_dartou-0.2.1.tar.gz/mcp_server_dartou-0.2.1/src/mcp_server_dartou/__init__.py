#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mcp.server.fastmcp import FastMCP
import requests
import json
import os
import argparse
from datetime import datetime, timedelta
from typing import List, Optional

# 解析命令行参数
parser = argparse.ArgumentParser(description='广告数据查询MCP服务')
parser.add_argument('--token', type=str, required=True, help='API访问token')
args = parser.parse_args()

# 创建MCP服务器
mcp = FastMCP("广告数据查询服务")

# 从命令行获取token
def get_token_from_config():
    # 只从命令行获取token
    if args.token:
        return args.token
    else:
        raise ValueError("必须提供命令行参数--token")

def compress_response(response_data: dict, requested_zhibiao=None, is_deep=False) -> dict:
    """
    压缩API响应数据，减少token占用
    
    策略：
    1. 将list数据转换为表格格式（表头+行数据）
    2. 将原始字段名转换为中文指标名作为headers
    3. 只保留用户请求的指标，过滤掉不需要的数据
    4. 不返回prop_map映射关系，直接使用中文表头
    5. 当is_deep为True时，额外保留所有以UI结尾的字段，确保下探功能正常工作
    """
    if not response_data or response_data.get('code') != 0:
        return response_data
    
    data = response_data.get('data', {})
    if not data:
        return response_data
    
    result = {
        "code": response_data.get('code'),
        "msg": response_data.get('msg')
    }
    
    # 处理列表数据
    items = data.get('list', [])
    if not items:
        result['data'] = data
        return result
    
    # 获取propMap用于转换表头
    prop_map = data.get('propMap', {})
    
    # 如果用户提供了指定的指标列表，准备要保留的字段
    field_indices_to_keep = None
    requested_fields = []
    if requested_zhibiao and prop_map:
        # 找出用户请求指标对应的英文字段名
        for zhibiao in requested_zhibiao:
            if zhibiao in prop_map:
                requested_fields.append(prop_map[zhibiao])
        
        if requested_fields:
            field_indices_to_keep = []
    
    # 构建压缩后的表格式数据
    all_headers = list(items[0].keys())
    
    # 反转propMap，创建从英文字段名到中文指标名的映射
    reverse_prop_map = {}
    if prop_map:
        for cn_name, en_field in prop_map.items():
            reverse_prop_map[en_field] = cn_name
    
    # 转换headers为中文，并过滤字段
    headers = []
    filtered_indices = []  # 要保留的字段索引
    date_index = -1  # 日期字段的索引
    
    for i, field in enumerate(all_headers):
        # 判断是否保留该字段
        keep_field = True
        
        # 如果指定了要保留的字段，检查当前字段是否在列表中
        if field_indices_to_keep is not None:
            # 如果是下探查询(is_deep=True)且字段以UI结尾，则保留
            if is_deep and field.endswith('UI'):
                keep_field = True
            # 否则，只保留用户请求的字段
            elif field not in requested_fields:
                keep_field = False
        
        if not keep_field:
            continue
        
        # 将英文字段名转换为中文指标名
        if field in reverse_prop_map:
            header_name = reverse_prop_map[field]
            headers.append(header_name)
            # 记录日期字段的索引
            if header_name == '日期':
                date_index = len(headers) - 1
        else:
            headers.append(field)  # 如果没有对应的中文名，保留英文名
            # 检查是否为Date字段
            if field == 'Date':
                date_index = len(headers) - 1
        
        filtered_indices.append(i)
    
    # 预先检查是否有总计行
    has_total_row = False
    total_row_index = -1
    for idx, item in enumerate(items):
        if 'Date' in item and item['Date'] == '总计':
            has_total_row = True
            total_row_index = idx
            break
    
    # 按过滤后的索引提取数据
    rows = []
    for idx, item in enumerate(items):
        item_values = list(item.values())
        # 只保留需要的字段
        filtered_row = [item_values[i] for i in filtered_indices]
        
        # 如果是总计行且日期字段存在，确保其值为"总计"
        if has_total_row and idx == total_row_index and date_index >= 0 and len(filtered_row) > date_index:
            filtered_row[date_index] = "总计"
        
        rows.append(filtered_row)
    
    # 如果没有找到明确的总计行，但有多行数据，则假设最后一行是总计行
    if not has_total_row and len(rows) > 1 and date_index >= 0:
        # 检查最后一行的日期字段是否为空或非日期格式
        last_row = rows[-1]
        if len(last_row) > date_index:
            if not last_row[date_index] or last_row[date_index] == "":
                last_row[date_index] = "总计"
    
    # 构建结果 - 使用中文字段名，不返回prop_map
    compressed_data = {
        "headers": headers,  # 已转换为中文的表头
        "rows": rows
    }
    
    result['data'] = compressed_data
    
    return result

@mcp.tool()
def get_ad_count_list(
    version: str = "0.1.85", 
    appid: str = "59",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    zhibiao_list: Optional[List[str]] = ["日期", "创角成本", "新增创角", "广告计划名称", "创意名称", "项目名称", "广告状态", "备注", "新增注册", "创角率", "点击率", "激活率", "点击成本", "活跃用户", "曝光次数", "千次展现均价", "点击数", "一阶段花费", "二阶段花费", "当日充值", "当日付费次数", "当日充值人数", "新增付费人数", "首充付费人数", "首充付费次数", "老用户付费人数", "新增付费金额", "首充付费金额", "老用户付费金额", "新增付费率", "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额", "小游戏注册首日广告变现ROI", "当月注册用户充值金额", "消耗", "新增付费成本", "付费成本", "注册成本", "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI", "付费首日ROI", "付费累计ROI", "付费分成后首日ROI", "付费分成后累计ROI", "计算累计ROI所用金额", "计算累计ROI所用消耗", "24小时ROI"],
    media: Optional[List[str]] = None,
    group_key: Optional[str] = None,
    toushou: Optional[List[str]] = None,
    self_cid: Optional[List[str]] = None,
    ji_hua_id: Optional[List[str]] = None,
    ji_hua_name: Optional[str] = None,
    ad_status: Optional[List[str]] = None,
    creative_id: Optional[List[str]] = None,
    vp_adgroup_id: Optional[List[str]] = None,
    is_deep: Optional[bool] = False,
) -> dict:
    """
## get_ad_count_list工具说明

当用户需要分析广告数据时，你需要使用MCP工具`get_ad_count_list`来查询广告数据。该工具可以获取广告投放的各类指标数据，支持多种筛选和分组方式。

### 返回结果说明

返回格式为表格形式，包含headers(表头)和rows(数据行)，headers与rows一一对应:
```
{
    "code": 0,
    "msg": "查询成功",
    "data": {
        "headers": ["日期", "创角成本", "新增创角", ...], // 中文指标名
        "rows": [
            ["20250711", 4.86, 3773, ...],   // 第一行数据
            ["20250710", 7.62, 2340, ...],   // 第二行数据
            ["总计", 12345.67, 6113, ...],   // 最后一行是所有数据的总计行
            ...
        ]
    }
}
```

特别注意：返回结果中最后一行通常是总计行，其第一列（日期列）的值为"总计"，表示该行是所有数据的汇总。

### 参数详情

调用函数时需要提供以下参数，除了必填参数之外，其余参数如果用户未提及，则用默认值：

1. **version** (必填，字符串)

   - 系统版本，默认值："0.1.85"

2. **appid** (选填，字符串)

   - 游戏ID，默认值："59"（正统三国）

3. **start_time** (必填，字符串)

   - 开始时间，格式：YYYY-MM-DD

   - 例如："2023-01-01"

   - 注意：如果只查询一天数据，start_time和end_time需设为同一天

4. **end_time** (必填，字符串)

   - 结束时间，格式：YYYY-MM-DD

   - 例如："2023-01-31"

   - 注意：如果只查询一天数据，start_time和end_time需设为同一天

5. **zhibiao_list** (必填，字符串数组)

   - 默认值:["日期", "创角成本", "新增创角", "广告计划名称", "创意名称", "项目名称", "广告状态", "备注", "新增注册", "创角率", "点击率", "激活率", "点击成本", "活跃用户", "曝光次数", "千次展现均价", "点击数", "一阶段花费", "二阶段花费", "当日充值", "当日付费次数", "当日充值人数", "新增付费人数", "首充付费人数", "首充付费次数", "老用户付费人数", "新增付费金额", "首充付费金额", "老用户付费金额", "新增付费率", "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额", "小游戏注册首日广告变现ROI", "当月注册用户充值金额", "消耗", "新增付费成本", "付费成本", "注册成本", "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI", "付费首日ROI", "付费累计ROI", "付费分成后首日ROI", "付费分成后累计ROI", "计算累计ROI所用金额", "计算累计ROI所用消耗", "24小时ROI"]。

6. **media** (选填，字符串数组)

   - 媒体列表，默认为空

   - 可选值：全选(全选)、sphdr(视频号达人)、bd(百度)、xt(星图)、bdss(百度搜索)、gdt(广点通)、bz(b站)、zh(知乎)、dx(抖小广告量)、tt(今日头条)、uc(uc)、gg(谷歌)、nature(自然量)

   - 例如：["gdt"] 表示查询广点通

7. **group_key** (选填，字符串)

   - 分组键，默认为空

   - 可选值：vp_advert_pitcher_id(投手)、dt_vp_fx_cid(self_cid)、vp_adgroup_id(项目id)、vp_advert_channame(媒体)、vp_campaign_id(广告id)、vp_originality_id(创意id)

   - 例如："vp_campaign_id" 表示按广告ID分组

8. **toushou** (选填，字符串数组)

   - 投手列表，默认为空

   - 可选值：lll(李霖林)、dcx(戴呈翔)、yxr(尹欣然)、syf(施逸风)、gyy(郭耀月)、zp(张鹏)、zmn(宗梦男)

   - 例如：["lll"] 表示查询李霖林的投放数据

9. **self_cid** (选填，字符串数组)

   - 广告cid，默认为空

   - 例如：["ztsg_gdt_lll_3342", "ztsg_xt_zp_1"]

10. **ji_hua_id** (选填，字符串数组)

    - 广告id，默认为空

    - 例如：["41910413241", "40159842292"]

11. **ji_hua_name** (选填，字符串)

    - 广告名称，默认为空

    - 例如："02-0515-站内-词包1-双出价-3977"

12. **ad_status** (选填，字符串数组)

    - 广告状态，默认为空

    - 可选值：ADGROUP_STATUS_FROZEN(已冻结)、ADGROUP_STATUS_SUSPEND(暂停中)、ADGROUP_STATUS_DELETED(已删除)、ADGROUP_STATUS_NOT_IN_DELIVERY_TIME(广告未到投放时间)、ADGROUP_STATUS_ACTIVE(投放中)、ADGROUP_STATUS_ACCOUNT_BALANCE_NOT_ENOUGH(账户余额不足)、ADGROUP_STATUS_DAILY_BUDGET_REACHED(广告达到日预算上限)、ADGROUP_STATUS_STOP(投放结束)

    - 例如：["ADGROUP_STATUS_ACTIVE"] 表示查询投放中的广告

13. **creative_id** (选填，字符串数组)

    - 创意id，默认为空

    - 例如：["12", "87"]

14. **vp_adgroup_id** (选填，字符串数组)

    - 项目id，默认为空

    - 例如：["0", "159842"]

15. **is_deep** (选填，布尔值)

    - 是否获取下探ui，默认为False,只有需要下探数据时才设置为True

特别注意：所有列表类型参数必须使用正确的JSON数组格式，例如：

- 正确：["创角成本", "新增创角"]

- 错误："创角成本,新增创角"

媒体参数必须使用规定的代码而非中文名称：

- 正确：["gdt"]（代表广点通）

- 错误：["广点通"]

## 重要提示

1. zhibiao_list默认值:["日期", "创角成本", "新增创角", "广告计划名称", "创意名称", "项目名称", "广告状态", "备注", "新增注册", "创角率", "点击率", "激活率", "点击成本", "活跃用户", "曝光次数", "千次展现均价", "点击数", "一阶段花费", "二阶段花费", "当日充值", "当日付费次数", "当日充值人数", "新增付费人数", "首充付费人数", "首充付费次数", "老用户付费人数", "新增付费金额", "首充付费金额", "老用户付费金额", "新增付费率", "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额", "小游戏注册首日广告变现ROI", "当月注册用户充值金额", "消耗", "新增付费成本", "付费成本", "注册成本", "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI", "付费首日ROI", "付费累计ROI", "付费分成后首日ROI", "付费分成后累计ROI", "计算累计ROI所用金额", "计算累计ROI所用消耗", "24小时ROI"]

2. 如果用户只查询一天的数据，需要把开始时间和结束时间都设为同一天

3. 多个筛选条件可以组合使用，如媒体+投手、广告ID+状态等
    """
    

    token = get_token_from_config()
    
    # 设置默认值
    if start_time is None:
        # 默认查询昨天的数据
        yesterday = datetime.now() - timedelta(days=1)
        start_time = yesterday.strftime("%Y-%m-%d")
    
    if end_time is None:
        # 默认查询到今天
        end_time = datetime.now().strftime("%Y-%m-%d")
    if zhibiao_list is None:
        zhibiao_list = ["日期", "创角成本", "新增创角", "广告计划名称", "创意名称", "项目名称", "广告状态", "备注", "新增注册", "创角率", "点击率", "激活率", "点击成本", "活跃用户", "曝光次数", "千次展现均价", "点击数", "一阶段花费", "二阶段花费", "当日充值", "当日付费次数", "当日充值人数", "新增付费人数", "首充付费人数", "首充付费次数", "老用户付费人数", "新增付费金额", "首充付费金额", "老用户付费金额", "新增付费率", "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额", "小游戏注册首日广告变现ROI", "当月注册用户充值金额", "消耗", "新增付费成本", "付费成本", "注册成本", "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI", "付费首日ROI", "付费累计ROI", "付费分成后首日ROI", "付费分成后累计ROI", "计算累计ROI所用金额", "计算累计ROI所用消耗", "24小时ROI"]

    # API接口地址
    url = "https://bi.dartou.com/testapi/ad/GetAdCountList"
    
    # 设置请求头
    headers = {
        "X-Token": token,
        "X-Ver": version,
        "Content-Type": "application/json"
    }
    
    # 构建请求体
    payload = {
        "appid": appid,
        "start_time": start_time,
        "end_time": end_time,
        "zhibiao_list": zhibiao_list,
        "media": media,
        "group_key": group_key,
        "toushou": toushou,
        "self_cid": self_cid,
        "ji_hua_id": ji_hua_id,
        "ji_hua_name": ji_hua_name,
        "ad_status": ad_status,
        "creative_id": creative_id,
        "vp_adgroup_id": vp_adgroup_id,
        "is_deep": is_deep
    }
    
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 解析响应
        result = response.json()
        
        # 检查响应状态
        if result.get("code") == 0:
            print("请求成功!")
            return compress_response(result, zhibiao_list, is_deep)
        else:
            print(f"请求失败: {result.get('msg')}")
            return result
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"code": -1, "msg": str(e)}
    

def main() -> None:
    mcp.run(transport="stdio")

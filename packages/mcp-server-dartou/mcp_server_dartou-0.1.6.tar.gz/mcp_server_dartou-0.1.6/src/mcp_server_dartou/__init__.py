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

def compress_response(response_data: dict) -> dict:
    """
    压缩API响应数据，减少token占用
    
    策略：
    1. 将list数据转换为表格格式（表头+行数据）
    2. 直接使用原始字段名作为headers
    3. 移除冗余映射关系
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
    
    # 提取第一个对象的所有键作为表头
    if items:
        # 构建压缩后的表格式数据
        headers = list(items[0].keys())
        rows = []
        for item in items:
            rows.append([item.get(h, '') for h in headers])
        
        # 构建结果 - 直接使用原始字段名，移除field_map
        compressed_data = {
            "headers": headers,  # 直接使用原始字段名
            "rows": rows
        }
        
        # 如果需要，保留propMap的简化版本
        if 'propMap' in data:
            compressed_data['prop_map'] = data['propMap']
        
        result['data'] = compressed_data
    else:
        result['data'] = data
    
    return result

@mcp.tool()
def get_ad_count_list(
    version: str = "0.1.85", 
    appid: str = "59",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    zhibiao_list: Optional[List[str]] = None,
    media: Optional[List[str]] = None,
    group_key: Optional[str] = None,
    toushou: Optional[List[str]] = None,
    self_cid: Optional[List[str]] = None,
    ji_hua_id: Optional[List[str]] = None,
    ji_hua_name: Optional[str] = None,
    ad_status: Optional[List[str]] = None,
    creative_id: Optional[List[str]] = None,
    vp_adgroup_id: Optional[List[str]] = None,
    is_deep: Optional[bool] = True,
) -> dict:
    """
## get_ad_count_list工具说明

当用户需要分析广告数据时，你需要使用MCP工具`get_ad_count_list`来查询广告数据。该工具可以获取广告投放的各类指标数据，支持多种筛选和分组方式。

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

    - 是否获取下探ui，默认为True

特别注意：所有列表类型参数必须使用正确的JSON数组格式，例如：

- 正确：["创角成本", "新增创角"]

- 错误："创角成本,新增创角"

媒体参数必须使用规定的代码而非中文名称：

- 正确：["gdt"]（代表广点通）

- 错误：["广点通"]


### 返回数据格式说明

函数返回经过压缩的API响应数据，结构如下：

```
{
    "code": 0,
    "msg": "success",
    "data": {
        "headers": ["字段1", "字段2", "字段3", ...],
        "rows": [
            ["值1", "值2", "值3", ...],
            ["值1", "值2", "值3", ...],
            ...
        ],
        "prop_map": {
      "24小时ROI": "24h_pay_amount_roi",
      "7日ROI": "sevenRoi",
      "一键起量消耗": "sum_acquisition_cost",
      "一阶段花费": "sum_wechat_cost_stage1",
      "二阶段花费": "sum_wechat_cost_stage2",
      "付费分成后累计ROI": "divideAccumulativeROI",
      "付费分成后首日ROI": "dividefirstDayRoi",
      "付费成本": "payPrimeCost",
      "付费累计ROI": "accumulativeROI",
      "付费首日ROI": "firstDayRoi",
      "分成后累计ROI": "divideAccumulativeAllROI",
      "分成后首日ROI": "dividefirstDayAllRoi",
      "创意名称": "vp_creative_name",
      "创角成本": "createRolePrimeCost",
      "创角率": "createRoleScale",
      "千次展现均价": "thousand_display_price",
      "备注": "vp_cid_remark",
      "小游戏广告变现金额（平台上报）": "adBuyMoney2",
      "小游戏注册首日广告变现ROI": "income_val_24h_roi",
      "小游戏注册首日广告变现金额": "income_val_24hs",
      "广告变现人数": "adBuyUsers",
      "广告变现成本": "adBuyCost",
      "广告状态": "vp_ad_status",
      "广告计划名称": "vp_campaign_name",
      "当日付费次数": "payCount",
      "当日充值": "payMoney",
      "当日充值人数": "payUser",
      "新增arppu": "newPayArpu",
      "新增付费人数": "newPayUser",
      "新增付费成本": "newPayPrimeCost",
      "新增付费率": "newPayScale",
      "新增付费金额": "newPayMoney",
      "新增创角": "regRoleCount",
      "新增注册": "regUserCount",
      "日期": "Date",
      "曝光次数": "view_count",
      "注册成本": "regPrimeCost",
      "注册首日广告变现arppu": "income_val_24h_arppu",
      "注册首日广告变现人数": "income_val_24h_count",
      "注册首日广告变现成本": "income_val_24h_cost",
      "活跃arppu": "activeArpu",
      "活跃付费率": "activeUserScale",
      "活跃用户": "activeUserCount",
      "消耗": "cost",
      "激活率": "activeScale",
      "点击成本": "clickPrimeCost",
      "点击数": "click_cnt",
      "点击率": "clickScale",
      "累计ROI": "accumulativeAllROI",
      "老用户付费人数": "oldPayUser",
      "老用户付费金额": "oldPayMoney",
      "计算累计ROI所用消耗": "accumulativeCost",
      "计算累计ROI所用金额": "accumulatedPayMoney",
      "项目名称": "vp_adgroup_name",
      "首充付费人数": "accumulatedPayUser",
      "首充付费次数": "accumulatedPayCount",
      "首充付费金额": "accumulatedFirstPayMoney",
      "首日ROI": "firstDayAllRoi"
    }
    
}
```

数据对应关系说明：
1. `headers`：表头字段名列表，与原始API返回的字段名保持一致
2. `rows`：表格行数据，每行是一个数组，数组中的元素与`headers`一一对应
3. `prop_map`：属性映射关系，提供特定字段的中文含义，如"累计ROI"对应"accumulativeAllROI"

例如，如果`headers`是`["日期", "消耗", "点击数"]`，那么`rows`中的每个数组元素分别对应这些字段：
- `rows[0][0]`对应第一行的"日期"
- `rows[0][1]`对应第一行的"消耗"
- `rows[0][2]`对应第一行的"点击数"

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
            return compress_response(result)
        else:
            print(f"请求失败: {result.get('msg')}")
            return result
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"code": -1, "msg": str(e)}
    
@mcp.tool()
def get_order_list(
    appid: str = "59",
    start_time: str = None,
    end_time: str = None,
    dt_part_time_col: str = "toYYYYMMDD(dt_part_date)",
    isDistinct: bool = False,
    is_new_ver: bool = True,
    page: int = 1,
    ui: str = None,
    limit: int = 20,
    type: int = 1,
    openID: Optional[str] = None,
    orderByCol: Optional[str] = None,
    orderByType: Optional[str] = None,
    version: str = "0.1.77"
) -> dict:
    """
# get_order_list工具说明

当用户需要分析广告数据下探详情时，你需要使用MCP工具get_order_list来查询广告数据下探数据。该工具可以根据指标ID获取详细订单列表数据，支持多种筛选条件。

## 参数详情

调用函数时需要提供以下参数，除了必填参数之外，其余参数如果用户未提及，则用默认值:

### appid (选填，字符串)

- 游戏ID，默认值:"59"(正统三国)

### start_time (必填，字符串)

- 查询范围开始时间，格式：YYYYMMDD

- 例如:"20230101"

- 默认值:昨天日期

### end_time (必填，字符串)

- 查询范围结束时间，格式：YYYYMMDD

- 例如:"20230131"

- 默认值:今天日期

### dt_part_time_col (选填，字符串)

- 查询SQL片段，默认值:"toYYYYMMDD(dt_part_date)"

### isDistinct (选填，布尔值)

- 是否进行openid去重，默认值:false

### is_new_ver (选填，布尔值)

- 后端业务参数，默认值:true

### page (选填，整数)

- 当前页码，默认值:1

### ui (必填，字符串)

- 下探行唯一ID，需要从get_ad_count_list工具返回的ui获得

### limit (选填，整数)

- 每页查询数量，默认值:20

### type (必填，整数)

- 下探指标名称映射，默认值:1

- 可选值:1(新增注册)、2(新增创角)、3(活跃用户)，其他指标传0

### openID (选填，字符串)

- 微信openID，默认为空

### orderByCol (选填，字符串)

- 排序字段，默认为空

### orderByType (选填，字符串)

- 排序类型，默认为空

- 可选值:asc(升序)、desc(降序)

### version (选填，字符串)

- API版本号，默认值:"0.1.85"

## 特别注意

- ui参数是必填的、type参数是必填的、start_time参数是必填的、end_time参数是必填的，其他参数如果用户未提及则使用默认值

- 日期格式必须严格遵循YYYYMMDD格式

- 如果查询一段时间的数据，需确保end_time不早于start_time

## 调用入参示例

### 查询指定唯一ID的新增注册数据(默认)

```

ui="abc123",

type=1

```

### 查询2023年1月1日至1月31日的新增创角数据，每页显示50条

```

start_time="20230101",

end_time="20230131",

ui="abc123",

type=2,

limit=50

```

### 查询活跃用户数据并按某字段降序排序

```

ui="abc123",

type=3,

orderByCol="some_field",

orderByType="desc"

```

### 返回数据格式说明

函数返回经过压缩的API响应数据，结构如下：

```
{
    "code": 0,
    "msg": "success",
    "data": {
        "headers": ["字段1", "字段2", "字段3", ...],
        "rows": [
            ["值1", "值2", "值3", ...],
            ["值1", "值2", "值3", ...],
            ...
        ],
        "prop_map": {
      "24小时ROI": "24h_pay_amount_roi",
      "7日ROI": "sevenRoi",
      "一键起量消耗": "sum_acquisition_cost",
      "一阶段花费": "sum_wechat_cost_stage1",
      "二阶段花费": "sum_wechat_cost_stage2",
      "付费分成后累计ROI": "divideAccumulativeROI",
      "付费分成后首日ROI": "dividefirstDayRoi",
      "付费成本": "payPrimeCost",
      "付费累计ROI": "accumulativeROI",
      "付费首日ROI": "firstDayRoi",
      "分成后累计ROI": "divideAccumulativeAllROI",
      "分成后首日ROI": "dividefirstDayAllRoi",
      "创意名称": "vp_creative_name",
      "创角成本": "createRolePrimeCost",
      "创角率": "createRoleScale",
      "千次展现均价": "thousand_display_price",
      "备注": "vp_cid_remark",
      "小游戏广告变现金额（平台上报）": "adBuyMoney2",
      "小游戏注册首日广告变现ROI": "income_val_24h_roi",
      "小游戏注册首日广告变现金额": "income_val_24hs",
      "广告变现人数": "adBuyUsers",
      "广告变现成本": "adBuyCost",
      "广告状态": "vp_ad_status",
      "广告计划名称": "vp_campaign_name",
      "当日付费次数": "payCount",
      "当日充值": "payMoney",
      "当日充值人数": "payUser",
      "新增arppu": "newPayArpu",
      "新增付费人数": "newPayUser",
      "新增付费成本": "newPayPrimeCost",
      "新增付费率": "newPayScale",
      "新增付费金额": "newPayMoney",
      "新增创角": "regRoleCount",
      "新增注册": "regUserCount",
      "日期": "Date",
      "曝光次数": "view_count",
      "注册成本": "regPrimeCost",
      "注册首日广告变现arppu": "income_val_24h_arppu",
      "注册首日广告变现人数": "income_val_24h_count",
      "注册首日广告变现成本": "income_val_24h_cost",
      "活跃arppu": "activeArpu",
      "活跃付费率": "activeUserScale",
      "活跃用户": "activeUserCount",
      "消耗": "cost",
      "激活率": "activeScale",
      "点击成本": "clickPrimeCost",
      "点击数": "click_cnt",
      "点击率": "clickScale",
      "累计ROI": "accumulativeAllROI",
      "老用户付费人数": "oldPayUser",
      "老用户付费金额": "oldPayMoney",
      "计算累计ROI所用消耗": "accumulativeCost",
      "计算累计ROI所用金额": "accumulatedPayMoney",
      "项目名称": "vp_adgroup_name",
      "首充付费人数": "accumulatedPayUser",
      "首充付费次数": "accumulatedPayCount",
      "首充付费金额": "accumulatedFirstPayMoney",
      "首日ROI": "firstDayAllRoi"
    }
}
```

数据对应关系说明：
1. `headers`：表头字段名列表，与原始API返回的字段名保持一致
2. `rows`：表格行数据，每行是一个数组，数组中的元素与`headers`一一对应
3. `prop_map`：属性映射关系，提供特定字段的中文含义，如"首日ROI"对应"firstDayAllRoi"

例如，如果`headers`是`["用户ID", "注册时间", "设备型号"]`，那么`rows`中的每个数组元素分别对应这些字段：
- `rows[0][0]`对应第一行的"用户ID"
- `rows[0][1]`对应第一行的"注册时间"
- `rows[0][2]`对应第一行的"设备型号"

## 重要提示

- 必须提供下探行唯一ID(ui)、下探指标名称映射(type)、查询范围开始时间(start_time)、查询范围结束时间(end_time)，这是必填参数

- 默认情况下查询的是昨天到今天的数据

- 查询结果会分页显示，默认每页20条，可通过page和limit参数控制分页，默认page=1，limit=20，需要和用户说明清楚

- 可以通过orderByCol和orderByType参数控制返回结果的排序方式
    """
    
    token = get_token_from_config()
    
    # 设置默认值
    if start_time is None:
        # 默认查询昨天的数据
        yesterday = datetime.now() - timedelta(days=1)
        start_time = yesterday.strftime("%Y%m%d")
    
    if end_time is None:
        # 默认查询到今天
        end_time = datetime.now().strftime("%Y%m%d")
    
    if ui is None:
        raise ValueError("必须提供下探行唯一ID (ui)")

    # API接口地址
    url = "https://bi.dartou.com/testapi/ad/GetOrderList"
    
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
        "dt_part_time_col": dt_part_time_col,
        "isDistinct": isDistinct,
        "is_new_ver": is_new_ver,
        "page": page,
        "ui": ui,
        "limit": limit,
        "type": type
    }
    
    # 添加可选参数
    if openID is not None and openID != "":
        payload["openID"] = openID
    
    if orderByCol is not None and orderByCol != "":
        payload["orderByCol"] = orderByCol
    
    if orderByType is not None and orderByType != "":
        payload["orderByType"] = orderByType
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # 解析响应
        result = response.json()
        
        # 检查响应状态
        if result.get("code") == 0:
            print("数据下探请求成功!")
            return compress_response(result)
        else:
            print(f"数据下探请求失败: {result.get('msg')}")
            return result
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"code": -1, "msg": str(e)}

def main() -> None:
    mcp.run(transport="stdio")

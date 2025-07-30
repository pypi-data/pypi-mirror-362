from mcp.server.fastmcp import FastMCP
import requests
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Optional
from enum import IntEnum
from collections import defaultdict

# 解析命令行参数
parser = argparse.ArgumentParser(description='广告素材数据查询MCP服务')
parser.add_argument('--token', type=str, required=True, help='API访问token')
args = parser.parse_args()

# 创建MCP服务器
mcp = FastMCP("广告素材数据查询服务")

ZHI_BIAO_FIELD_MAP = {
    # 基础信息类
    "日期": "date",
    "素材id": "vp_originality_id",
    "素材名称": "vp_originality_name",
    "素材类型": "vp_originality_type",
    "素材封面uri": "cover_uri",
    "视频uri": "show_video_uris",
    "制作人": "producer",
    "创意人": "creative_user",
    "素材创造时间": "created_at",

    # 效果指标类
    "3秒播放率": "play_3s_rate",
    "完播率": "completion_rate",
    "是否低效素材": "is_inefficient_material",
    "是否AD低质素材": "is_ad_low_quality_material",
    "是否AD优质素材": "is_ad_high_quality_material",
    "低质原因": "low_quality_reason",

    # 转化指标类
    "新增注册": "regUserCount",
    "新增创角": "regRoleCount",
    "创角率": "role_creation_rate",
    "点击率": "click_rate",
    "激活率": "activation_rate",
    "点击成本": "clickPrimeCost",
    "活跃用户": "activeScale",
    "当日充值": "payMoney",
    "当日付费次数": "payCount",
    "当日充值人数": "payUser",
    "新增付费人数": "newPayUser",
    "首充付费人数": "first_pay_users",
    "新增付费金额": "newPayMoney",
    "首充付费金额": "first_pay_money",
    "新增付费率": "new_pay_rate",
    "活跃付费率": "active_pay_rate",
    "活跃arppu": "active_arppu",
    "新增arppu": "new_arppu",

    # ROI相关
    "小游戏注册首日广告变现金额": "income_val_24hs",
    "小游戏注册首日广告变现ROI": "income_val_24h_roi",
    "消耗": "cost",
    "新增付费成本": "newPayPrimeCost",
    "付费成本": "payPrimeCost",
    "注册成本": "regRolePrimeCost",
    "创角成本": "createRolePrimeCost",
    "首日ROI": "firstDayRoi",
    "累计ROI": "accumulativeROI",
    "分成后首日ROI": "dividefirstDayRoi",
    "分成后累计ROI": "dividedAccumulativeROI",
}

# 新增API返回字段映射表
API_FIELD_MAP = {
    "vp_originality_id": "show_vp_originality_id",
    "vp_originality_name": "show_originality_names",
    "vp_originality_type": "show_originality_type",
    "cover_uri": "show_img_uris",
    "show_video_uris": "show_video_uris",
    "producer": "show_producers",
    "creative_user": "show_creative_persons",
    "created_at": "show_material_create_times",
    "is_inefficient_material": "show_is_inefficient_material",
    # 其余字段如API返回与ZHI_BIAO_FIELD_MAP一致的可不写
}


class AdQualityOption(IntEnum):
    DEFAULT = -1
    HIGH_QUALITY = 1
    LOW_QUALITY = 2


def get_token_from_config():
    # 只从命令行获取token
    if args.token:
        return args.token
    else:
        raise ValueError("必须提供命令行参数--token")


def is_numeric(value):
    """判断是否为可转换为浮点数的值"""
    try:
        if value is None:
            return False
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def safe_float(value):
    """安全地将字符串或 None 转为 float"""
    try:
        return float(value)
    except (TypeError, ValueError, KeyError):
        return 0.0


def generate_markdown_table(data_list: List[dict], zhibiao_list: Optional[List[str]] = None) -> tuple[str, dict]:
    if not data_list:
        return "无数据可生成表格", {}

    if zhibiao_list:
        display_headers = zhibiao_list
        actual_headers = [ZHI_BIAO_FIELD_MAP.get(z, z) for z in zhibiao_list]
    else:
        display_headers = list(ZHI_BIAO_FIELD_MAP.keys())
        actual_headers = list(ZHI_BIAO_FIELD_MAP.values())

    summary = defaultdict(float)
    numeric_fields = []
    for k in actual_headers:
        for item in data_list:
            v = item.get(k)
            try:
                if v is not None and v != '' and v != 'undefined':
                    float(v)
                    numeric_fields.append(k)
                    break
            except Exception:
                continue

    markdown = f"| {' | '.join(display_headers)} |\n"
    markdown += f"| {' | '.join(['---'] * len(display_headers))} |\n"

    for item in data_list:
        row = []
        for header in actual_headers:
            value = item.get(header, '')
            if header in numeric_fields:
                try:
                    summary[header] += float(value) if value not in (None, '', 'undefined') else 0.0
                except Exception:
                    pass
            row.append(str(value))
        markdown += f"| {' | '.join(row)} |\n"

    summary_row = []
    for header in actual_headers:
        if header in numeric_fields:
            summary_row.append(f"{summary[header]: .2f}")
        else:
            summary_row.append('汇总' if header == 'groupKey' else '')
    markdown += f"| {' | '.join(summary_row)} |\n"

    return markdown, summary


# 从命令行获取token
@mcp.tool()
def get_ad_material_list(
        version: str = "0.1.87",
        appid: str = "59",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        zhibiao_list: Optional[List[str]] = None,
        media: Optional[List[str]] = None,
        self_cid: Optional[List[str]] = None,
        toushou: Optional[List[str]] = None,
        component_id: Optional[List[str]] = None,
        vp_adgroup_id: Optional[List[str]] = None,
        creative_id: Optional[List[str]] = None,
        group_key: Optional[str] = None,
        producer: Optional[List[str]] = None,
        creative_user: Optional[List[str]] = None,
        vp_originality_id: Optional[List[str]] = None,
        vp_originality_name: Optional[List[str]] = None,
        vp_originality_type: Optional[List[str]] = None,
        is_inefficient_material: AdQualityOption = AdQualityOption.DEFAULT,
        is_ad_low_quality_material: AdQualityOption = AdQualityOption.DEFAULT
) -> dict:
    """
    ## get_ad_material_list工具说明
    当用户需要分析广告素材数据时，你需要调用此MCP工具'get_ad_material_list'来查询广告素材数据。
    该工具可以获取广告投放的各类指标数据，支持多种筛选和分组方式，并将结果转换为Markdown表格格式，
    在调用此工具获取数据的过程中，需要先通过此工具将获取到的数据处理成Markdown表格的形式，再根据此表格进行输出回答分析，不得添加任何未出现在表中的信息。
    注意：转换为markdown表格为中间处理过程，并非输出过程，例如：在调用工具后可能会获得以下字段：
      "list": [
        {
          "accumulatedPayUser": 0,
          "adBuyUsers": "0",
          "cost": 0.71,
          "groupKey": "20250516-正统三国-蔡睿韬-HB-蔡睿韬-黄月英",
          "newPayMoney": 0,
          "payMoney": 0,
          "regRoleCount": 0,
          "regUserCount": 4,
          "show_video_uris": "https://txgamecdn.dartou.com/dartou/bi/352/20250516-正统三国-蔡睿韬-HB-蔡睿韬-黄月英.mp4",
          "show_vp_originality_id": "19006381271"
        },
        {
          "accumulatedPayUser": 0,
          "adBuyUsers": "0",
          "cost": 0,
          "groupKey": "20250418-正统三国-郑显洋-SB-郑显洋-2",
          "newPayMoney": 0,
          "payMoney": 0,
          "regRoleCount": 0,
          "regUserCount": 0,
          "show_video_uris": "https://txgamecdn.dartou.com/dartou/bi/89/20250418-正统三国-郑显洋-SB-郑显洋-2.mp4",
          "show_vp_originality_id": "18135653547"
        },
        ...
     ]
    需要将所有"list"列表中的数据转换为markdown表格，例如将上述示例转换为markdown表格的结果为：
    | Group Key                                 | Accumulated Pay User | Ad Buy Users | Cost | New Pay Money | Pay Money | Reg Role Count | Reg User Count | Show Video URIs                                              | Show VP Originality ID |
| ----------------------------------------- | -------------------- | ------------ | ---- | ------------- | --------- | -------------- | -------------- | ------------------------------------------------------------ | ---------------------- |
| 20250516-正统三国-蔡睿韬-HB-蔡睿韬-黄月英 | 0                    | 0            | 0.71 | 0             | 0         | 0              | 4              | https://txgamecdn.dartou.com/dartou/bi/352/20250516-正统三国-蔡睿韬-HB-蔡睿韬-黄月英.mp4 | 19006381271            |
| 20250418-正统三国-郑显洋-SB-郑显洋-2      | 0                    | 0            | 0    | 0             | 0         | 0              | 0              | https://txgamecdn.dartou.com/dartou/bi/89/20250418-正统三国-郑显洋-SB-郑显洋-2.mp4 | 18135653547            |

注意：以上格式中的数据仅供参考，具体以实际查询到的数据为准。

    ### 参数详情

    调用函数时需要提供以下参数，除了必填参数之外，其他参数如果用户没有说明，则使用默认值

    1、**version**（必填，字符串）
        - 系统版本，默认值："0.1.87"

    2、**appid**（选填，字符串）
        - 游戏ID，默认值："59"（正统三国）

    3、**start_time**（必填，字符串）
        - 开始时间，格式：YYYY-MM-DD
        - 例如 "2023-01-01"
        - 注意：如果只查询一天数据，start_time和end_time需设为同一天

    4、**end_time**（必填，字符串）
        - 结束时间，格式：YYYY-MM-DD
        - 例如："2023-01-01"
        - 注意：如果只查询一天数据，start_time和end_time需设为同一天

    5、**zhibiao_list**（必填，字符串数组）
        - [“日期“]必须包含在指标内，其他参数选填，如果用户未指定zhibiao_list入参，则默认入参所有指标。
        - 需要查询的指标列表
        - 不指定时默认查询所有51个指标
        - 例如：["日期", "创角成本", "新增创角"]

    6. **media** (选填，字符串数组)
        - 媒体列表，默认为空
        - 可选值：全选(全选)、sphdr(视频号达人)、bd(百度)、xt(星图)、bdss(百度搜索)、gdt(广点通)、bz(b站)、zh(知乎)、dx(抖小广告量)、tt(今日头条)、uc(uc)、gg(谷歌)、nature(自然量)
        - 例如：["gdt"] 表示查询广点通

    7. **self_cid** (选填，字符串数组)
        - 广告cid，默认为空
        - 例如：["ztsg_gdt_zp_3006", "ztsg_gdt_syf_02"]

    8. **toushou** (选填，字符串数组)
        - 投手列表，默认为空
        - 可选值：lll(李霖林)、dcx(戴呈翔)、yxr(尹欣然)、syf(施逸风)、gyy(郭耀月)、zp(张鹏)、zmn(宗梦男)
        - 例如：["lll"] 表示查询李霖林的投放数据

    9、**component_id**（选填，字符串数组）
        - 组件id，默认为空

    10、**vp_adgroup_id**（选填，字符串数组）
        - 计划id，默认为空
        - 例如：["0", "159842"]

    11、**creative_id**（选填，字符串数组）
        - 创意id，默认为空
        - 例如：["12", "87"]

    12. **group_key** (选填，字符串)
        - 分组键，默认为空
        - 可选值：vp_advert_pitcher_id(投手)、dt_vp_fx_cid(self_cid)、vp_adgroup_id(项目id)、vp_advert_channame(媒体)、vp_campaign_id(广告id)、vp_originality_id(创意id)
        - 例如："vp_campaign_id" 表示按广告ID分组

    13、**producer**（选填，字符串数组）
        - 制作人，默认为空
        - 可选值：蔡睿韬、王子鹏、颜隆隆、郑显洋、李霖林、张鹏、谢雨、占雪涵、方晓聪、刘伍攀、张航、刘锦、翁国峻、刘婷婷、张泽祖、戴呈翔、AI、其他
        - 例如：["蔡睿韬"]表示制作人为蔡睿韬

    14、**creative_user**（选填，字符串数组）
        - 创意人，默认为空
        - 可选值：蔡睿韬、王子鹏、颜隆隆、郑显洋、李霖林、张鹏、谢雨、占雪涵、方晓聪、刘伍攀、张航、刘锦、翁国峻、刘婷婷、张泽祖、戴呈翔、AI、其他
        - 例如：["张鹏"]表示创意人为张鹏

    15、**vp_originality_id**（选填，字符串数组）
        - 素材id，默认为空
        - 例如：["7498289972262535194"]

    16、**vp_originality_name**（选填，字符串数组）
        - 素材名，默认为空
        - 例如：["20250428-正统三国-王子鹏-SB-王子鹏-地域优势-3"]

    17、**vp_originality_type**（选填，字符串数组）
        - 素材类型，默认为空
        - 可选值：图片、视频
        - 例如：["视频"]

    18、**is_inefficient_material**（选填，integer）
        - 低效素材，默认为-1
        - 可选值：-1，1，2
        - 其中-1表示全选，1表示是，2表示否

    19、**is_ad_low_quality_material**（选填，integer）
        - AD优/低质，默认为-1
        - 可选值：-1，1，2
        - 其中-1表示全选，1表示是，2表示否

特别注意：所有列表类型参数必须使用正确的JSON数组格式，例如：

- 正确：["创角成本", "新增创角"]

- 错误："创角成本,新增创角"

媒体参数必须使用规定的代码而非中文名称：

- 正确：["gdt"]（代表广点通）

- 错误：["广点通"]

### 调用入参示例

# 查询2025年1月1日至1月31日广点通渠道的创角成本、新增创角和点击率

    version="0.1.85",

    appid="59",

    start_time="2025-01-01",

    end_time="2025-01-31",

    zhibiao_list=["日期", "创角成本", "新增创角", "点击率"],

    media=["gdt"]

# 查询某一天李霖林投手的所有广告数据

    version="0.1.87",

    start_time="2025-06-24",

    end_time="2025-06-24",

    toushou=["lll"]

## 重要提示

1. 如果用户没有指定指标要求，将默认显示全部指标。
2. 如果用户只查询一天的数据，需要把开始时间和结束时间都设为同一天。
3. 多个筛选条件可以组合使用，如媒体+投手、广告ID+状态等。
4. 确保数据的准确性，如未查询到数据，需如实回答，不要胡编乱造。
5. 转换为markdown表格为中间处理过程，需要在查询到数据后立即执行，而不是在输出回答的过程中执行，除非用户明确要求需要图表分析数据。
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
    # 构建请求体前，zhibiao_list直接作为API请求体字段
    if zhibiao_list:
        payload_zhibiao_list = zhibiao_list
    else:
        payload_zhibiao_list = list(ZHI_BIAO_FIELD_MAP.values())

    # API接口地址
    url = "https://bi.dartou.com/testapi/ad/GetMaterialCountList"

    # 设置请求头
    headers = {
        "X-Token": token,
        "X-Ver": version,
        "Content-Type": "application/json"
    }

    # 构建请求体
    # 构建请求体
    payload = {
        "appid": appid,
        "start_time": start_time,
        "end_time": end_time,
        "zhibiao_list": payload_zhibiao_list,
        "media": media,
        "self_cid": self_cid,
        "toushou": toushou,
        "component_id": component_id,
        "vp_adgroup_id": vp_adgroup_id,
        "creative_id": creative_id,
        "group_key": group_key,
        "producer": producer,
        "creative_user": creative_user,
        "vp_originality_id": vp_originality_id,
        "vp_originality_name": vp_originality_name,
        "vp_originality_type": vp_originality_type,
        "is_ad_low_quality_material": is_ad_low_quality_material.value,
        "is_inefficient_material": is_inefficient_material.value
    }

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 解析响应
        result = response.json()

        # 检查响应状态
        if result.get("code") == 0:
            print("请求成功!")
            data_list = result.get("data", {}).get("list", [])
            if data_list:
                markdown_table, summary_stats = generate_markdown_table(data_list, zhibiao_list=zhibiao_list)

                print("接口原始响应:", result)
                print("转换后的Markdown表格:\n", markdown_table)
                return {
                    "code": 0,
                    "msg": "查询成功",
                    "markdown_table": markdown_table,
                    "summary_stats": summary_stats,
                }
            else:
                print("未查询到数据")
                return {"code": 0, "msg": "未查询到数据", "markdown_table": "", "summary_stats": {}}
        else:
            return {
                "code": result.get("code"),
                "msg": result.get("msg"),
                "markdown_table": "",
                "summary_stats": {}
            }

    except Exception as e:
        return {
            "code": -1,
            "msg": str(e),
            "markdown_table": "",
            "summary_stats": {}
        }


def main() -> None:
    mcp.run(transport="stdio")

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


def generate_markdown_table(data_list: List[dict]) -> tuple[str, dict]:
    """
    将数据列表转换为Markdown表格格式，并对数值型字段进行汇总统计。

    Args:
        data_list: API返回的数据列表

    Returns:
        tuple: (Markdown表格字符串, 汇总统计字典)
    """
    if not data_list:
        return "无数据可生成表格", {}

    # 获取所有可能的字段（表头）
    headers = set()
    for item in data_list:
        headers.update(item.keys())
    headers = sorted(headers)  # 按字母顺序排序表头

    # 初始化汇总统计字典
    summary = defaultdict(float)
    numeric_fields = [
        'accumulatedPayUser', 'adBuyUsers', 'clickScale', 'cost',
        'createRoleScale', 'groupKey', 'newPayMoney', 'payMoney',
        'regRoleCount', 'regUserCount', 'show_video_uris', 'show_vp_originality_id'
    ]

    # 构建Markdown表格
    markdown = f"| {' | '.join(headers)} |\n"
    markdown += f"| {' | '.join(['---'] * len(headers))} |\n"

    # 填充表格数据并统计
    for item in data_list:
        row = []
        for header in headers:
            value = item.get(header, '')
            row.append(str(value))
            # 对数值型字段进行汇总
            if header in numeric_fields and isinstance(value, (int, float)):
                summary[header] += value
        markdown += f"| {' | '.join(row)} |\n"

    # 添加汇总行
    summary_row = []
    for header in headers:
        if header in summary:
            summary_row.append(f"{summary[header]: .2f}")
        else:
            summary_row.append('汇总' if header == 'groupKey' else '')
    markdown += f"| {' | '.join(summary_row)} |\n"

    return markdown, dict(summary)


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
    在调用此工具获取数据的过程中，需要先通过此工具将获取到的数据处理成Markdown表格的形式，再根据此表格进行输出回答分析。
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

    version="0.1.85",

    start_time="2025-06-24",

    end_time="2025-06-24",

    toushou=["lll"]

## 重要提示

1. 如果用户没有指定指标要求，将默认显示全部51个指标。
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
    if zhibiao_list is None:
        zhibiao_list = ["日期", "素材id", "素材名称", "素材类型", "素材封面uri", "制作人", "创意人", "素材创造时间",
                        "3秒播放率", "完播率", "是否低效素材", "是否AD低质素材", "是否AD优质素材", "低质原因",
                        "新增注册", "新增创角", "创角率", "点击率", "激活率", "点击成本", "活跃用户", "当日充值",
                        "当日付费次数", "当日充值人数", "新增付费人数", "首充付费人数", "新增付费金额", "首充付费金额",
                        "新增付费率", "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额",
                        "小游戏注册首日广告变现ROI", "新增付费成本", "消耗", "付费成本", "注册成本", "创角成本",
                        "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI"]

    # API接口地址
    url = "https://bi.dartou.com/testapi/ad/GetMaterialCountList"

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
                markdown_table, summary_stats = generate_markdown_table(data_list)
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

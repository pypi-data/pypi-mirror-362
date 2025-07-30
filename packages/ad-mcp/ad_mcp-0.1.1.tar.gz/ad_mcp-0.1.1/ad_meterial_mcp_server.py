from mcp.server.fastmcp import FastMCP
import requests
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Optional

parser = argparse.ArgumentParser(description='广告数据查询MCP服务')
parser.add_argument('--token', type=str, required=True, help='API访问token')
args = parser.parse_args()

mcp = FastMCP("广告素材查询服务")


def get_token_from_config():
    if args.token:
        return args.token
    else:
        raise ValueError("必须提供命令参数--token")


@mcp.tool()
def get_ad_count_list(
        version: str = "0.1.77",
        appid: str = "59",
        zhibiao_list: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        media: Optional[List[str]] = None,
        toushou: Optional[List[str]] = None,
        group_key: Optional[str] = None,
        self_cid: Optional[List[str]] = None,
        producer: Optional[List[str]] = None,
        creative_user: Optional[List[str]] = None,
        vp_originality_id: Optional[List[str]] = None,
        vp_adgroup_id: Optional[List[str]] = None,
        vp_originality_name: Optional[List[str]] = None,
        vp_originality_type: Optional[List[str]] = None,
        is_inefficient_material: int = -1,
        is_ad_low_quality_material: int = -1,
        is_deep: bool = False,
        is_old_table: bool = False,
        component_id: Optional[List[str]] = None,
        creative_id: Optional[List[str]] = None
) -> dict:
    """
    广告数据相关功能，包括查询广告数据、获取指标列表、如果用户只查询一天，需要把开始时间和结束时间都设为同一天
    token: 请求token
    version: 系统版本
         appid: 游戏ID，默认为"59"（正统三国）
         zhibiao_list: 指标
         start_time: 范围查询开始时间, 格式：YYYY-MM-DD
         end_time: 范围查询结束时间，格式：YYYY-MM-DD
         media: 媒体，查询广点通媒体：["gdt"]
         toushou: 投手
         group_key: 分组，默认按素材名称分组
         self_cid: 广告账户id
         producer: 制作人
         creative_user: 创意人
         vp_originality_id: 素材id
         vp_adgroup_id: 计划id
         vp_originality_name: 素材名
         vp_originality_type: 素材类型
         is_inefficient_material: 低效素材：取值-1（全选），1（是），2（否）
         is_ad_low_quality_material: AD优/低质：取值-1（全选），1（低质），2（优质）
         is_deep: 下探：取值：true（是），false（否）
         is_old_table: 旧报表：取值true（是），false（否），当media中包含gdt（广点通）时可选
         component_id: 组件id
         creative_id: 创意id
        :return: dict，API响应数据和配置数据
        """

    token = get_token_from_config()

    if start_time is None:
        yesterday = datetime.now() - timedelta(days=1)
        start_time = yesterday.strftime("%Y-%m-%d")

    if end_time is None:
        end_time = datetime.now().strftime("%Y-%m-%d")
    if zhibiao_list is None:
        zhibiao_list = [
            "日期", "素材名称", "素材id", "素材类型", "素材封面uri", "制作人", "创意人",
            "素材创造时间", "3秒播放率", "完播率", "是否低效素材", "是否AD低质素材",
            "是否AD优质素材", "低质原因", "新增注册", "新增创角", "创角率", "点击率",
            "激活率", "点击成本", "活跃用户", "当日充值", "当日付费次数", "当日充值人数",
            "新增付费人数", "首充付费人数", "新增付费金额", "首充付费金额", "新增付费率",
            "活跃付费率", "活跃arppu", "新增arppu", "小游戏注册首日广告变现金额",
            "小游戏注册首日广告变现ROI", "新增付费成本", "消耗", "付费成本", "注册成本",
            "创角成本", "首日ROI", "累计ROI", "分成后首日ROI", "分成后累计ROI"
        ]

    url = "https://bi.dartou.com/testapi/ad/GetMaterialCountList"
    headers = {
        "X-Token": token,
        "X-Ver": version,
        "Content-Type": "application/json"
    }
    payload = {
        "appid": appid,
        "zhibiao_list": zhibiao_list,
        "start_time": start_time,
        "end_time": end_time,
        "media": media,
        "toushou": toushou,
        "group_key": group_key,
        "self_cid": self_cid,
        "producer": producer,
        "creative_user": creative_user,
        "vp_originality_id": vp_originality_id,
        "vp_adgroup_id": vp_adgroup_id,
        "vp_originality_name": vp_originality_name,
        "vp_originality_type": vp_originality_type,
        "is_inefficient_material": is_inefficient_material,
        "is_ad_low_quality_material": is_ad_low_quality_material,
        "is_deep": is_deep,
        "is_old_table": is_old_table,
        "component_id": component_id,
        "creative_id": creative_id
    }

    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        result = response.json()
        if result.get("code") == 0:
            print("请求成功")
            return result
        else:
            print(f"请求失败：{result.get('msg')}")
            return result
    except Exception as e:
        print(f'error: {str(e)}')
        return {"code": -1, "msg": str(e)}

    # 兜底，理论不会走到这里
    return {"code": -1, "msg": "未知错误"}


if __name__ == '__main__':
    print("启动广告素材查询MCP服务...")
    mcp.run(transport='stdio')

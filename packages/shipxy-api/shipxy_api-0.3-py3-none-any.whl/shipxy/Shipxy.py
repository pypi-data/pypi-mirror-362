from typing import List

from pydantic import BaseModel

from shipxy.BaseMethon import postMethodJson, getMethodJson
from shipxy.ResponseObj import SearchShipResponse, SingleShipResponse, ManyShipResponse, FleetShipResponse, \
    SurRoundingShipResponse, AreaShipResponse, ShipRegistryResponse, SearchShipParticularResponse, SearchPortResponse, \
    GetBerthShipsResponse, GetAnchorShipsResponse, GetETAShipsResponse, GetShipTrackResponse, \
    SearchShipApproachResponse, GetPortOfCallByShipResponse, GetPortOfCallByShipPortResponse, GetShipStatusResponse, \
    GetPortOfCallByPortResponse, PlanRouteByPointResponse, PlanRouteByPortResponse, GetSingleETAPreciseResponse, \
    GetWeatherResponse, GetWeatherByPointResponse, GetAllTyphoonResponse, GetSingleTyphoonResponse, GetTidesResponse, \
    GetTideDataResponse, GetNavWarningResponse, FleetResponse, BaseResponse, AreaResponse


def SearchShip(key: str, keywords: str, max: int = 100) -> SearchShipResponse:
    """
    * 1船舶查询-1.1船舶模糊查询
    * https://hiiau7lsqq.feishu.cn/wiki/VCSYw1FU3iP0zwk2IIFcf2oynPb
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param keywords: 关键字：必填，船舶查询的输入关键字，可以是船名、呼号、MMSI、IMO 等；匹配原则：MMSI 为 9 位数, IMO 为 7 位数
    :param max: 最大返回数量：选填，最多返回的结果数量，该值最大 100
    :return:
    """
    params = {
        "key": key,
        "keywords": keywords,
        "max": max
    }
    response = postMethodJson("/SearchShip", params)
    return SearchShipResponse(**response)


def GetSingleShip(key: str, mmsi: int) -> SingleShipResponse:
    """
    * 1船舶查询-1.2船舶位置查询-单船位置查询
    * https://hiiau7lsqq.feishu.cn/wiki/GxF2w6cZHisQiEkBRatcoIqlnfc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：必填，船舶mmsi编号，9 位数字
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
    }
    response = getMethodJson("/GetSingleShip", params)
    return SingleShipResponse(**response)


def GetManyShip(key: str, mmsis: str) -> ManyShipResponse:
    """
    * 1船舶查询-1.2船舶位置查询-多船位置查询
    * https://hiiau7lsqq.feishu.cn/wiki/GxF2w6cZHisQiEkBRatcoIqlnfc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsis: 船舶mmsi编号：必填，船舶编号，船舶mmsi编号，多船查询以英文逗号隔开，单次查询船舶数量不超过100
    :return:
    """
    params = {
        "key": key,
        "mmsis": mmsis,
    }
    response = getMethodJson("/GetManyShip", params)
    return ManyShipResponse(**response)


def GetFleetShip(key: str, fleet_id: str) -> FleetShipResponse:
    """
    * 1船舶查询-1.2船舶位置查询-船队船位置查询
    * https://hiiau7lsqq.feishu.cn/wiki/GxF2w6cZHisQiEkBRatcoIqlnfc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队编号：必填，控制台中维护的船队id，查询船队下所有船舶数据。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
    }
    response = getMethodJson("/GetFleetShip", params)
    return FleetShipResponse(**response)


def GetSurRoundingShip(key: str, mmsi: int) -> SurRoundingShipResponse:
    """
    * 1船舶查询-1.3周边船舶查询
    * https://hiiau7lsqq.feishu.cn/wiki/XXTiwDpetivSFhkciWic6qarnOc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：必填，船舶mmsi编号，9 位数字
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
    }
    response = getMethodJson("/GetSurRoundingShip", params)
    return SurRoundingShipResponse(**response)


def GetAreaShip(key: str, region: str, output: int = 1, scode: int = None) -> AreaShipResponse:
    """
    * 1船舶查询-1.4区域船舶查询
    * https://hiiau7lsqq.feishu.cn/wiki/ZlcrwKpgqik1L3kvbIMcBJUCn1U
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param region: 查询区域：必填，经纬度逗号分隔，多个点减号分隔，如： （lng,lat - lng,lat ）经纬度数，多个经纬度坐标点必须按照顺时针或逆时针依次输入。
    :param output: 输出格式：选填，输出数据格式类型选择：0为二进制 Base64 编码，1为json格式，默认为1
    :param scode: 会话令牌：选填，当区域范围船舶单次请求无法全部返回时，可以根据首次请求返回的scode再次请求剩余的数据，保证全部返回。
    :return:
    """
    params = {
        "key": key,
        "region": region,
        "output": output,
        "scode": scode
    }
    response = getMethodJson("/GetAreaShip", params)
    return AreaShipResponse(**response)


def GetShipRegistry(key: str, mmsi: int) -> ShipRegistryResponse:
    """
    * 1船舶查询-1.5船舶船籍查询
    * https://hiiau7lsqq.feishu.cn/wiki/Ko5gw1o0ZiMQankWEAscSMoin7g
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：必填，船舶mmsi编号，9 位数字
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
    }
    response = getMethodJson("/GetShipRegistry", params)
    return ShipRegistryResponse(**response)


def SearchShipParticular(key: str, mmsi: int = None, imo: int = None, call_sign: str = None,
                         ship_name: str = None) -> SearchShipParticularResponse:
    """
    * 1船舶查询-1.6船舶档案查询
    * https://hiiau7lsqq.feishu.cn/wiki/Vvd2wHECliYz6okSoYucTRXvnsd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param kwargs: 可变参数
    :param mmsi: 船舶mmsi编号：非必填，船舶mmsi编号，9位数字。请求时船舶mmsi编号、imo、呼号、名称必填一项，全部不填则请求失败。
    :param imo: imo编号：非必填，船舶imo编号
    :param call_sign: 船舶呼号：非必填，船舶呼号，如果不同船舶的呼号相同，则相同呼号档案都将返回
    :param ship_name: 船舶名称：非必填，船舶英文名称，如果不同船舶的名称相同，则同名船舶的档案都将返回
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "imo": imo,
        "call_sign": call_sign,
        "ship_name": ship_name
    }
    # for key, value in kwargs.items():
    #     params[key] = value
    response = getMethodJson("/SearchShipParticular", params)
    return SearchShipParticularResponse(**response)


def SearchPort(key: str, keywords: str, max: int = 100) -> SearchPortResponse:
    """
    * 2港口查询-2.1港口信息查询
    * https://hiiau7lsqq.feishu.cn/wiki/DAlUwEn9Zi50gckSv0uc1qsIn6f
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param keywords: 关键字：必填，船舶查询的输入关键字，可以是船名、呼号、MMSI、IMO 等；匹配原则：MMSI 为 9 位数, IMO 为 7 位数
    :param max: 最大返回数量：选填，最多返回的结果数量，该值最大 100
    :return:
    """
    params = {
        "key": key,
        "keywords": keywords,
        "max": max
    }
    response = getMethodJson("/SearchPort", params)
    return SearchPortResponse(**response)


def GetBerthShips(key: str, port_code: str, ship_type: int = None) -> GetBerthShipsResponse:
    """
    * 2港口查询-2.2港口当前靠泊船查询
    * https://hiiau7lsqq.feishu.cn/wiki/KdBNwIxOhijpALkCkNXc69MKn3g
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param port_code: 港口标准code：必填，港口标准五位码
    :param ship_type: 船舶类型：选填，筛选船舶的类型，船舶类型清单请参考文档，不填写时返回全部船舶。
    :return:
    """
    params = {
        "key": key,
        "port_code": port_code,
        "ship_type": ship_type
    }
    response = getMethodJson("/GetBerthShips", params)
    return GetBerthShipsResponse(**response)


def GetAnchorShips(key: str, port_code: str, ship_type: int = None) -> GetAnchorShipsResponse:
    """
    * 2港口查询-2.3港口当前到锚船舶查询
    * https://hiiau7lsqq.feishu.cn/wiki/WTHnwa66niA4VhkmNVXchRRSnYe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param port_code: 港口标准code：必填，港口标准五位码
    :param ship_type: 船舶类型：选填，筛选船舶的类型，船舶类型清单请参考文档，不填写时返回全部船舶。
    :return:
    """
    params = {
        "key": key,
        "port_code": port_code,
        "ship_type": ship_type
    }
    response = getMethodJson("/GetAnchorShips", params)
    return GetAnchorShipsResponse(**response)


def GetETAShips(key: str, port_code: str, start_time: int, end_time: int, ship_type: int = None) -> GetETAShipsResponse:
    """
    * 2港口查询-2.4港口预抵船舶查询
    * https://hiiau7lsqq.feishu.cn/wiki/Poe3wdXkwiwzMUkATcJcigeBnJh
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param port_code: 港口标准code：必填，港口标准五位码
    :param start_time: 开始时间：必填，开始时间，utc时间戳。开始时间必须大于当前时间
    :param end_time: 结束时间：必填，结束时间，utc时间戳。单次请求查询中，开始时间和结束时间的间隔不超过1周。
    :param ship_type: 船舶类型：选填，筛选船舶的类型，船舶类型清单请参考文档，不填写时返回全部船舶。
    :return:
    """
    params = {
        "key": key,
        "port_code": port_code,
        "start_time": start_time,
        "end_time": end_time,
        "ship_type": ship_type
    }
    response = getMethodJson("/GetETAShips", params)
    return GetETAShipsResponse(**response)


def GetShipTrack(key: str, mmsi: int, start_time: int, end_time: int, output: int = 1) -> GetShipTrackResponse:
    """
    * 3历史行为-3.1船舶历史轨迹查询
    * https://hiiau7lsqq.feishu.cn/wiki/RK2Uwh7tziQ7SnkzlDgcUk8Nnkc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶编号：必填，船舶mmsi编号
    :param start_time: 开始时间：必填，查询的开始时间，unix时间戳
    :param end_time: 结束时间：必填，查询的截止时间，unix时间戳
    :param output: 输出格式：选填，输出数据格式类型选择：0为二进制 Base64 编码，1为json格式，默认为1。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "start_time": start_time,
        "end_time": end_time,
        "output": output
    }
    response = getMethodJson("/GetShipTrack", params)
    return GetShipTrackResponse(**response)


def SearchshipApproach(key: str, mmsi: int, start_time: int, end_time: int,
                       approach_zone: int = None) -> SearchShipApproachResponse:
    """
    * 3历史行为-3.2船舶搭靠记录查询
    * https://hiiau7lsqq.feishu.cn/wiki/GYrTwxfzRiQdDxkJYOWcF3kKnnf
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶编号：必填，船舶mmsi编号，9 位数字
    :param start_time: 开始时间：必填，开始时间，utc时间戳。
    :param end_time: 结束时间：必填，结束时间，utc时间戳。单次请求查询中，开始时间和结束时间的间隔不超过1个月。
    :param approach_zone: 搭靠地区：选填，1代表港口地区搭靠；2代表锚地搭靠；3代表其他地点搭靠；不填写返回全部。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "start_time": start_time,
        "end_time": end_time,
        "approach_zone": approach_zone
    }
    response = getMethodJson("/SearchshipApproach", params)
    return SearchShipApproachResponse(**response)


def GetPortofCallByShip(key: str, mmsi: int, start_time: int, end_time: int, imo: int = None, ship_name: str = None,
                        call_sign: str = None,
                        time_zone: int = 2) -> GetPortOfCallByShipResponse:
    """
    * 4挂靠记录-4.1船舶历史挂靠记录
    * https://hiiau7lsqq.feishu.cn/wiki/Sv5rw61KVioV0ekq4ytcBpGgnGd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：非必填，船舶mmsi编号，9位数字。请求时船舶mmsi编号、imo、呼号、名称必填一项，全部不填则请求失败。
    :param imo: imo编号：非必填，船舶imo编号
    :param ship_name: 船舶名称：非必填，船舶英文名称，如果不同船舶的名称相同，则同名船舶的档案都将返回
    :param call_sign: 船舶呼号：非必填，船舶呼号，如果不同船舶的呼号相同，则相同呼号档案都将返回
    :param start_time: 开始时间：必填，历史靠港记录开始时间，Unix 时间戳start_time与end_time为必填项，表示查询[start_time，end_time]之间的结果，最多1次只能查询1年（366天）的靠港记录.
    :param end_time: 结束时间：必填，历史靠港记录结束时间，unix 时间戳。
    :param time_zone: 时区：选填，时间类型(选填)。 1当地时区，如果不存在，使用零时区；2北京时区；3零时区，即格林尼治平均时。默认值：2。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "imo": imo,
        "ship_name": ship_name,
        "call_sign": call_sign,
        "start_time": start_time,
        "end_time": end_time,
        "time_zone": time_zone
    }
    response = getMethodJson("/GetPortofCallByShip", params)
    return GetPortOfCallByShipResponse(**response)


def GetPortofCallByShipPort(key: str, mmsi: int, port_code: str,
                            start_time: int, end_time: int, imo: int = None, ship_name: str = None,
                            call_sign: str = None,
                            time_zone: int = 2) -> GetPortOfCallByShipPortResponse:
    """
    * 4挂靠记录-4.2船舶挂靠指定港口记录
    * https://hiiau7lsqq.feishu.cn/wiki/R01xw8GxYiPd08kGhDeckVojnSC
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：非必填，船舶mmsi编号，9位数字。请求时船舶mmsi编号、imo、呼号、名称必填一项，全部不填则请求失败。
    :param imo: imo编号：非必填，船舶imo编号
    :param ship_name: 船舶名称：非必填，船舶英文名称，如果不同船舶的名称相同，则同名船舶的档案都将返回
    :param call_sign: 船舶呼号：非必填，船舶呼号，如果不同船舶的呼号相同，则相同呼号档案都将返回
    :param port_code: 港口标准code：必填，港口标准五位码
    :param start_time: 开始时间：必填，历史靠港记录开始时间，Unix 时间戳start_time与end_time为必填项，表示查询[start_time，end_time]之间的结果，最多1次只能查询1年（366天）的靠港记录.
    :param end_time: 结束时间：必填，历史靠港记录结束时间，unix 时间戳。
    :param time_zone: 时区：选填，时间类型(选填)。 1当地时区，如果不存在，使用零时区；2北京时区；3零时区，即格林尼治平均时。默认值：2。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "imo": imo,
        "ship_name": ship_name,
        "call_sign": call_sign,
        "port_code": port_code,
        "start_time": start_time,
        "end_time": end_time,
        "time_zone": time_zone
    }
    response = getMethodJson("/GetPortofCallByShipPort", params)
    return GetPortOfCallByShipPortResponse(**response)


def GetShipStatus(key: str, mmsi: int, imo: int = None, ship_name: str = None, call_sign: str = None,
                  time_zone: int = 2) -> GetShipStatusResponse:
    """
    * 4挂靠记录-4.3船舶当前挂靠信息
    * https://hiiau7lsqq.feishu.cn/wiki/O3PRwZoAjiX3DdknudicZnVpnxH
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：必填，船舶mmsi编号，9位数字。请求时船舶mmsi编号、imo、呼号、名称必填一项，全部不填则请求失败。
    :param imo: imo编号：非必填，船舶imo编号
    :param ship_name: 船舶名称：非必填，船舶英文名称，如果不同船舶的名称相同，则同名船舶的档案都将返回
    :param call_sign: 船舶呼号：非必填，船舶呼号，如果不同船舶的呼号相同，则相同呼号档案都将返回
    :param time_zone: 时区：选填，时间类型(选填)。 1当地时区，如果不存在，使用零时区；2北京时区；3零时区，即格林尼治平均时。默认值：2。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "imo": imo,
        "ship_name": ship_name,
        "call_sign": call_sign,
        "time_zone": time_zone
    }
    response = getMethodJson("/GetShipStatus", params)
    return GetShipStatusResponse(**response)


def GetPortofCallByPort(key: str, port_code: str, start_time: int, end_time: int, type: int = 1,
                        time_zone: int = 2) -> GetPortOfCallByPortResponse:
    """
    * 4挂靠记录-4.4港口挂靠历史船舶
    * https://hiiau7lsqq.feishu.cn/wiki/G9BDwzNPqiXdyckzFrBctxYUnHd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param port_code: 港口标准code：必填，港口标准五位码
    :param start_time: 开始时间：必填，历史靠港记录开始时间，Unix 时间戳start_time与end_time为必填项，表示查询[start_time，end_time]之间的结果，最多1次只能查询1年（366天）的靠港记录.
    :param end_time: 结束时间：必填，历史靠港记录结束时间，unix 时间戳。
    :param type: 查询类型：选填，查询类型（选填）。1，按照ATA（到港时间）查询；2，按照ATD（离港时间）查询。默认值：1
    :param time_zone: 时区：选填，时间类型(选填)。 1当地时区，如果不存在，使用零时区；2北京时区；3零时区，即格林尼治平均时。默认值：2。
    :return:
    """
    params = {
        "key": key,
        "port_code": port_code,
        "start_time": start_time,
        "end_time": end_time,
        "type": type,
        "time_zone": time_zone
    }
    response = getMethodJson("/GetPortofCallByPort", params)
    return GetPortOfCallByPortResponse(**response)


def PlanRouteByPoint(key: str, start_point: str, end_point: str, avoid: str = None,
                     through: str = None) -> PlanRouteByPointResponse:
    """
    * 5航线规划-5.1点到点航线规划
    * https://hiiau7lsqq.feishu.cn/wiki/A3UBwJ7pViozTskSFwPcJ4Ldnze
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param start_point: 起始点：必填，出发的位置点，lng,lat
    :param end_point: 结束点：必填，到达的位置点，lng,lat
    :param avoid: 绕航节点：非必填，需要避让的节点，id详见附录7 。绕航多节点时，不同id之间使用逗号分隔；不填则不绕航；一次请求绕航的节点控制在10个以内。
    :param through: 查询类型：非必填，必经的点，lng,lat - lng,lat；多点之间用“-”连接；不填则不必经；一次请求途经的节点控制在30个以内。
    :return:
    """
    params = {
        "key": key,
        "start_point": start_point,
        "end_point": end_point,
        "avoid": avoid,
        "through": through,
    }
    response = getMethodJson("/PlanRouteByPoint", params)
    return PlanRouteByPointResponse(**response)


def PlanRouteByPort(key: str, start_port_code: str, end_port_code: str, avoid: str = None,
                    through: str = None) -> PlanRouteByPortResponse:
    """
    * 5航线规划-5.2港到港航线规划
    * https://hiiau7lsqq.feishu.cn/wiki/NpsbwNzWWiJRy2k79bscVljTntd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param start_port_code: 起始港：必填，出发港PortCode港口标准五位码
    :param end_port_code: 结束港：必填，到达港PortCode港口标准五位码
    :param avoid: 绕航节点：非必填，需要避让的节点，id详见附录7 。绕航多节点时，不同id之间使用逗号分隔；不填则不绕航；一次请求绕航的节点控制在10个以内。
    :param through: 查询类型：非必填，必经的点，lng,lat - lng,lat；多点之间用“-”连接；不填则不必经；一次请求途经的节点控制在30个以内。
    :return:
    """
    params = {
        "key": key,
        "start_port_code": start_port_code,
        "end_port_code": end_port_code,
        "avoid": avoid,
        "through": through
    }
    response = getMethodJson("/PlanRouteByPort", params)
    return PlanRouteByPortResponse(**response)


def GetSingleETAPrecise(key: str, mmsi: int, port_code: str, speed: float = None) -> GetSingleETAPreciseResponse:
    """
    * 5航线规划-5.3预计到达时间(ETA)查询
    * https://hiiau7lsqq.feishu.cn/wiki/NMxnw8fEHiRhrPkIpwTcovdfnOg
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param mmsi: 船舶mmsi编号：必填，船舶mmsi编号，9 位数字
    :param port_code: 港口标准code：非必填，港口标准CODE值，可以使用港口查询API获取。如果此处不填写港口，则默认查询船舶在AIS中填写的下一目的港口。
    :param speed: 设定船速：非必填，船舶在接下来的航行中维持的速度，单位：节。如果此处不填写，则默认按照船舶近一个月的平均航速来计算预计到达，平均航速是去掉在港口地区锚泊的船速信息后计算的平均值。
    :return:
    """
    params = {
        "key": key,
        "mmsi": mmsi,
        "port_code": port_code,
        "speed": speed,
    }
    response = getMethodJson("/GetSingleETAPrecise", params)
    return GetSingleETAPreciseResponse(**response)


def GetWeatherByPoint(key: str, lng: float, lat: float, weather_time: int = None) -> GetWeatherByPointResponse:
    """
    * 6气象天气-6.1单点海洋气象
    * https://hiiau7lsqq.feishu.cn/wiki/AFfAwtwc1ifij6k5JQ9c2u3hnbh
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param weather_time: 时间：非必填，utc时间，Unix时间戳。不填写则查询最近时间的气象数据。
    :param lng: 经度：必填，WGS84坐标系，格式为lng=155.2134。
    :param lat: 纬度：必填，WGS84坐标系，格式为lat=20.2134。
    :return:
    """
    params = {
        "key": key,
        "weather_time": weather_time,
        "lng": lng,
        "lat": lat,
    }
    response = getMethodJson("/GetWeatherByPoint", params)
    return GetWeatherByPointResponse(**response)


def GetWeather(key: str, weather_type: int) -> GetWeatherResponse:
    """
    * 6气象天气-6.2海区气象
    * https://hiiau7lsqq.feishu.cn/wiki/EEdPwP4kqi10qjkehH5cmK2Onwc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param weather_type: 区域类型：必填，查询区域的类型：0：全部；1：沿岸；2：近海；3：远海。
    :return:
    """
    params = {
        "key": key,
        "weather_type": weather_type,
    }
    response = getMethodJson("/GetWeather", params)
    return GetWeatherResponse(**response)


def GetAllTyphoon(key: str) -> GetAllTyphoonResponse:
    """
    * 6气象天气-6.3全球台风-获取全球台风列表
    * https://hiiau7lsqq.feishu.cn/wiki/PuWSw4Nteir49WkMccMcryjNnbp
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :return:
    """
    params = {
        "key": key,
    }
    response = getMethodJson("/GetAllTyphoon", params)
    return GetAllTyphoonResponse(**response)


def GetSingleTyphoon(key: str, typhoon_id: int) -> GetSingleTyphoonResponse:
    """
    * 6气象天气-6.3全球台风-获取单个台风信息
    * https://hiiau7lsqq.feishu.cn/wiki/PuWSw4Nteir49WkMccMcryjNnbp
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param typhoon_id: 台风序号：必填，通过查询台风列表获得
    :return:
    """
    params = {
        "key": key,
        "typhoon_id": typhoon_id
    }
    response = getMethodJson("/GetSingleTyphoon", params)
    return GetSingleTyphoonResponse(**response)


def GetTides(key: str) -> GetTidesResponse:
    """
    * 6气象天气-6.4国内港口潮汐-查询国内潮汐观测站列表
    * https://hiiau7lsqq.feishu.cn/wiki/Ayoiw98eSi0PrpkZnLnclCy8nzd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :return:
    """
    params = {
        "key": key,
    }
    response = getMethodJson("/GetTides", params)
    return GetTidesResponse(**response)


def GetTideData(key: str, port_code: str, start_date: str, end_date: str) -> GetTideDataResponse:
    """
    * 6气象天气-6.4国内港口潮汐-查询单个观测站潮汐详情
    * https://hiiau7lsqq.feishu.cn/wiki/Ayoiw98eSi0PrpkZnLnclCy8nzd
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param port_code: 潮汐观测站id：必填，港口潮汐观测站id
    :param start_date: 起始日期：必填，查询潮汐起始日期（2022-09-26），支持从2020年开始往后的历史数据查询。
    :param end_date: 结束日期：必填，查询潮汐结束日期（2022-10-03）
    :return:
    """
    params = {
        "key": key,
        "port_code": port_code,
        "start_date": start_date,
        "end_date": end_date
    }
    response = getMethodJson("/GetTideData", params)
    return GetTideDataResponse(**response)


def GetNavWarning(key: str, start_time: str, end_time: str, warning_type: int = 0) -> GetNavWarningResponse:
    """
    * 8海事数据-8.1航行警告查询
    * https://hiiau7lsqq.feishu.cn/wiki/DCgdwVip5ifCpAkQ3lfcq8OEnOc
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param start_time: 开始时间：必填，筛选航行警告发布时间。
    :param end_time: 结束时间：必填，筛选航行警告发布时间
    :param warning_type: 警告类型：非必填，警告类型筛选，默认是0，返回全部类型。1军事任务，2船舶演习，3实弹射击，4船舶作业，5航标动态，6船舶搁浅，7船舶试航，8沉没，9人员伤亡，10施工作业，11撤销航警，12其他
    :return:
    """
    params = {
        "key": key,
        "start_time": start_time,
        "end_time": end_time,
        "warning_type": warning_type
    }
    response = getMethodJson("/GetNavWarning", params)
    return GetNavWarningResponse(**response)


def AddFleet(key: str, fleet_name: str, mmsis: str, monitor: int) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-创建船队
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_name: 船队名称：必填，为您创建的船队起名，用来后续查询和区分
    :param mmsis: 船舶清单：必填，添加船队下管理的船舶信息，输入多个mmsi编号，用英文逗号隔开
    :param monitor: 监控内容：必填，选择船队进行监控的内容，1代表船队船舶查询；2代表船位实时推送；3代表船舶到离事件推送；4代表动态ETA推送；5代表AIS异常事件推送；6代表区域监控推送；7代表船舶搭靠事件推送。多选以英文逗号隔开。
    :return:
    """
    params = {
        "key": key,
        "fleet_name": fleet_name,
        "mmsis": mmsis,
        "monitor": monitor
    }
    response = postMethodJson("/AddFleet", params)
    return FleetResponse(**response)


def UpdateFleet(key: str, fleet_id: str, fleet_name: str, mmsis: str, monitor: int) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-更新船队信息
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :param fleet_name: 船队名称：非必填，输入名称则更新船队名称
    :param mmsis: 船舶清单：非必填，批量更新船队船舶信息，输入船舶mmsi编号，以英文逗号隔开。覆盖式全量更新，不做单独的增加和减少。
    :param monitor: 监控内容：非必填，变更船队进行监控的内容，1代表船队船舶查询；2代表船位实时推送；3代表船舶到离事件推送；4代表动态ETA推送；5代表AIS异常事件推送；6代表区域监控推送；7代表船舶搭靠事件推送。多选以英文逗号隔开。覆盖式全量更新，不做单独的增加和减少。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
        "fleet_name": fleet_name,
        "mmsis": mmsis,
        "monitor": monitor
    }
    response = postMethodJson("/UpdateFleet", params)
    return FleetResponse(**response)


def GetFleet(key: str, fleet_id: str) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-查询船队
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
    }
    response = getMethodJson("/GetFleet", params)
    return FleetResponse(**response)


def DeleteFleet(key: str, fleet_id: str) -> BaseResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-删除船队
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
    }
    response = postMethodJson("/DeleteFleet", params)
    return BaseResponse(**response)


def AddFleetShip(key: str, fleet_id: str, mmsis: str) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-船队船舶增加
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :param mmsis: 船舶清单：必填，添加船队管理的船舶，mmsi编号，以英文逗号隔开。增量更新，不变动原有船队船舶，输入的mmsi编号与原有重复时，新填入的不会增加到船队中。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
        "mmsis": mmsis,
    }
    response = postMethodJson("/AddFleetShip", params)
    return FleetResponse(**response)


def UpdateFleetShip(key: str, fleet_id: str, mmsis: str) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-船队船舶批量更新
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :param mmsis: 船舶清单：必填，添加船队管理的船舶，mmsi编号，以英文逗号隔开。批量覆盖原有的船舶列表，替代式更新。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
        "mmsis": mmsis,
    }
    response = postMethodJson("/UpdateFleetShip", params)
    return FleetResponse(**response)


def DeleteFleetShip(key: str, fleet_id: str, mmsis: str) -> FleetResponse:
    """
    * 9监控推送-9.1监控船队管理-设置监控船舶列表-船队船舶删除
    * https://hiiau7lsqq.feishu.cn/wiki/RtL0w0iHDioEP6kvZcScIC95nSe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param fleet_id: 船队id：必填，船队的ID，用来对船队信息进行维护的唯一标识。
    :param mmsis: 船舶清单：必填，添加船队管理的船舶，mmsi编号，以英文逗号隔开。批量覆盖原有的船舶列表，替代式更新。
    :return:
    """
    params = {
        "key": key,
        "fleet_id": fleet_id,
        "mmsis": mmsis,
    }
    response = postMethodJson("/DeleteFleetShip", params)
    return FleetResponse(**response)


def AddArea(key: str, area_bounds: str, area_name: str, url: str, filter_type: int, ship_type: str, length: str,
            fleet_id: str) -> AreaResponse:
    """
    * 9监控推送-9.4区域监控推送-区域创建
    * https://hiiau7lsqq.feishu.cn/wiki/A0hSwImnBiuKeMkkXOmcfEA9nBe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param area_bounds: 区域范围：必填，经纬度逗号分隔，多个点减号分隔，如： （lng,lat - lng,lat - lng,lat ）经纬度数，多个经纬度坐标点必须按照顺时针或逆时针依次输入。
    :param area_name: 区域名称：必填，为您创建的区域起名，用来后续查询和区分
    :param url: 推送url：必填，推送的url地址，触发监控条件时候向这个url地址推送数据。
    :param filter_type: 筛选类型：必填，区域筛选监控的类型，1代表全部船舶，2代表根据船舶类型和长度筛选匹配，3代表船队船舶。选择1的时候，不需要输入船舶类型、长度和船队id，输入也不会保存；选择2的时候，船舶类型和船舶长度为必填；选择3的时候，船队id为必填。
    :param ship_type: 船舶类型：非必填，区域监控船舶的类型，根据船舶类型筛选监控并推送，多个类型使用英文逗号隔开，不填则全选。船舶类型列表请参考开发文档附录。
    :param length:  船舶长度：非必填，区域监控船舶长度，根据船舶的长度筛选并推送，多个长度使用英文逗号隔开，不填则全选。1，代表0-40米；2，代表40-80米；3，代表80-160米；4，代表160-240米；5，代表240-320米；6，代表320米以上。
    :param fleet_id:  船队id：非必填，区域监控船队，如果只想监控某一只或一批船舶在区域的进出情况。可以创建船队，输入fleet_id则会监控船队下所有船舶。填入此参数则不会再使用ship_type监控船只，只监控船队船舶。
    :return:
    """
    params = {
        "key": key,
        "area_bounds": area_bounds,
        "area_name": area_name,
        "url": url,
        "filter_type": filter_type,
        "ship_type": ship_type,
        "length": length,
        "fleet_id": fleet_id
    }
    response = postMethodJson("/AddArea", params)
    return AreaResponse(**response)


def UpdateArea(key: str, area_id: str, area_bounds: str, area_name: str, url: str, filter_type: int, ship_type: str,
               length: str, fleet_id: str) -> AreaResponse:
    """
    * 9监控推送-9.4区域监控推送-区域更新
    * https://hiiau7lsqq.feishu.cn/wiki/A0hSwImnBiuKeMkkXOmcfEA9nBe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param area_id: 区域的ID：必填，区域的id，唯一标识，用来后续对区域的删改查
    :param area_bounds: 区域范围：必填，经纬度逗号分隔，多个点减号分隔，如： （lng,lat - lng,lat - lng,lat ）经纬度数，多个经纬度坐标点必须按照顺时针或逆时针依次输入。
    :param area_name: 区域名称：必填，为您创建的区域起名，用来后续查询和区分
    :param url: 推送url：必填，推送的url地址，触发监控条件时候向这个url地址推送数据。
    :param filter_type: 筛选类型：必填，区域筛选监控的类型，1代表全部船舶，2代表根据船舶类型和长度筛选匹配，3代表船队船舶。选择1的时候，不需要输入船舶类型、长度和船队id，输入也不会保存；选择2的时候，船舶类型和船舶长度为必填；选择3的时候，船队id为必填。
    :param ship_type: 船舶类型：非必填，区域监控船舶的类型，根据船舶类型筛选监控并推送，多个类型使用英文逗号隔开，不填则全选。船舶类型列表请参考开发文档附录。
    :param length:  船舶长度：非必填，区域监控船舶长度，根据船舶的长度筛选并推送，多个长度使用英文逗号隔开，不填则全选。1，代表0-40米；2，代表40-80米；3，代表80-160米；4，代表160-240米；5，代表240-320米；6，代表320米以上。
    :param fleet_id:  船队id：非必填，区域监控船队，如果只想监控某一只或一批船舶在区域的进出情况。可以创建船队，输入fleet_id则会监控船队下所有船舶。填入此参数则不会再使用ship_type监控船只，只监控船队船舶。
    :return:
    """
    params = {
        "key": key,
        "area_id": area_id,
        "area_bounds": area_bounds,
        "area_name": area_name,
        "url": url,
        "filter_type": filter_type,
        "ship_type": ship_type,
        "length": length,
        "fleet_id": fleet_id
    }
    response = postMethodJson("/UpdateArea", params)
    return AreaResponse(**response)


def GetArea(key: str, area_id: str) -> AreaResponse:
    """
    * 9监控推送-9.4区域监控推送-区域查询
    * https://hiiau7lsqq.feishu.cn/wiki/A0hSwImnBiuKeMkkXOmcfEA9nBe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param area_id: 区域的ID：必填，区域的id，唯一标识，用来后续对区域的删改查
    :return:
    """
    params = {
        "key": key,
        "area_id": area_id,
    }
    response = postMethodJson("/GetArea", params)
    return AreaResponse(**response)


def DeleteArea(key: str, area_id: str) -> BaseResponse:
    """
    * 9监控推送-9.4区域监控推送-区域查询
    * https://hiiau7lsqq.feishu.cn/wiki/A0hSwImnBiuKeMkkXOmcfEA9nBe
    :param key: 授权码：必填，船讯网授权码，验证服务权限
    :param area_id: 区域的ID：必填，区域的id，唯一标识，用来后续对区域的删改查
    :return:
    """
    params = {
        "key": key,
        "area_id": area_id,
    }
    response = postMethodJson("/DeleteArea", params)
    return BaseResponse(**response)

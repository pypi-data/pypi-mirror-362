from typing import List, Optional

from pydantic import BaseModel, Field

class BaseResponse(BaseModel):
    status: int = None
    msg: str = None

class SearchShipResult(BaseModel):
    match_type: int = None
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    data_source: int = None
    last_time: str = None
    last_time_utc: int = None


class SearchShipResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: List[SearchShipResult] = None


class ShipPosition(BaseModel):
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    ship_cnname: str = None  # 有些结果可能没有此字段
    data_source: int = None
    ship_type: int = None
    length: float = None
    width: float = None
    left: float = None
    trail: float = None
    draught: float = None
    dest: str = None
    destcode: str = None
    eta: str = None
    eta_utc: int = None  # 有些接口可能没有此字段
    navistat: int = None
    lat: float = None
    lng: float = None
    sog: float = None
    cog: float = None
    hdg: float = None
    rot: float = None
    last_time: str = None
    last_time_utc: int = None


class SingleShipResponse(BaseModel):
    status: int = None
    msg: str = None
    data: ShipPosition = None


class ManyShipResponse(BaseModel):
    status: int = None
    msg: str = None
    data: list[ShipPosition] = None


class FleetShipResponse(BaseModel):
    status: int = None
    msg: str = None
    data: list[ShipPosition] = None


class SurRoundingShipResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[ShipPosition] = None


class AreaShipData(BaseModel):
    total: int = None
    scode: int = None
    continue_: Optional[int] = Field(None, alias='continue')  # 使用 alias 映射字段名  # 'continue'为Python关键字，改为continue_
    ship_list: list[ShipPosition] = None


class AreaShipResponse(BaseModel):
    status: int = None
    msg: str = None
    data: AreaShipData = None


class ShipRegistryData(BaseModel):
    mmsi: int = None
    registry: str = None


class ShipRegistryResponse(BaseModel):
    status: int = None
    msg: str = None
    data: ShipRegistryData = None


class EngineInfo(BaseModel):
    designer: str = None
    powerKW: int = None


class ShipParticularData(BaseModel):
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    length: float = None
    mould_width: float = None
    flag_country_code: str = None
    flag_country: str = None
    build_country: str = None
    build_date: str = None
    class_name: str = None
    pandi_club: str = None
    ship_type: str = None
    ship_type_level5_subgroup: str = None
    ship_type_group: str = None
    ship_status: str = None
    gross_tonnage: float = None
    net_tonnage: float = None
    deadweight: float = None
    teu: int = None
    speed_max: float = None
    speed_service: float = None
    draught: float = None
    port_of_registry: str = None
    group_code: str = None
    group_company: str = None
    group_country_code: str = None
    group_country: str = None
    shipmanager_code: str = None
    shipmanager_company: str = None
    shipmanager_country_code: str = None
    shipManager_country: str = None
    operator_code: str = None
    operator_company: str = None
    operator_country_code: str = None
    operator_country: str = None
    doc_code: str = None
    doc_company: str = None
    doc_country_code: str = None
    doc_country: str = None
    registered_code: str = None
    registered_owner: str = None
    registered_country_code: str = None
    registered_country: str = None
    technical_code: str = None
    technical_manager: str = None
    technical_country_code: str = None
    technical_country: str = None
    builder_code: str = None
    builder_company: str = None
    builder_country_code: str = None
    builder_country: str = None
    update_time: str = None
    main_engine_list: list[EngineInfo] = None
    aux_engine_list: list[EngineInfo] = None


class SearchShipParticularResponse(BaseModel):
    status: int = None
    msg: str = None
    data: list[ShipParticularData] = None


class PortData(BaseModel):
    port_code: str = None
    port_name: str = None
    port_cnname: str = None
    port_time_zone: str = None
    port_country_name: str = None
    port_country_cnname: str = None
    port_country_code: str = None


class SearchPortResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[PortData] = None


class BerthShipData(BaseModel):
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    ship_type: int = None
    length: float = None
    width: float = None
    left: float = None
    trail: float = None
    draught: float = None
    arrival_time: str = None
    arrival_time_utc: int = None
    stay_time: float = None
    navistat: int = None  # 有些数据可能没有该字段


class GetBerthShipsResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[BerthShipData] = None


class AnchorShipData(BaseModel):
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    ship_type: int = None
    length: float = None
    width: float = None
    left: float = None
    trail: float = None
    draught: float = None
    arrival_time: str = None
    arrival_time_utc: int = None
    stay_time: float = None
    navistat: int = None  # 有些数据可能没有该字段


class GetAnchorShipsResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[AnchorShipData] = None


class ETAShipData(BaseModel):
    mmsi: int = None
    ship_name: str = None
    imo: int = None
    dwt: float = None
    ship_type: str = None
    length: float = None
    width: float = None
    draught: float = None
    preport_cnname: str = None
    last_time: str = None
    last_time_utc: int = None
    eta: str = None
    eta_utc: int = None
    dest: str = None
    ship_flag: str = None
    registry: str = None


class GetETAShipsResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[ETAShipData] = None


class ShipTrackPoint(BaseModel):
    data_source: int = None
    utc: int = None
    lng: float = None
    lat: float = None
    sog: float = None
    cog: float = None


class GetShipTrackResponse(BaseModel):
    status: int = None
    msg: str = None
    data: list[ShipTrackPoint] = None


class ApproachShipInfo(BaseModel):
    mmsi: int = None
    imo: int = None
    call_sign: str = None
    ship_name: str = None
    ship_type: int = None


class ApproachEventInfo(BaseModel):
    approach_zone: int = None
    lat: float = None
    lng: float = None
    port_code: str = None
    position: str = None
    approach_time: str = None
    approach_time_utc: int = None
    separation_time: str = None
    separation_time_utc: int = None
    duration: float = None
    sog: float = None


class ApproachDataItem(BaseModel):
    approach_ship: ApproachShipInfo = None
    approach_event: ApproachEventInfo = None


class ShipApproachData(BaseModel):
    ship_data: ApproachShipInfo = None
    approach_data: list[ApproachDataItem] = None


class SearchShipApproachResponse(BaseModel):
    status: int = None
    msg: str = None
    data: ShipApproachData = None


class PortOfCallData(BaseModel):
    ship_name: str = None
    call_sign: str = None
    imo: int = None
    mmsi: int = None
    ship_type: int = None
    port_cnname: str = None
    port_name: str = None
    port_time_zone: str = None
    port_code: str = None
    terminal_name: str = None
    berth_name: str = None
    port_country_cnname: str = None
    port_country_name: str = None
    port_country_code: str = None
    arrival_anchorage: str = None
    ata: str = None
    atb: str = None
    atd: str = None
    arrival_draught: float = None
    departure_draught: float = None
    stay_time: float = None
    stay_terminal_time: float = None


class GetPortOfCallByShipResponse(BaseModel):
    status: int = None
    msg: str = None
    data: list[PortOfCallData] = None


class PortOfCallByShipPortData(BaseModel):
    ship_name: str = None
    call_sign: str = None
    imo: int = None
    mmsi: int = None
    ship_type: str = None
    port_cnname: str = None
    port_name: str = None
    port_time_zone: str = None
    port_code: str = None
    terminal_name: str = None
    berth_name: str = None
    port_country_cnname: str = None
    port_country_name: str = None
    port_country_code: str = None
    arriveanchorage: str = None
    ata: str = None
    atb: str = None
    atd: str = None
    arrival_draught: float = None
    departure_draught: float = None
    stay_time: float = None
    stay_terminal_time: float = None


class GetPortOfCallByShipPortResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[PortOfCallByShipPortData] = None


class PortInfo(BaseModel):
    port_code: str = None
    port_name: str = None
    port_cnname: str = None
    port_time_zone: str = None
    port_country_name: str = None
    port_country_cnname: str = None
    port_country_code: str = None
    arrive_anchorage: str = None
    ata: str = None
    atb: str = None
    atd: str = None
    # currentport 可能有 country_en、country_code、arriveanchorage
    country_en: str = None
    country_code: str = None
    arriveanchorage: str = None


class ShipStatusData(BaseModel):
    ship_name: str = None
    call_sign: str = None
    imo: int = None
    mmsi: int = None
    ship_type: str = None
    current_sea_area: str = None
    sea_area_code: str = None
    current_city: str = None
    current_city_code: str = None
    lng: float = None
    lat: float = None
    previousport: PortInfo = None
    currentport: PortInfo = None


class GetShipStatusResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[ShipStatusData] = None


class PortCallPortInfo(BaseModel):
    port_code: str = None
    port_cnname: str = None
    port_name: str = None
    port_time_zone: str = None
    terminal_name: str = None
    berth_name: str = None
    arrival_anchorage: str = None
    ata: str = None
    atb: str = None
    atd: str = None
    arrival_draught: float = None
    departure_draught: float = None
    stay_time: float = None
    stay_terminal_time: float = None


class PortOfCallByPortData(BaseModel):
    imo: int = None
    mmsi: int = None
    ship_type: str = None
    ship_name: str = None
    call_sign: str = None
    currentport: PortCallPortInfo = None
    previousport: PortCallPortInfo = None
    nextport: PortCallPortInfo = None


class GetPortOfCallByPortResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[PortOfCallByPortData] = None


class RoutePoint(BaseModel):
    lng: float = None
    lat: float = None


class PlanRouteByPointData(BaseModel):
    distance: float = None
    route: list[RoutePoint] = None


class PlanRouteByPointResponse(BaseModel):
    status: int = None
    msg: str = None
    data: PlanRouteByPointData = None


class PlanRouteByPortData(BaseModel):
    distance: float = None
    route: list[RoutePoint] = None


class PlanRouteByPortResponse(BaseModel):
    status: int = None
    msg: str = None
    data: PlanRouteByPortData = None


class SingleETAShipInfo(BaseModel):
    mmsi: int = None
    imo: int = None
    ship_name: str = None
    call_sign: str = None
    ship_type: int = None


class SingleETALocationInfo(BaseModel):
    lng: float = None
    lat: float = None
    speed: float = None
    sog: float = None
    sea_area: str = None
    sea_area_code: int = None


class SingleETAPortInfo(BaseModel):
    port_code: str = None
    port_cnname: str = None
    port_name: str = None
    time_zone: int = None
    port_country_code: str = None
    port_country_name: str = None
    port_country_cnname: str = None
    ata: float = None
    atb: float = None
    atd: float = None


class SingleETANextPortInfo(BaseModel):
    port_code: str = None
    port_cnname: str = None
    port_name: str = None
    time_zone: int = None
    port_country_code: str = None
    port_country_name: str = None
    port_country_cnname: str = None
    sailed_distance: float = None
    sailed_time: float = None
    ais_speed: float = None
    speed: float = None
    eta: str = None
    eta_utc: int = None
    remaining_distance: float = None
    distance: float = None


class GetSingleETAPreciseData(BaseModel):
    ship: SingleETAShipInfo = None
    location: SingleETALocationInfo = None
    preport: SingleETAPortInfo = None
    nextport: SingleETANextPortInfo = None


class GetSingleETAPreciseResponse(BaseModel):
    status: int = None
    msg: str = None
    data: GetSingleETAPreciseData = None


class WeatherData(BaseModel):
    weather_type: int = None
    sea_area: str = None
    publish_time: str = None
    center_lat: float = None
    center_lng: float = None
    forecastaging: str = None
    meteorological: str = None
    winddirection: str = None
    windpower: str = None
    waveheight: str = None
    visibility: float = None


class GetWeatherResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[WeatherData] = None


class TyphoonListItem(BaseModel):
    typhoon_id: int = None
    typhoon_code: int = None
    typhoon_cncode: str = None
    typhoon_cnname: str = None
    typhoon_name: str = None
    current_year: int = None
    dataMark: str = None


class GetAllTyphoonResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[TyphoonListItem] = None


class TyphoonDetailItem(BaseModel):
    typhoon_id: int = None
    typhoon_time: int = None
    forecast: str = None
    fhour: str = None
    lat: float = None
    lng: float = None
    grade: int = None
    mspeed: float = None
    pressure: float = None
    kspeed: float = None
    direction: str = None
    radius7: float = None
    radius10: float = None
    radius7_s: float = None
    radius10_s: float = None
    radius12_s: float = None


class GetSingleTyphoonResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[TyphoonDetailItem] = None


class TideStationInfo(BaseModel):
    port_code: int = None
    port_cnname: str = None
    port_name: str = None
    port_country_cnname: str = None
    port_country_name: str = None
    lat: float = None
    lng: float = None
    port_time_zone: str = None
    datumn: str = None
    tide_type: str = None


class GetTidesResponse(BaseModel):
    status: int = None
    msg: str = None
    total: int = None
    data: list[TideStationInfo] = None


class TideOverviewItem(BaseModel):
    tide_date: str = None
    tide_time1: str = None
    tide_time2: str = None
    tide_time3: str = None
    tide_time4: str = None
    tide_height1: float = None
    tide_height2: float = None
    tide_height3: float = None
    tide_height4: float = None
    tide_lowhigh1: str = None
    tide_lowhigh2: str = None
    tide_lowhigh3: str = None
    tide_lowhigh4: str = None


class TideDetailItem(BaseModel):
    tide_date: str = None
    h0: float = None
    h1: float = None
    h2: float = None
    h3: float = None
    h4: float = None
    h5: float = None
    h6: float = None
    h7: float = None
    h8: float = None
    h9: float = None
    h10: float = None
    h11: float = None
    h12: float = None
    h13: float = None
    h14: float = None
    h15: float = None
    h16: float = None
    h17: float = None
    h18: float = None
    h19: float = None
    h20: float = None
    h21: float = None
    h22: float = None
    h23: float = None


class GetTideDataData(BaseModel):
    overview: list[TideOverviewItem] = None
    detail: list[TideDetailItem] = None


class GetTideDataResponse(BaseModel):
    status: int = None
    msg: str = None
    data: GetTideDataData = None


class GetWeatherByPointData(BaseModel):
    bm500: float = None
    humidity: float = None
    oceandir: float = None
    oceanspeed: float = None
    pressure: float = None
    swelldir: float = None
    swellheight: float = None
    swellperiod: float = None
    temperature: float = None
    visibility: float = None
    waveheight: float = None
    winddir: float = None
    windspeed: float = None
    publish_time: str = None
    lng: float = None
    lat: float = None


class GetWeatherByPointResponse(BaseModel):
    status: float = None
    msg: str = None
    data: GetWeatherByPointData = None


class GetNavWarningData(BaseModel):
    warning_type: int = None
    source: str = None
    title: str = None
    range_type: int = None
    range_points: str = None
    radius: float = None
    pub_time: str = None
    expire_time: str = None
    content: str = None


class GetNavWarningResponse(BaseModel):
    status: float = None
    msg: str = None
    total: int = None
    data: List[GetNavWarningData] = None

class FleetData(BaseModel):
    fleet_id: str = None
    fleet_name: str = None
    mmsis: str = None
    monitor: str = None

class FleetResponse(BaseModel):
    status: int = None
    msg: str = None
    data: FleetData = None

class AreaData(BaseModel):
    area_id: str = None
    area_bounds: str = None
    area_name: str = None
    url: str = None
    filter_type: int = None
    ship_type: Optional[str] = None
    length: Optional[str] = None
    fleet_id: Optional[str] = None

class AreaResponse(BaseModel):
    status: int = None
    msg: str = None
    data: AreaData = None
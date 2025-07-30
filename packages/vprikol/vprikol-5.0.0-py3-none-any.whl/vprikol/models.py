import datetime
from enum import Enum
from typing import List, Optional, Dict, Union, Any, Literal
from pydantic import BaseModel, Field


class RatingType(str, Enum):
    ADMINS = "admins"
    ADVOCATES = "advocates"
    COMBINE_OPERATORS = "combine_operators"
    BUS_DRIVERS = "bus_drivers"
    TRACTOR_DRIVERS = "tractor_drivers"
    CATCHERS = "catchers"
    COLLECTORS = "collectors"
    CORN_PILOTS = "corn_pilots"
    CRYPTO_ASC = "crypto_asc"
    CRYPTO_BTC = "crypto_btc"
    ELECTRIC_TRAIN_DRIVERS = "electric_train_drivers"
    LVL_FAMILIES = "lvl_families"
    LVL_PLAYERS = "lvl_players"
    MECHANICS = "mechanics"
    RICHEST = "richest"
    OUTBIDS = "outbids"
    PILOTS = "pilots"
    SELLERS = "sellers"
    TAXI_DRIVERS = "taxi_drivers"
    TRAM_DRIVERS = "tram_drivers"
    TRUCKERS = "truckers"
    CLADMENS = "cladmens"


class EstateType(str, Enum):
    HOUSES = "houses"
    BUSINESSES = "businesses"


class ValidationError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = None


class AuctionInfo(BaseModel):
    active: bool
    minimal_bet: int
    time_end: Optional[datetime.datetime]
    start_price: int


class Coordinates(BaseModel):
    x: float
    y: float


class HouseEntry(BaseModel):
    id: int
    owner: Optional[str]
    name: Optional[str]
    auction: AuctionInfo
    coordinates: Coordinates


class BusinessEntry(BaseModel):
    id: int
    owner: Optional[str]
    name: str
    auction: AuctionInfo
    coordinates: Coordinates


class EstateResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    houses: List[HouseEntry]
    businesses: List[BusinessEntry]


class CheckRpNameData(BaseModel):
    value: Optional[str]
    is_existing: bool
    is_confirmed: bool
    nationalities_chart: Optional[str]


class CheckRpResponse(BaseModel):
    first_name: CheckRpNameData
    last_name: CheckRpNameData
    nickname: str


class ServerInfo(BaseModel):
    server_id: int
    server_label: str


class PlayerGeneral(BaseModel):
    account_id: int
    nickname: str
    gender: str
    skin_id: int
    played_hours: int
    phone_number: Optional[int]
    health: int
    hunger: int
    max_hunger: int
    drug_addict_lvl: int
    marriage: Optional[str]
    job_label: str


class PlayerFraction(BaseModel):
    fraction_id: Optional[int]
    fraction_label: Optional[str]
    rank_number: Optional[int]
    rank_label: Optional[str]


class IndividualAccounts(BaseModel):
    account_1: Optional[int] = Field(None, alias="1")
    account_2: Optional[int] = Field(None, alias="2")
    account_3: Optional[int] = Field(None, alias="3")
    account_4: Optional[int] = Field(None, alias="4")
    account_5: Optional[int] = Field(None, alias="5")
    account_6: Optional[int] = Field(None, alias="6")


class PlayerMoney(BaseModel):
    az_coins: int
    total_money: int
    cash: int
    bank_balance: int
    deposit: int
    have_bank_card: bool
    charity_money: int
    phone_balance: int
    individual_accounts: IndividualAccounts


class PlayerLvl(BaseModel):
    lvl: int
    current_xp: int
    max_xp: int


class PlayerPunishes(BaseModel):
    law_count: int
    wanted_lvl: int
    warns_count: int


class PlayerVIP(BaseModel):
    vip_lvl: int
    vip_label: str
    vip_expiration_date: Optional[datetime.datetime]
    have_addition_vip: bool
    addition_vip_expiration_date: Optional[datetime.datetime]


class FindPlayerResponse(BaseModel):
    server: ServerInfo
    general: PlayerGeneral
    fraction: PlayerFraction
    money: PlayerMoney
    lvl: PlayerLvl
    punishes: PlayerPunishes
    vip_info: PlayerVIP


class MembersPlayer(BaseModel):
    account_id: Optional[int]
    nickname: str
    is_online: bool
    is_leader: bool
    rank_number: int
    rank_label: Optional[str]
    ingame_id: Optional[int]
    nickname_color: Optional[int]


class MembersRecord(BaseModel):
    online_players: int
    leader_nickname: Optional[str]
    modified_at: Optional[datetime.datetime]
    modified_by: Literal["system", "admin"]


class MembersResponse(BaseModel):
    server_id: int
    fraction_id: int
    server_label: str
    fraction_label: str
    total_players: int
    total_online: int
    leader_nickname: Optional[str]
    is_leader_online: bool
    online_updated_at: datetime.datetime
    members_updated_at: datetime.datetime
    online_record: MembersRecord
    players: List[MembersPlayer]


class OnlineEntry(BaseModel):
    date: datetime.date
    hours: int
    minutes: int
    seconds: int


class OnlineResponse(BaseModel):
    online: List[OnlineEntry]
    have_active_session: bool
    active_session_login_at: Optional[datetime.datetime]
    last_login_at: Optional[datetime.datetime]
    last_logout_at: Optional[datetime.datetime]


class RatingPlayer(BaseModel):
    position: int
    nickname: str
    value: Any
    server_id: int
    server_label: str
    additional_value: Optional[Any] = None
    az_coins: Optional[int] = None
    family: Optional[str] = None


class RatingResponse(BaseModel):
    server_id: int
    server_label: str
    rating_type: RatingType
    updated_at: datetime.datetime
    players: List[RatingPlayer]


class RpNickResponse(BaseModel):
    name: str
    surname: str
    nickname: str


class ServerStatusResponse(BaseModel):
    server_id: int
    server_ip: str
    server_port: int
    server_label: str
    online_players: int
    max_players: int
    is_closed: bool
    server_vk: Optional[str] = None
    server_discord: Optional[str] = None
    main_admin_vk: Optional[str] = None
    deputy_main_admin_vk: Optional[str] = None
    updated_at: datetime.datetime


class TokenResponse(BaseModel):
    id: int
    project_label: str
    token: Optional[str]
    activated: bool
    disabled_logs: bool
    service: bool
    subscription_until: Optional[datetime.datetime]
    created_at: datetime.datetime
    modified_at: datetime.datetime


class RequestLogEntry(BaseModel):
    id: int
    api_method: Optional[str]
    http_method: str
    params: Dict[str, Any]
    ip_address: str
    created_at: datetime.datetime


class RequestLogResponse(BaseModel):
    data: List[RequestLogEntry]
    next_request_start_id: Optional[int]


class RequestStatsResponse(BaseModel):
    total_count: int
    methods: Dict[str, int]


class LeaderEntry(BaseModel):
    fraction_id: int
    fraction_label: str
    nickname: str
    ingame_id: int
    phone_number: Optional[int]
    afk: Optional[int]


class LeadersResponse(BaseModel):
    data: List[LeaderEntry]
    server_id: int
    server_label: str
    updated_at: datetime.datetime


class InterviewEntry(BaseModel):
    fraction_id: int
    fraction_label: str
    place: Optional[str]
    time: Optional[str]


class InterviewsResponse(BaseModel):
    server_id: int
    server_label: str
    data: List[InterviewEntry]
    updated_at: datetime.datetime


class PlayerEntry(BaseModel):
    color: int
    ping: int
    id: int
    lvl: int
    nickname: str


class PlayersResponse(BaseModel):
    server_id: int
    server_label: str
    players: List[PlayerEntry]
    updated_at: datetime.datetime


class TerritoriesCount(BaseModel):
    grove: int = 0
    ballas: int = 0
    vagos: int = 0
    rifa: int = 0
    aztec: int = 0
    nw: int = 0


class MapResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    image: str
    territories_count: TerritoriesCount


class BotAccount(BaseModel):
    nickname: str
    avg_sessions_per_day: float
    avg_session_duration_seconds: float


class BotDetectionResponse(BaseModel):
    accounts: List[BotAccount]


class CheckrRpManualOverrideEntry(BaseModel):
    value: str
    status: Literal["confirmed", "denied"]


class CheckRpManualOverridesListResponse(BaseModel):
    names: List[CheckrRpManualOverrideEntry]
    surnames: List[CheckrRpManualOverrideEntry]

import datetime
from typing import List, Optional, Union, Literal
from pydantic import parse_obj_as

from .models import (ServerStatusResponse, RatingResponse, CheckRpResponse, RpNickResponse, EstateResponse, MembersResponse, FindPlayerResponse, OnlineResponse, TokenResponse, RequestLogResponse,
                     RequestStatsResponse, LeadersResponse, InterviewsResponse, PlayersResponse, MapResponse, RatingType, EstateType, BotDetectionResponse, CheckRpManualOverridesListResponse)
from . import api


class VprikolAPI:
    def __init__(self, token: Optional[str] = None, base_url: str = "https://apitest.szx.su/"):
        self.base_url = base_url
        self.headers = {}
        if token:
            self.headers["VP-API-Token"] = token

    async def get_token_information(self, token_id: Union[int, Literal["current", "all", "deactivated"]] = "current") -> Union[TokenResponse, List[TokenResponse]]:
        response_json = await api.get_json(self.base_url, f"token/{token_id}", self.headers)
        if isinstance(response_json, list):
            return parse_obj_as(List[TokenResponse], response_json)
        return TokenResponse.parse_obj(response_json)

    async def get_server_status(self, server_id: int) -> ServerStatusResponse:
        params = {"server_id": str(server_id)}
        response_json = await api.get_json(self.base_url, "status", self.headers, params=params)
        return ServerStatusResponse.parse_obj(response_json)

    async def get_rating(self, server_id: int, rating_type: RatingType) -> RatingResponse:
        params = {"server_id": str(server_id), "rating_type": rating_type.value}
        response_json = await api.get_json(self.base_url, "rating", self.headers, params=params)
        return RatingResponse.parse_obj(response_json)

    async def get_estate(self, server_id: int, estate_type: Optional[EstateType] = None, nickname: Optional[str] = None, min_id: Optional[int] = None, max_id: Optional[int] = None) -> EstateResponse:
        params = {"server_id": str(server_id)}
        if estate_type:
            params["type"] = estate_type.value
        if nickname:
            params["nickname"] = nickname
        if min_id is not None:
            params["min_id"] = str(min_id)
        if max_id is not None:
            params["max_id"] = str(max_id)

        response_json = await api.get_json(self.base_url, "estate", self.headers, params=params)
        return EstateResponse.parse_obj(response_json)

    async def check_rp_nickname(self, first_name: Optional[str] = None, last_name: Optional[str] = None) -> CheckRpResponse:
        params = {}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name

        response_json = await api.get_json(self.base_url, "checkrp", self.headers, params=params)
        return CheckRpResponse.parse_obj(response_json)

    async def generate_rp_nickname(self, gender: str, nation: str) -> RpNickResponse:
        params = {"gender": gender, "nation": nation}
        response_json = await api.get_json(self.base_url, "rpnick", self.headers, params=params)
        return RpNickResponse.parse_obj(response_json)

    async def get_leaders(self, server_id: int) -> LeadersResponse:
        params = {"server_id": str(server_id)}
        response_json = await api.get_json(self.base_url, "ingame/leaders", self.headers, params=params)
        return LeadersResponse.parse_obj(response_json)

    async def get_deputies(self, server_id: int) -> LeadersResponse:
        params = {"server_id": str(server_id)}
        response_json = await api.get_json(self.base_url, "ingame/deputies", self.headers, params=params)
        return LeadersResponse.parse_obj(response_json)

    async def get_interviews(self, server_id: int) -> InterviewsResponse:
        params = {"server_id": str(server_id)}
        response_json = await api.get_json(self.base_url, "ingame/interviews", self.headers, params=params)
        return InterviewsResponse.parse_obj(response_json)

    async def get_players(self, server_id: int) -> PlayersResponse:
        params = {"server_id": str(server_id)}
        response_json = await api.get_json(self.base_url, "ingame/players", self.headers, params=params)
        return PlayersResponse.parse_obj(response_json)

    async def get_server_map(self, server_id: int, only_ghetto: bool = False) -> MapResponse:
        params = {"server_id": str(server_id), "only_ghetto": str(only_ghetto).lower()}
        response_json = await api.get_json(self.base_url, "ingame/map", self.headers, params=params)
        return MapResponse.parse_obj(response_json)

    async def get_token_requests_history(self, token_id: Union[int, Literal["current"]] = "current", limit: int = 50, request_start_id: Optional[int] = None,
                                         date_from: Optional[datetime.datetime] = None, date_to: Optional[datetime.datetime] = None,
                                         api_method: Optional[str] = None, ip_address: Optional[str] = None) -> RequestLogResponse:
        params = {"limit": str(limit)}
        if request_start_id is not None:
            params["request_start_id"] = str(request_start_id)
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()
        if api_method:
            params["api_method"] = api_method
        if ip_address:
            params["ip_address"] = ip_address

        response_json = await api.get_json(self.base_url, f"token/{token_id}/requests", self.headers, params=params)
        return RequestLogResponse.parse_obj(response_json)

    async def get_token_requests_stats(self, token_id: Union[int, Literal["current"]] = "current",
                                       date_from: Optional[datetime.datetime] = None, date_to: Optional[datetime.datetime] = None,
                                       api_method: Optional[str] = None, ip_address: Optional[str] = None) -> RequestStatsResponse:
        params = {}
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()
        if api_method:
            params["api_method"] = api_method
        if ip_address:
            params["ip_address"] = ip_address

        response_json = await api.get_json(self.base_url, f"token/{token_id}/requests/stats", self.headers, params=params)
        return RequestStatsResponse.parse_obj(response_json)

    async def find_player(self, server_id: int, nickname: str) -> FindPlayerResponse:
        params = {"server_id": str(server_id), "nickname": nickname}
        response_json = await api.get_json(self.base_url, "player/find", self.headers, params=params)
        return FindPlayerResponse.parse_obj(response_json)

    async def get_player_online(self, server_id: int, nickname: str, date_from: Optional[datetime.datetime] = None, date_to: Optional[datetime.datetime] = None) -> OnlineResponse:
        params = {"server_id": str(server_id), "nickname": nickname}
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()

        response_json = await api.get_json(self.base_url, "player/online", self.headers, params=params)
        return OnlineResponse.parse_obj(response_json)

    async def get_fraction_members(self, server_id: int, fraction_id: int) -> MembersResponse:
        params = {"server_id": str(server_id), "fraction_id": str(fraction_id)}
        response_json = await api.get_json(self.base_url, "fraction/members", self.headers, params=params)
        return MembersResponse.parse_obj(response_json)

    async def get_manual_checkrp_overrides(self) -> CheckRpManualOverridesListResponse:
        response_json = await api.get_json(self.base_url, "internal/checkrp/overrides", self.headers)
        return CheckRpManualOverridesListResponse.parse_obj(response_json)

    async def get_current_ip(self) -> str:
        return await api.get_json(self.base_url, "internal/ip", self.headers)

    async def list_disabled_methods(self) -> List[str]:
        response_json = await api.get_json(self.base_url, "internal/disabled-methods", self.headers)
        return parse_obj_as(List[str], response_json)

    async def detect_bots(self, server_id: int, date_from: Optional[datetime.datetime] = None, date_to: Optional[datetime.datetime] = None) -> BotDetectionResponse:
        params = {"server_id": str(server_id)}
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()

        response_json = await api.get_json(self.base_url, "internal/detect-bots", self.headers, params=params)
        return BotDetectionResponse.parse_obj(response_json)

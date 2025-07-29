import asyncio
import json
import time
from pydantic import BaseModel
from typing import Optional
import httpx
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient

from sb_on_demand.oracle_account_data import OracleAccountData
from sb_on_demand.oracle_account_data_layout import OracleAccountDataLayout
import base64
from construct import Struct, Array, Byte


class RandomnessRevealResponse(BaseModel):
    signature: bytes
    recovery_id: int
    value: bytes

    @classmethod
    def from_json(cls, json_str: str) -> "RandomnessRevealResponse":
        data = json.loads(json_str)
        # value: list[int] -> bytes
        if isinstance(data.get("value"), list):
            data["value"] = bytes(data["value"])
        # signature: base64 string -> bytes
        if isinstance(data.get("signature"), str):
            data["signature"] = base64.b64decode(data["signature"])
        return cls(**data)

    def to_bytes(self) -> bytes:
        # RandomnessRevealParamsLayout to bytes
        layout = Struct(
            "signature" / Array(64, Byte),
            "recovery_id" / Byte,
            "value" / Array(32, Byte),
        )
        # 确保长度正确
        sig = self.signature if len(self.signature) == 64 else self.signature.ljust(64, b"\x00")
        val = self.value if len(self.value) == 32 else self.value.ljust(32, b"\x00")

        return layout.build(
            {
                "signature": list(sig),
                "recovery_id": self.recovery_id,
                "value": list(val),
            }
        )


class OracleGatewayConfig(BaseModel):
    chain: str
    disable_heartbeats: bool
    ed25519_pubkey: str
    enable_gateway: int
    enable_guardian: int
    enable_pull_oracle: int
    enable_push_oracle: int
    gateway_advertise_interval: int
    gateway_ingress: str
    heartbeat_interval: int
    key_rotate_interval: int
    mr_enclave: str
    network_id: str
    oracle_authority: str
    oracle_ingress: str
    pagerduty_api_key: Optional[str]
    payer_secret: Optional[str]
    payer_secret_filepath: str
    guardian_oracle: str
    pull_oracle: str
    push_oracle: str
    push_queue: str
    routine_max_jitter: int
    rpc_url: str
    secp256k1_pubkey: str
    switchboard_on_demand_program_id: str
    version_filepath: str
    version: str
    wss_rpc_url: str
    known_oracles: str
    system_time: int
    restricted: bool
    api_key_service_url: str


async def test_oracles(connection: AsyncClient, oracles: list[Pubkey]) -> list[Pubkey]:
    async def test_oracle(oracle: Pubkey) -> Optional[Pubkey]:
        try:
            oracle_data = await fetch_oracle_account_data(connection, oracle)
            if oracle_data:
                # Filter for verified oracles (verification_status == 4) that are valid for at least 1 hour
                if (
                    oracle_data.enclave
                    and oracle_data.enclave.verification_status == 4
                    and oracle_data.enclave.valid_until > int(time.time()) + 3600
                ):
                    if await test_gateway(oracle_data.gateway_uri):
                        return oracle
                    else:
                        return None
                else:
                    return None
        except Exception as e:
            print(f"Oracle test failed for {oracle}: {e}")
        return None

    results = await asyncio.gather(*[test_oracle(oracle) for oracle in oracles])
    return [oracle for oracle in results if oracle is not None]


async def fetch_oracle_account_data(connection: AsyncClient, oracle: Pubkey) -> OracleAccountData:
    account_info = await connection.get_account_info(oracle)
    if account_info.value and account_info.value.data:
        data_bytes = account_info.value.data
        parsed = OracleAccountDataLayout.parse(data_bytes)
        return OracleAccountData(parsed)
    return None


async def test_gateway(gateway_url: str) -> bool:
    url = f"{gateway_url.rstrip('/')}/gateway/api/v1/test"  # 规范化URL拼接
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)  # 添加超时

        if response.status_code == 200 and response.text:
            return True
    except (httpx.RequestError, httpx.TimeoutException, Exception) as e:
        print(f"Gateway test failed for {url}: {e}")
    return False


class FetchRandomnessRevealParams:
    def __init__(self, randomnessAccount: Pubkey, slothash: bytes, slot: int, rpc: str):
        self.randomnessAccount = randomnessAccount
        self.slothash = slothash
        self.slot = slot
        self.rpc = rpc


# send request to oracle's gateway to fetch randomness reveal
async def fetch_randomness_reveal(gateway_url: str, params: FetchRandomnessRevealParams) -> RandomnessRevealResponse:
    url = f"{gateway_url.rstrip('/')}/gateway/api/v1/randomness_reveal"
    headers = {"Content-Type": "application/json"}
    data = None

    slothash_bytes = params.slothash
    data = {
        "slothash": list(slothash_bytes),  # Convert bytes to list of integers
        "randomness_key": bytes(params.randomnessAccount).hex(),
        "slot": params.slot,
        "rpc": params.rpc,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data, timeout=10.0)

        if response.status_code == 500:
            print(f"Server error (500) response body: {response.text}")

        # Check if the response is valid JSON
        if response.status_code == 200:
            return RandomnessRevealResponse.from_json(response.text)
        else:
            return response.text
    except Exception as err:
        print(f"fetch_randomness_reveal error: {err}")
        raise

from dataclasses import dataclass
from typing import List
from solders.pubkey import Pubkey


@dataclass
class Quote:
    enclave_signer: Pubkey
    mr_enclave: bytes
    verification_status: int
    padding1: bytes
    verification_timestamp: int
    valid_until: int
    quote_registry: bytes
    registry_key: bytes
    secp256k1_signer: bytes
    last_ed25519_signer: Pubkey
    last_secp256k1_signer: bytes
    last_rotate_slot: int
    guardian_approvers: List[Pubkey]
    guardian_approvers_len: int
    padding2: bytes
    staging_ed25519_signer: Pubkey
    staging_secp256k1_signer: bytes
    eth_signer: bytes
    _ebuf4: bytes
    last_sign_ts: int
    _ebuf3: bytes
    _ebuf2: bytes
    _ebuf1: bytes

    @classmethod
    def from_dict(cls, d):
        return cls(
            enclave_signer=Pubkey.from_bytes(d["enclave_signer"]),
            mr_enclave=d["mr_enclave"],
            verification_status=int.from_bytes(d["verification_status"], byteorder="little"),
            padding1=d["padding1"],
            verification_timestamp=d["verification_timestamp"],
            valid_until=d["valid_until"],
            quote_registry=d["quote_registry"],
            registry_key=d["registry_key"],
            secp256k1_signer=d["secp256k1_signer"],
            last_ed25519_signer=Pubkey.from_bytes(d["last_ed25519_signer"]),
            last_secp256k1_signer=d["last_secp256k1_signer"],
            last_rotate_slot=d["last_rotate_slot"],
            guardian_approvers=[Pubkey.from_bytes(x) for x in d["guardian_approvers"]],
            guardian_approvers_len=d["guardian_approvers_len"],
            padding2=d["padding2"],
            staging_ed25519_signer=Pubkey.from_bytes(d["staging_ed25519_signer"]),
            staging_secp256k1_signer=d["staging_secp256k1_signer"],
            eth_signer=d["eth_signer"],
            _ebuf4=d["_ebuf4"],
            last_sign_ts=d["last_sign_ts"],
            _ebuf3=d["_ebuf3"],
            _ebuf2=d["_ebuf2"],
            _ebuf1=d["_ebuf1"],
        )

    def to_json_dict(self):
        def encode_value(val):
            if isinstance(val, Pubkey):
                return str(val)
            elif isinstance(val, bytes):
                return "0x" + val.hex()
            elif isinstance(val, list):
                return [encode_value(x) for x in val]
            else:
                return val

        return {k: encode_value(getattr(self, k)) for k in self.__dataclass_fields__}


@dataclass
class OracleAccountData:
    discriminator: bytes
    enclave: Quote
    authority: Pubkey
    queue: Pubkey
    created_at: int
    last_heartbeat: int
    secp_authority: bytes
    gateway_uri: str
    permissions: int
    is_on_queue: bool
    _padding1: bytes
    lut_slot: int
    last_reward_epoch: int
    operator: Pubkey
    _ebuf3: bytes
    _ebuf2: bytes
    _ebuf1: bytes

    def __init__(self, d: dict):
        self.discriminator = d["discriminator"]
        self.enclave = Quote.from_dict(d["enclave"])
        self.authority = Pubkey.from_bytes(d["authority"])
        self.queue = Pubkey.from_bytes(d["queue"])
        self.created_at = d["created_at"]
        self.last_heartbeat = d["last_heartbeat"]
        self.secp_authority = d["secp_authority"]
        self.gateway_uri = d["gateway_uri"].split(b"\x00", 1)[0].decode("utf-8")
        self.permissions = d["permissions"]
        self.is_on_queue = bool(d["is_on_queue"])
        self._padding1 = d["_padding1"]
        self.lut_slot = d["lut_slot"]
        self.last_reward_epoch = d["last_reward_epoch"]
        self.operator = Pubkey.from_bytes(d["operator"])
        self._ebuf3 = d["_ebuf3"]
        self._ebuf2 = d["_ebuf2"]
        self._ebuf1 = d["_ebuf1"]

    def to_json_dict(self):
        def encode_value(val):
            if isinstance(val, Pubkey):
                return str(val)
            elif isinstance(val, bytes):
                return "0x" + val.hex()
            elif hasattr(val, "to_json_dict"):
                return val.to_json_dict()
            else:
                return val

        return {
            "discriminator": encode_value(self.discriminator),
            "enclave": self.enclave.to_json_dict(),
            "authority": encode_value(self.authority),
            "queue": encode_value(self.queue),
            "created_at": self.created_at,
            "last_heartbeat": self.last_heartbeat,
            "secp_authority": encode_value(self.secp_authority),
            "gateway_uri": encode_value(self.gateway_uri),
            "permissions": self.permissions,
            "is_on_queue": self.is_on_queue,
            "_padding1": encode_value(self._padding1),
            "lut_slot": self.lut_slot,
            "last_reward_epoch": self.last_reward_epoch,
            "operator": encode_value(self.operator),
            "_ebuf3": encode_value(self._ebuf3),
            "_ebuf2": encode_value(self._ebuf2),
            "_ebuf1": encode_value(self._ebuf1),
        }

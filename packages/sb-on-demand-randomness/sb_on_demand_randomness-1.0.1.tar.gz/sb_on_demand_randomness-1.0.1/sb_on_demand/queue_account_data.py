from dataclasses import dataclass
from typing import List
from solders.pubkey import Pubkey


@dataclass
class VaultInfo:
    vault_key: Pubkey
    last_reward: int

    @classmethod
    def from_dict(cls, d):
        return cls(vault_key=Pubkey.from_bytes(d["vault_key"]), last_reward=d["last_reward"])

    def to_json_dict(self):
        return {"vault_key": str(self.vault_key), "last_reward": self.last_reward}


@dataclass
class QueueAccountData:
    discriminator: bytes
    authority: Pubkey
    mr_enclaves: List[Pubkey]
    oracle_keys: List[Pubkey]
    reserved1: bytes
    oracle_signing_keys: List[bytes]
    max_quote_verification_age: int
    last_heartbeat: int
    node_timeout: int
    oracle_min_stake: int
    allow_authority_override_after: int
    mr_enclaves_len: int
    oracle_keys_len: int
    reward: int
    curr_idx: int
    gc_idx: int
    require_authority_heartbeat_permission: int
    require_authority_verify_permission: int
    require_usage_permissions: int
    signer_bump: int
    mint: Pubkey
    lut_slot: int
    allow_subsidies: int
    _ebuf6: bytes
    ncn: Pubkey
    _resrved: int
    vaults: List[VaultInfo]
    last_reward_epoch: int
    _ebuf4: bytes
    _ebuf2: bytes
    _ebuf1: bytes

    def __init__(self, d: dict):
        self.discriminator = d["discriminator"]
        self.authority = Pubkey.from_bytes(d["authority"])
        self.mr_enclaves = [Pubkey.from_bytes(x) for x in d["mr_enclaves"]]
        self.oracle_keys = [Pubkey.from_bytes(x) for x in d["oracle_keys"]]
        self.reserved1 = d["reserved1"]
        self.oracle_signing_keys = d["oracle_signing_keys"]
        self.max_quote_verification_age = d["max_quote_verification_age"]
        self.last_heartbeat = d["last_heartbeat"]
        self.node_timeout = d["node_timeout"]
        self.oracle_min_stake = d["oracle_min_stake"]
        self.allow_authority_override_after = d["allow_authority_override_after"]
        self.mr_enclaves_len = d["mr_enclaves_len"]
        self.oracle_keys_len = d["oracle_keys_len"]
        self.reward = d["reward"]
        self.curr_idx = d["curr_idx"]
        self.gc_idx = d["gc_idx"]
        self.require_authority_heartbeat_permission = d["require_authority_heartbeat_permission"]
        self.require_authority_verify_permission = d["require_authority_verify_permission"]
        self.require_usage_permissions = d["require_usage_permissions"]
        self.signer_bump = d["signer_bump"]
        self.mint = Pubkey.from_bytes(d["mint"])
        self.lut_slot = d["lut_slot"]
        self.allow_subsidies = d["allow_subsidies"]
        self._ebuf6 = d["_ebuf6"]
        self.ncn = Pubkey.from_bytes(d["ncn"])
        self._resrved = d["_resrved"]
        self.vaults = [VaultInfo.from_dict(v) for v in d["vaults"]]
        self.last_reward_epoch = d["last_reward_epoch"]
        self._ebuf4 = d["_ebuf4"]
        self._ebuf2 = d["_ebuf2"]
        self._ebuf1 = d["_ebuf1"]

    def to_json_dict(self):
        def encode_value(val):
            if isinstance(val, Pubkey):
                return str(val)
            elif isinstance(val, bytes):
                return "0x" + val.hex()
            elif isinstance(val, list):
                return [encode_value(x) for x in val]
            elif hasattr(val, "to_json_dict"):
                return val.to_json_dict()
            else:
                return val

        return {
            "discriminator": encode_value(self.discriminator),
            "authority": encode_value(self.authority),
            "mr_enclaves": encode_value(self.mr_enclaves),
            "oracle_keys": encode_value(self.oracle_keys),
            "reserved1": encode_value(self.reserved1),
            "oracle_signing_keys": encode_value(self.oracle_signing_keys),
            "max_quote_verification_age": self.max_quote_verification_age,
            "last_heartbeat": self.last_heartbeat,
            "node_timeout": self.node_timeout,
            "oracle_min_stake": self.oracle_min_stake,
            "allow_authority_override_after": self.allow_authority_override_after,
            "mr_enclaves_len": self.mr_enclaves_len,
            "oracle_keys_len": self.oracle_keys_len,
            "reward": self.reward,
            "curr_idx": self.curr_idx,
            "gc_idx": self.gc_idx,
            "require_authority_heartbeat_permission": self.require_authority_heartbeat_permission,
            "require_authority_verify_permission": self.require_authority_verify_permission,
            "require_usage_permissions": self.require_usage_permissions,
            "signer_bump": self.signer_bump,
            "mint": encode_value(self.mint),
            "lut_slot": self.lut_slot,
            "allow_subsidies": self.allow_subsidies,
            "_ebuf6": encode_value(self._ebuf6),
            "ncn": encode_value(self.ncn),
            "_resrved": self._resrved,
            "vaults": [v.to_json_dict() if hasattr(v, "to_json_dict") else v for v in self.vaults],
            "last_reward_epoch": self.last_reward_epoch,
            "_ebuf4": encode_value(self._ebuf4),
            "_ebuf2": encode_value(self._ebuf2),
            "_ebuf1": encode_value(self._ebuf1),
        }

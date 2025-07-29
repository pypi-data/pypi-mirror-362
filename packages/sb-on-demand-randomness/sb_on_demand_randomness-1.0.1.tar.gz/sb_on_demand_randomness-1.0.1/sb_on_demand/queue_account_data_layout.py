from construct import *

Pubkey_raw = Bytes(32)

VaultInfo = Struct(
    "vault_key" / Pubkey_raw,
    "last_reward" / Int64ul,
)

QueueAccountDataLayout = Struct(
    "discriminator" / Bytes(8),
    "authority" / Pubkey_raw,
    "mr_enclaves" / Array(32, Pubkey_raw),
    "oracle_keys" / Array(78, Pubkey_raw),
    "reserved1" / Bytes(40),
    "oracle_signing_keys" / Array(78, Bytes(20)),
    "max_quote_verification_age" / Int64sl,
    "last_heartbeat" / Int64sl,
    "node_timeout" / Int64sl,
    "oracle_min_stake" / Int64ul,
    "allow_authority_override_after" / Int64sl,
    "mr_enclaves_len" / Int32ul,
    "oracle_keys_len" / Int32ul,
    "reward" / Int32ul,
    "curr_idx" / Int32ul,
    "gc_idx" / Int32ul,
    "require_authority_heartbeat_permission" / Byte,
    "require_authority_verify_permission" / Byte,
    "require_usage_permissions" / Byte,
    "signer_bump" / Byte,
    "mint" / Pubkey_raw,
    "lut_slot" / Int64ul,
    "allow_subsidies" / Byte,
    "_ebuf6" / Bytes(15),
    "ncn" / Pubkey_raw,
    "_resrved" / Int64ul,
    "vaults" / Array(4, VaultInfo),
    "last_reward_epoch" / Int64ul,
    "_ebuf4" / Bytes(32),
    "_ebuf2" / Bytes(256),
    "_ebuf1" / Bytes(504),
)

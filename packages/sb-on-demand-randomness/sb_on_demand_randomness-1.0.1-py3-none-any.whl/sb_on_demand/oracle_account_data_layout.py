from construct import *

Pubkey_raw = Bytes(32)

QuoteLayout = Struct(
    "enclave_signer" / Pubkey_raw,
    "mr_enclave" / Bytes(32),
    "verification_status" / Bytes(1),
    "padding1" / Bytes(7),
    "verification_timestamp" / Int64sl,
    "valid_until" / Int64sl,
    "quote_registry" / Bytes(32),
    "registry_key" / Bytes(64),
    "secp256k1_signer" / Bytes(64),
    "last_ed25519_signer" / Pubkey_raw,
    "last_secp256k1_signer" / Bytes(64),
    "last_rotate_slot" / Int64ul,
    "guardian_approvers" / Array(64, Pubkey_raw),
    "guardian_approvers_len" / Bytes(1),
    "padding2" / Bytes(7),
    "staging_ed25519_signer" / Pubkey_raw,
    "staging_secp256k1_signer" / Bytes(64),
    "eth_signer" / Bytes(20),
    "_ebuf4" / Bytes(4),
    "last_sign_ts" / Int64sl,
    "_ebuf3" / Bytes(128),
    "_ebuf2" / Bytes(256),
    "_ebuf1" / Bytes(512),
)

OracleAccountDataLayout = Struct(
    "discriminator" / Bytes(8),
    "enclave" / QuoteLayout,
    "authority" / Pubkey_raw,
    "queue" / Pubkey_raw,
    "created_at" / Int64sl,
    "last_heartbeat" / Int64sl,
    "secp_authority" / Bytes(64),
    "gateway_uri" / Bytes(64),
    "permissions" / Int64ul,
    "is_on_queue" / Bytes(1),
    "_padding1" / Bytes(7),
    "lut_slot" / Int64ul,
    "last_reward_epoch" / Int64ul,
    "operator" / Pubkey_raw,
    "_ebuf3" / Bytes(16),
    "_ebuf2" / Bytes(64),
    "_ebuf1" / Bytes(1024),
)

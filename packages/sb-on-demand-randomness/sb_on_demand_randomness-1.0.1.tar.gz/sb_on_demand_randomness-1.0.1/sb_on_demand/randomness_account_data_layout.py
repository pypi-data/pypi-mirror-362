from construct import *


Pubkey_raw = Bytes(32)


RandomnessAccountDataLayout = Struct(
    "discriminator" / Bytes(8),
    "authority" / Pubkey_raw,
    "queue" / Pubkey_raw,
    "seed_slothash" / Bytes(32),
    "seed_slot" / Int64ul,
    "oracle" / Pubkey_raw,
    "reveal_slot" / Int64ul,
    "value" / Bytes(32),
    "lut_slot" / Int64ul,
    "_ebuf3" / Bytes(24),
    "_ebuf2" / Bytes(64),
    "_ebuf1" / Bytes(128),
    "active_secp256k1_signer" / Bytes(64),
    "active_secp256k1_expiration" / Int64sl,
)

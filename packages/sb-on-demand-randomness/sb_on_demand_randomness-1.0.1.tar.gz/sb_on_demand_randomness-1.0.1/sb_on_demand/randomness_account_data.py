from dataclasses import dataclass
from solders.pubkey import Pubkey


@dataclass
class RandomnessAccountData:
    discriminator: bytes
    authority: Pubkey
    queue: Pubkey
    seed_slothash: bytes
    seed_slot: int
    oracle: Pubkey
    reveal_slot: int
    value: bytes
    lut_slot: int
    _ebuf3: bytes
    _ebuf2: bytes
    _ebuf1: bytes
    active_secp256k1_signer: bytes
    active_secp256k1_expiration: int

    def __init__(self, d: dict):
        self.discriminator = d["discriminator"]
        self.authority = Pubkey.from_bytes(d["authority"])
        self.queue = Pubkey.from_bytes(d["queue"])
        self.seed_slothash = d["seed_slothash"]
        self.seed_slot = d["seed_slot"]
        self.oracle = Pubkey.from_bytes(d["oracle"])
        self.reveal_slot = d["reveal_slot"]
        self.value = d["value"]
        self.lut_slot = d["lut_slot"]
        self._ebuf3 = d["_ebuf3"]
        self._ebuf2 = d["_ebuf2"]
        self._ebuf1 = d["_ebuf1"]
        self.active_secp256k1_signer = d["active_secp256k1_signer"]
        self.active_secp256k1_expiration = d["active_secp256k1_expiration"]

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
            "queue": encode_value(self.queue),
            "seed_slothash": encode_value(self.seed_slothash),
            "seed_slot": self.seed_slot,
            "oracle": encode_value(self.oracle),
            "reveal_slot": self.reveal_slot,
            "value": encode_value(self.value),
            "lut_slot": self.lut_slot,
            "_ebuf3": encode_value(self._ebuf3),
            "_ebuf2": encode_value(self._ebuf2),
            "_ebuf1": encode_value(self._ebuf1),
            "active_secp256k1_signer": encode_value(self.active_secp256k1_signer),
            "active_secp256k1_expiration": self.active_secp256k1_expiration,
        }

import struct
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address
from solana.constants import ADDRESS_LOOKUP_TABLE_PROGRAM_ID, SYSTEM_PROGRAM_ID
from solders.instruction import AccountMeta, Instruction
from sb_on_demand.oracle_account_utility import RandomnessRevealResponse


SYSTEM_RECENT_SLOT_HASH_ID = Pubkey.from_string("SysvarS1otHashes111111111111111111111111111")
ON_DEMAND_MAINNET_PID = Pubkey.from_string("SBondMDrcV3K4kxZR1HNVT7osZxAHVHgYXL5Ze1oMUv")
ON_DEMAND_MAINNET_GUARDIAN_QUEUE = Pubkey.from_string("B7WgdyAgzK7yGoxfsBaNnY6d41bTybTzEh4ZuQosnvLK")
ON_DEMAND_MAINNET_QUEUE = Pubkey.from_string("A43DyUGA7s8eXPxqEjJY6EBu1KKbNgfxF8h17VAHn13w")

ON_DEMAND_DEVNET_PID = Pubkey.from_string("Aio4gaXjXzJNVLtzwtNVmSqGKpANtXhybbkhtAC94ji2")
ON_DEMAND_DEVNET_GUARDIAN_QUEUE = Pubkey.from_string("BeZ4tU4HNe2fGQGUzJmNS2UU2TcZdMUUgnCH6RPg4Dpi")
ON_DEMAND_DEVNET_QUEUE = Pubkey.from_string("EYiAmGSdsQTuCw413V5BzaruWuCCSDgTPtBGvLkXHbe7")

WSOL_MINT = Pubkey.from_string("So11111111111111111111111111111111111111112")
SYNERGY_PID = Pubkey.from_string("Uetge5b85Pry5wbUqPy94RwyCmqsjN7x2nYsky2SNGY")


def generate_create_random_ix(
    randomness: Pubkey, authority: Pubkey, payer: Pubkey, current_slot: int, network: str = "mainnet-beta"
) -> Instruction:
    PID = ON_DEMAND_DEVNET_PID if network == "devnet" else ON_DEMAND_MAINNET_PID
    QUEUE_ID = ON_DEMAND_DEVNET_QUEUE if network == "devnet" else ON_DEMAND_MAINNET_QUEUE

    reward_escrow = get_associated_token_address(randomness, WSOL_MINT)
    state, _ = Pubkey.find_program_address([bytes(b"STATE")], PID)
    lut_signer, _ = Pubkey.find_program_address([b"LutSigner", bytes(randomness)], PID)
    lut_seed = [bytes(lut_signer), struct.pack("<Q", current_slot)]
    lut, _ = Pubkey.find_program_address(lut_seed, ADDRESS_LOOKUP_TABLE_PROGRAM_ID)

    accounts = [
        AccountMeta(pubkey=randomness, is_signer=True, is_writable=True),
        AccountMeta(pubkey=reward_escrow, is_signer=False, is_writable=True),
        AccountMeta(pubkey=authority, is_signer=True, is_writable=True),
        AccountMeta(pubkey=QUEUE_ID, is_signer=False, is_writable=True),
        AccountMeta(pubkey=payer, is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=WSOL_MINT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=state, is_signer=False, is_writable=False),
        AccountMeta(pubkey=lut_signer, is_signer=False, is_writable=False),
        AccountMeta(pubkey=lut, is_signer=False, is_writable=True),
        AccountMeta(pubkey=ADDRESS_LOOKUP_TABLE_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

    DISCRIMINATOR = bytes.fromhex("0909cc213274710f")
    data = DISCRIMINATOR + struct.pack("<Q", current_slot)

    ix = Instruction(PID, data, accounts)
    return ix


def generate_commit_ix(
    randomness: Pubkey, oracle: Pubkey, authority: Pubkey, network: str = "mainnet-beta"
) -> Instruction:
    PID = ON_DEMAND_DEVNET_PID if network == "devnet" else ON_DEMAND_MAINNET_PID
    QUEUE_ID = ON_DEMAND_DEVNET_QUEUE if network == "devnet" else ON_DEMAND_MAINNET_QUEUE

    accounts = [
        AccountMeta(pubkey=randomness, is_signer=False, is_writable=True),
        AccountMeta(pubkey=QUEUE_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=oracle, is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYSTEM_RECENT_SLOT_HASH_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=authority, is_signer=True, is_writable=True),
    ]
    DISCRIMINATOR = bytes.fromhex("34aa98c9b385f28d")
    data = DISCRIMINATOR
    ix = Instruction(PID, data, accounts)
    return ix


def generate_reveal_ix(
    randomness: Pubkey,
    oracle: Pubkey,
    authority: Pubkey,
    payer: Pubkey,
    param: RandomnessRevealResponse,
    network: str = "mainnet-beta",
) -> Instruction:
    PID = ON_DEMAND_DEVNET_PID if network == "devnet" else ON_DEMAND_MAINNET_PID
    QUEUE_ID = ON_DEMAND_DEVNET_QUEUE if network == "devnet" else ON_DEMAND_MAINNET_QUEUE

    reward_escrow = get_associated_token_address(randomness, WSOL_MINT)

    stats_seed = b"OracleRandomnessStats"
    stats, _ = Pubkey.find_program_address([stats_seed, bytes(oracle)], PID)

    state, _ = Pubkey.find_program_address([bytes(b"STATE")], PID)
    accounts = [
        AccountMeta(pubkey=randomness, is_signer=False, is_writable=True),
        AccountMeta(pubkey=oracle, is_signer=False, is_writable=False),
        AccountMeta(pubkey=QUEUE_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=stats, is_signer=False, is_writable=True),
        AccountMeta(pubkey=authority, is_signer=True, is_writable=True),
        AccountMeta(pubkey=payer, is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYSTEM_RECENT_SLOT_HASH_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=reward_escrow, is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=WSOL_MINT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=state, is_signer=False, is_writable=False),
    ]

    DISCRIMINATOR = bytes.fromhex("c5b5bb0a1e3a1449")
    data = DISCRIMINATOR + param.to_bytes()
    ix = Instruction(PID, data, accounts)
    return ix

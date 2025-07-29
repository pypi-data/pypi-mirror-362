from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.signature import Signature
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solana.rpc.commitment import Processed
from solders.message import MessageV0
from sb_on_demand.instructions import (
    ON_DEMAND_DEVNET_QUEUE,
    ON_DEMAND_MAINNET_QUEUE,
    generate_commit_ix,
    generate_create_random_ix,
    generate_reveal_ix,
)
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price

from sb_on_demand.queue_account_utility import fetch_all_oracles, fetch_queue_account_data
import random

from sb_on_demand.randomness_account_utility import fetch_randomness_account_data
from sb_on_demand.oracle_account_utility import (
    FetchRandomnessRevealParams,
    fetch_oracle_account_data,
    fetch_randomness_reveal,
)


async def randomness_init(
    connection: AsyncClient, randomness_account: Keypair, payer: Keypair, authority: Keypair
) -> Signature:
    if "devnet" in connection._provider.endpoint_uri:
        network = "devnet"
    elif "mainnet-beta" in connection._provider.endpoint_uri:
        network = "mainnet-beta"
    else:
        raise ValueError("Unsupported network. Use devnet or mainnet-beta.")

    current_slot = (await connection.get_slot()).value

    recent_blockhash = (await connection.get_latest_blockhash(commitment=Processed)).value.blockhash

    init_ix = generate_create_random_ix(
        randomness=randomness_account.pubkey(),
        authority=authority.pubkey(),
        payer=payer.pubkey(),
        current_slot=current_slot,
        network=network,
    )

    msg = MessageV0.try_compile(
        payer=payer.pubkey(),
        instructions=[set_compute_unit_limit(120_000), set_compute_unit_price(100_000), init_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash,
    )
    if payer == authority:
        # If payer is the same as authority, we only need to sign with payer
        tx = VersionedTransaction(msg, [payer, randomness_account])
    else:
        tx = VersionedTransaction(msg, [payer, randomness_account, authority])
    resp = await connection.send_transaction(txn=tx, opts=TxOpts(skip_preflight=False, preflight_commitment=Processed))
    return resp.value


async def randomness_commit(
    connection: AsyncClient, randomness_account: Pubkey, payer: Keypair, authority: Keypair
) -> Signature:
    # Determine network from endpoint URI
    if "devnet" in connection._provider.endpoint_uri:
        network = "devnet"
    elif "mainnet-beta" in connection._provider.endpoint_uri:
        network = "mainnet-beta"
    else:
        raise ValueError("Unsupported network. Use devnet or mainnet-beta.")
    QUEUE_ID = ON_DEMAND_DEVNET_QUEUE if network == "devnet" else ON_DEMAND_MAINNET_QUEUE

    queue_data = await fetch_queue_account_data(connection, QUEUE_ID)
    available_oracles = await fetch_all_oracles(connection, queue_data)

    if not available_oracles:
        raise Exception("No available oracles found.")

    selected_oracle = random.choice(available_oracles)

    commit_ix = generate_commit_ix(
        randomness=randomness_account,
        oracle=selected_oracle,
        authority=authority.pubkey(),
        network=network,
    )

    recent_blockhash = (await connection.get_latest_blockhash(commitment=Processed)).value.blockhash
    msg = MessageV0.try_compile(
        payer=payer.pubkey(),
        instructions=[set_compute_unit_limit(20_000), set_compute_unit_price(100_000), commit_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash,
    )
    if payer == authority:
        # If payer is the same as authority, we only need to sign with payer
        tx = VersionedTransaction(msg, [payer])
    else:
        tx = VersionedTransaction(msg, [payer, authority])
    resp = await connection.send_transaction(txn=tx, opts=TxOpts(skip_preflight=False, preflight_commitment=Processed))
    return resp.value


async def randomness_reveal(
    connection: AsyncClient, randomness_account: Pubkey, payer: Keypair, authority: Keypair
) -> Signature:
    # Determine network from endpoint URI
    if "devnet" in connection._provider.endpoint_uri:
        network = "devnet"
    elif "mainnet-beta" in connection._provider.endpoint_uri:
        network = "mainnet-beta"
    else:
        raise ValueError("Unsupported network. Use devnet or mainnet-beta.")
    # find the oracle in commit
    randomness_account_data = await fetch_randomness_account_data(connection, randomness_account)
    oracle = randomness_account_data.oracle
    if not oracle:
        raise Exception("No oracle found for the randomness account.")

    # get api gateway for the oracle
    oracle_data = await fetch_oracle_account_data(connection, oracle)
    gateway_url = oracle_data.gateway_uri
    if not gateway_url:
        raise Exception("No gateway URL found for the oracle.")

    # get the randomness reveal parameters from the randomness account data
    param = FetchRandomnessRevealParams(
        randomnessAccount=randomness_account,
        slothash=randomness_account_data.seed_slothash,
        slot=int(randomness_account_data.seed_slot) & 0xFFFFFFFF,
        rpc=connection._provider.endpoint_uri,
    )
    # get the randomness reveal response from the oracle's gateway
    reveal_api_resp = await fetch_randomness_reveal(gateway_url, param)

    # send the reveal instruction to the on-demand program
    reveal_ix = generate_reveal_ix(
        randomness=randomness_account,
        oracle=oracle,
        authority=authority.pubkey(),
        payer=payer.pubkey(),
        param=reveal_api_resp,
        network=network,
    )

    recent_blockhash = (await connection.get_latest_blockhash(commitment=Processed)).value.blockhash
    msg = MessageV0.try_compile(
        payer=payer.pubkey(),
        instructions=[set_compute_unit_limit(60_000), set_compute_unit_price(100_000), reveal_ix],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash,
    )
    if payer == authority:
        # If payer is the same as authority, we only need to sign with payer
        tx = VersionedTransaction(msg, [payer])
    else:
        tx = VersionedTransaction(msg, [payer, authority])
    resp = await connection.send_transaction(txn=tx, opts=TxOpts(skip_preflight=False, preflight_commitment=Processed))
    return resp.value

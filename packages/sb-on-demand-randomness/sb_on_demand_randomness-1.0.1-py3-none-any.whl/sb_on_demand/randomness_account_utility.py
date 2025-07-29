from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed
from sb_on_demand.randomness_account_data import RandomnessAccountData
from sb_on_demand.randomness_account_data_layout import RandomnessAccountDataLayout


async def fetch_randomness_account_data(connection: AsyncClient, randomness: Pubkey) -> RandomnessAccountData:
    account_info = await connection.get_account_info(randomness, commitment=Processed)
    if account_info.value and account_info.value.data:
        data_bytes = account_info.value.data
        parsed = RandomnessAccountDataLayout.parse(data_bytes)
        return RandomnessAccountData(parsed)
    return None

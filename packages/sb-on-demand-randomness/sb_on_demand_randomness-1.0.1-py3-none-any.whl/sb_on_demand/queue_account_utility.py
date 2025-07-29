from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.constants import SYSTEM_PROGRAM_ID
from sb_on_demand.queue_account_data import QueueAccountData
from sb_on_demand.queue_account_data_layout import QueueAccountDataLayout


async def fetch_queue_account_data(connection: AsyncClient, queue: Pubkey) -> QueueAccountData:
    account_info = await connection.get_account_info(queue)
    if account_info.value and account_info.value.data:
        data_bytes = account_info.value.data
        parsed = QueueAccountDataLayout.parse(data_bytes)
        return QueueAccountData(parsed)
    return None


async def fetch_all_oracles(connection: AsyncClient, queue_data: QueueAccountData) -> list[Pubkey]:
    if queue_data:
        return [oracle for oracle in queue_data.oracle_keys if oracle != SYSTEM_PROGRAM_ID]
    return []

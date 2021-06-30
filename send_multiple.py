import logging
from flow_py_sdk import (
    cadence,
    flow_client,
    SignAlgo,
    HashAlgo,
    AccountKey,
    create_account_template,
    Tx,
    ProposalKey,
    Script
)
import pandas as pd
from config import Config
import asyncio
from pathlib import Path
from datetime import date

logger = logging.getLogger(__name__)
ctx = Config()

async def send_multiple(addresses_arg: cadence.Dictionary):
    async with flow_client(
        host=ctx.access_node_host, port=ctx.access_node_port
    ) as client:
        block = await client.get_latest_block()
        proposer = await client.get_account_at_latest_block(
            address=ctx.service_account_address.bytes
        )
        tx = Tx(
            code=open(Path(__file__).parent.joinpath(
                "./transfer_many_accounts.cdc"))
            .read(),
            reference_block_id=block.id,
            payer=ctx.service_account_address,
            proposal_key=ProposalKey(
                key_address=ctx.service_account_address,
                key_id=ctx.service_account_key_id,
                key_sequence_number=proposer.keys[
                    ctx.service_account_key_id
                ].sequence_number,
            ),
        ).add_authorizers(
            ctx.service_account_address
        ).add_arguments(
            addresses_arg
        ).with_gas_limit(
            9999
        ).with_envelope_signature(
            ctx.service_account_address,
            ctx.service_account_key_id,
            ctx.service_account_signer,
        )
        await client.execute_transaction(tx)

async def main(path:str, total:float):
    """
    path: csv路径
    total: 要分发的总数
    """
    df = pd.read_csv(path)
    df['比例'] =  df['占比'] / df['占比'].sum()
    distribution = list(
        map(
            lambda row:{'key':row[3],'value':round(row[4]*total,8)},
            df.to_records()
        )
    )
    pd.DataFrame.from_records(distribution).to_csv(f'record-{date.today()}.csv')
    addresses_arg = cadence.Dictionary(
        list(map(lambda i:cadence.KeyValuePair(
                cadence.Address.from_hex(i['key']), 
                cadence.UFix64(i['value']*1e8) # 100*1e-8 Flow
            ) , distribution))
    )
    await send_multiple(addresses_arg)

if __name__ == "__main__":
    asyncio.run(main('flow_test.csv',0.03))
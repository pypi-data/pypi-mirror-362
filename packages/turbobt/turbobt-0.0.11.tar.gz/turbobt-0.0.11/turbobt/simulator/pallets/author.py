import asyncio
import json

import scalecodec
import scalecodec.utils.ss58

from turbobt.simulator import db
from turbobt.substrate.pallets._base import Pallet


class Author(Pallet):
    def __init__(self, substrate):
        super().__init__(substrate)

        self._subscriptions = {}

    async def unwatchExtrinsic(self, bytes):
        self._subscriptions.pop(bytes, None)

    async def submitAndWatchExtrinsic(self, bytes):
        extrinsic_cls = self.substrate._registry.get_decoder_class("Extrinsic")
        extrinsic_obj = extrinsic_cls(
            data=scalecodec.ScaleBytes(bytes),
            metadata=self.substrate._metadata,
        )
        extrinsic = extrinsic_obj.decode()

        async with self.substrate.session_async() as session:
            extrinsic_model = db.Extrinsic(
                account_id=scalecodec.utils.ss58.ss58_encode(extrinsic["address"]),
                # block=db.Block.query_current(session).scalar_subquery(),
                block=1,
                call_args=json.dumps(extrinsic["call"]["call_args"]),
                call_function=extrinsic["call"]["call_function"],
                call_module=extrinsic["call"]["call_module"],
                era_current=extrinsic["era"][1],
                era_period=extrinsic["era"][0],
                nonce=extrinsic["nonce"],
                signature=extrinsic["signature"]["Sr25519"],
                tip=extrinsic["tip"],
            )

            session.add(extrinsic_model)
            await session.commit()

            extrinsic_id = f"0x{extrinsic_model.id.to_bytes().hex()}"
            extrinsic_block = extrinsic_model.block

        call_module = getattr(self.substrate, extrinsic["call"]["call_module"])
        call_function = getattr(call_module, extrinsic["call"]["call_function"])
        call_args = {
            arg["name"]: (
                scalecodec.utils.ss58.ss58_encode(arg["value"])
                if arg["type"] == "AccountId"
                else arg["value"]
            )
            for arg in extrinsic["call"]["call_args"]
        }

        await call_function(
            scalecodec.utils.ss58.ss58_encode(extrinsic["address"]),
            **call_args,
        )

        subscription = asyncio.Queue()
        subscription.put_nowait("ready")
        subscription.put_nowait(
            {
                "broadcast": [
                    "12D3KooWQgG8BL8VB6aXdzvnadkbJiQ6HnoxjSjrD9kuXuGGhP46",
                ],
            },
        )

        # TODO next upcoming block?
        subscription.put_nowait(
            {
                "inBlock": db.Block.get_hash(extrinsic_block),
            },
        )
        subscription.put_nowait(
            {
                "finalized": db.Block.get_hash(extrinsic_block),
            },
        )

        self._subscriptions[extrinsic_id] = subscription

        return extrinsic_id

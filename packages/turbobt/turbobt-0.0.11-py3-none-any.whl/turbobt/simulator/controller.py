import json

import sqlalchemy

from turbobt.simulator import MockedSubtensor, db


class Controller:
    def __init__(self, subtensor: MockedSubtensor):
        self.subtensor = subtensor

    # TODO pytest.raises (for testing extrinsics)
    # TODO pytest-httpx?

    async def wait_for_epoch(self):
        await self._on_epoch()

    async def _on_epoch(self):
        async with self.subtensor.session_async() as session:
            subnets = await session.execute(sqlalchemy.select(db.Subnet))

            for subnet in subnets.scalars():
                # https://github.com/opentensor/subtensor/blob/4c9836f8cc199bc323956509f59d86d1761dd021/pallets/subtensor/src/coinbase/run_coinbase.rs#L858
                # TODO No commits to reveal until at least epoch 2.

                reveal_epoch = 1    # TODO

                # TODO
                # expired_commits = session.query(db.CRV3WeightCommits).filter(
                #     db.CRV3WeightCommits.netuid == subnet.netuid,
                #     db.CRV3WeightCommits.reveal_round < reveal_epoch,
                # )
                # expired_commits.delete()

                commits = await session.execute(
                    sqlalchemy.select(db.CRV3WeightCommits).filter_by(
                        netuid=subnet.netuid,
                        commit_epoch=reveal_epoch,
                    ),
                )

                for commit in commits.scalars():
                    commit_data = json.loads(commit.commit)

                    # XXX do_set_weights
                    weights = [
                        db.Weights(
                            block=1,    #TODO
                            netuid=subnet.netuid,
                            validator=0,  # TODO uid
                            uid=uid,
                            weight=weight,
                        )
                        for uid, weight in zip(
                            commit_data["uids"],
                            commit_data["weights"],
                        )
                    ]

                    session.add_all(weights)

                # commits.delete()
                await session.commit()

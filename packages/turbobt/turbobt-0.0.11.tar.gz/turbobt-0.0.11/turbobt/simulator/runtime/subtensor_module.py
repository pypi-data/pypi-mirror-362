import ipaddress
import typing

import sqlalchemy

from turbobt.simulator import db
from turbobt.subtensor.exceptions import (
    HotKeyAlreadyRegisteredInSubNet,
    HotKeyNotRegisteredInNetwork,
)

AccountId = typing.TypeAlias = str


class SubtensorModule:
    def __init__(self, substrate):
        self.substrate = substrate

    async def burned_register(self, who, netuid: int, hotkey: AccountId):
        async with self.substrate.session_async() as session:
            neuron = await session.execute(
                sqlalchemy.select(db.Neuron).filter_by(
                    netuid=netuid,
                    hotkey=hotkey,
                ),
            )

            if neuron.scalar_one_or_none():
                raise HotKeyAlreadyRegisteredInSubNet

            neuron = db.Neuron(
                active=True,    # TODO?
                # block=db.Block.query_current(session).scalar_subquery(),
                block=1,
                coldkey=who,
                hotkey=hotkey,
                netuid=netuid,
            )

            session.add(neuron)
            await session.commit()

    async def commit_crv3_weights(self, who: str, netuid: int, commit: str, reveal_round: int):
        current_epoch = 1   # TODO

        async with self.substrate.session_async() as session:
            commits = await session.execute(
                sqlalchemy.select(db.CRV3WeightCommits).filter_by(
                    netuid=netuid,
                    commit_epoch=current_epoch,
                    who=who,
                ),
            )

            # if commits.count() >= 10:
            #     raise RuntimeError("TooManyUnrevealedCommits")

            commit_model = db.CRV3WeightCommits(
                netuid=netuid,
                commit_epoch=current_epoch,
                who=who,
                commit=commit.encode(),
                reveal_round=reveal_round,
            )

            session.add(commit_model)
            await session.commit()

        # https://github.com/opentensor/subtensor/blob/4c9836f8cc199bc323956509f59d86d1761dd021/pallets/subtensor/src/subnets/weights.rs#L229

    async def register_network(
        self,
        who,
        hotkey: str,
    ):
        # https://github.com/opentensor/subtensor/blob/9f33e759acd763497135043504dc048dcc599c31/pallets/subtensor/src/subnets/subnet.rs#L117

        async with self.substrate.session_async() as session:
            subnet = db.Subnet(
                block=1,  # TODO
                name="Test Network",
                token_symbol="T",
                owner_coldkey=hotkey,
                owner_hotkey=hotkey,
                tempo=360,
                identity="Test Identity",
            )

            session.add(subnet)
            await session.commit()

            subnet_hyperparams = db.SubnetHyperparams(
                block=subnet.block,
                netuid=subnet.netuid,
            )

            # Add the caller to the neuron set
            neuron = db.Neuron(
                active=True,    # TODO?
                block=subnet.block,
                coldkey=who,
                hotkey=hotkey,
                netuid=subnet.netuid,
                uid=0,
            )

            session.add(subnet_hyperparams)
            session.add(neuron)
            await session.commit()

    async def serve_axon(
        self,
        who,
        netuid: int,
        version: int,
        ip: int,
        port: int,
        ip_type: int,
        protocol: int,
        placeholder1: int,
        placeholder2: int,
    ):
        async with self.substrate.session_async() as session:
            neuron_id = await session.execute(
                sqlalchemy.select(db.Neuron.uid).filter_by(
                    netuid=netuid,
                    hotkey=who,    # cold?
                ).order_by(
                    db.Neuron.block.desc(),
                ).limit(1)
            )
            neuron_id = neuron_id.scalar_one_or_none()

            if neuron_id is None:
                raise HotKeyNotRegisteredInNetwork
            
            axon_info = db.AxonInfo(
                block=1,  # TODO
                ip=str(ipaddress.ip_address(ip)),
                netuid=netuid,
                port=port,
                protocol=protocol,
                uid=neuron_id,
            )

            session.add(axon_info)
            await session.commit()

    async def serve_axon_tls(
        self,
        who,
        netuid: int,
        version: int,
        ip: int,
        port: int,
        ip_type: int,
        protocol: int,
        placeholder1: int,
        placeholder2: int,
        certificate: bytes,
    ):
        await self.serve_axon(
            who,
            netuid,
            version,
            ip,
            port,
            ip_type,
            protocol,
            placeholder1,
            placeholder2,
        )

        async with self.substrate.session_async() as session:
            neuron_certificate = db.NeuronCertificate(
                block=1,  # TODO
                hotkey=who,
                netuid=netuid,
                algorithm=ord(certificate[0]),
                public_key=certificate[1:],
            )

            session.add(neuron_certificate)
            await session.commit()

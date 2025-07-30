import hashlib
import json

from sqlalchemy import ForeignKey, Identity, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


def default_block_hash(context):
    return Block.get_hash(context.get_current_parameters()["number"])


class Block(Base):
    __tablename__ = 'Blocks'

    number: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(
        default=default_block_hash, # TODO computed?
        index=True,
        unique=True,
    )

    @classmethod
    def get_hash(cls, block_number: int):
        return f"0x{hashlib.sha256(bytes(block_number)).hexdigest()}"

    @classmethod
    def query(cls, block: str | int | None = None):
        # TODO limit(1)

        if isinstance(block, int):
            return select(cls).filter_by(number=block).limit(1)

        if isinstance(block, str):
            return select(cls).filter_by(hash=block).limit(1)

        return select(cls).order_by(cls.number.desc()).limit(1)


class Extrinsic(Base):
    __tablename__ = 'Extrinsics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))

    account_id: Mapped[str]
    call_args: Mapped[str]  # TODO type
    call_function: Mapped[str]
    call_module: Mapped[str]
    era_current: Mapped[int]
    era_period: Mapped[int]
    nonce: Mapped[int]
    signature: Mapped[str]
    tip: Mapped[int]
    # mode

    def encode(self, substrate):
        extrinsic = substrate._registry.create_scale_object(
            "Extrinsic",
            metadata=substrate._metadata,
        )
        extrinsic.encode(
            {
                "account_id": self.account_id,
                "asset_id": {"tip": self.tip, "asset_id": None},
                "call_args": json.loads(self.call_args),
                "call_function": self.call_function,
                "call_module": self.call_module,
                "era": {
                    "current": self.era_current,
                    "period": self.era_period,
                },
                "mode": "Disabled",
                "nonce": self.nonce,
                "signature_version": 1,
                "signature": self.signature,
                "tip": self.tip,
            },
        )

        return str(extrinsic.data)


class Subnet(Base):
    __tablename__ = 'Subnets'

    netuid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))
    name: Mapped[str]
    token_symbol: Mapped[str]
    owner_coldkey: Mapped[str]
    owner_hotkey: Mapped[str]
    tempo: Mapped[int]
    identity: Mapped[str]


class SubnetHyperparams(Base):
    __tablename__ = 'SubnetHyperparams'

    netuid: Mapped[int] = mapped_column(primary_key=True)
    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))
    activity_cutoff: Mapped[int] = 5000


class Neuron(Base):
    __tablename__ = 'Neurons'

    uid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, server_default=Identity(start=5, increment=1))
    netuid: Mapped[int] = mapped_column(ForeignKey('Subnets.netuid'))
    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))
    active: Mapped[bool]
    coldkey: Mapped[str]
    hotkey: Mapped[str]
    consensus: Mapped[int] = 0
    dividends: Mapped[int] = 0
    emission: Mapped[int] = 0
    incentive: Mapped[int] = 0
    last_update: Mapped[int] = 0
    pruning_score: Mapped[int] = 65535
    rank: Mapped[int] = 0
    trust: Mapped[int] = 0
    validator_permit: Mapped[bool] = False
    validator_trust: Mapped[int] = 0

    axon_info: Mapped["AxonInfo"] = relationship(back_populates="neuron")
    certificate: Mapped["NeuronCertificate"] = relationship(back_populates="neuron")


class NeuronCertificate(Base):
    __tablename__ = 'NeuronCertificates'

    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'), primary_key=True)
    netuid: Mapped[int] = mapped_column(ForeignKey('Subnets.netuid'), primary_key=True)
    hotkey: Mapped[str] = mapped_column(ForeignKey('Neurons.hotkey'), primary_key=True)
    algorithm: Mapped[int]
    public_key: Mapped[bytes]

    neuron: Mapped["Neuron"] = relationship(back_populates="certificate")


class AxonInfo(Base):
    __tablename__ = 'AxonInfo'

    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))
    uid: Mapped[int] = mapped_column(ForeignKey('Neurons.uid'), primary_key=True)
    netuid: Mapped[int] = mapped_column(ForeignKey('Subnets.netuid'))
    ip: Mapped[str]
    port: Mapped[int]
    protocol: Mapped[int]

    neuron: Mapped["Neuron"] = relationship(back_populates="axon_info")


#XXX
class StorageDoubleMap(Base):
    __tablename__ = 'StorageDoubleMap'

    module: Mapped[str]
    storage: Mapped[str]
    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))

    key1: Mapped[int] = mapped_column(primary_key=True)
    key2: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[bytes] = mapped_column(nullable=True)


class CRV3WeightCommits(Base):
    __tablename__ = 'CRV3WeightCommits'

    netuid: Mapped[int] = mapped_column(primary_key=True)
    commit_epoch: Mapped[int] = mapped_column(primary_key=True)
    who: Mapped[str]
    commit: Mapped[bytes]
    reveal_round: Mapped[int]


class Weights(Base):
    __tablename__ = 'Weights'

    block: Mapped[int] = mapped_column(ForeignKey('Blocks.number'))
    netuid: Mapped[int] = mapped_column(primary_key=True)
    validator: Mapped[int] = mapped_column(primary_key=True)

    uid: Mapped[int]
    weight: Mapped[int]

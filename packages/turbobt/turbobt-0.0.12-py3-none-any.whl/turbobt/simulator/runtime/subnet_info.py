import sqlalchemy
import scalecodec.utils.ss58

from turbobt.simulator import db


class SubnetInfoRuntimeApi:
    def __init__(self, substrate):
        self.substrate = substrate

    async def get_dynamic_info(
        self,
        netuid: int,
        block_hash=None,
    ):
        async with self.substrate.session_async() as session:
            subnet = await session.execute(
                sqlalchemy.select(db.Subnet).filter_by(netuid=netuid).order_by(db.Subnet.block.desc())
            )
            subnet = subnet.scalar_one_or_none()

        if not subnet:
            return None

        return {
            "subnet_name": subnet.name.encode(),
            "token_symbol": subnet.token_symbol.encode(),
            "owner_coldkey": "0x" + scalecodec.utils.ss58.ss58_decode(subnet.owner_coldkey),
            "owner_hotkey": "0x" + scalecodec.utils.ss58.ss58_decode(subnet.owner_hotkey),
            "tempo": subnet.tempo,
            "subnet_identity": subnet.identity,
        }

    async def get_subnet_hyperparams(self, subnet: int, block_hash: str | None):
        # TODO hash

        async with self.substrate.session_async() as session:
            subnet_hyperparams = await session.execute(
                sqlalchemy.select(db.SubnetHyperparams).filter_by(
                    netuid=subnet,
                ).order_by(
                    db.SubnetHyperparams.block.desc(),
                ).limit(1),
            )
            subnet_hyperparams = subnet_hyperparams.scalar_one_or_none()
        
        if not subnet_hyperparams:
            return None

        return {
            "activity_cutoff": subnet_hyperparams.activity_cutoff,
            "adjustment_alpha": 0,
            "adjustment_interval": 100,
            "alpha_high": 58982,
            "alpha_low": 45875,
            "bonds_moving_avg": 900000,
            "commit_reveal_period": 1,
            "commit_reveal_weights_enabled": False,
            "difficulty": 10000000,
            "immunity_period": 4096,
            "kappa": 32767,
            "liquid_alpha_enabled": False,
            "max_burn": 100000000000,
            "max_difficulty": 4611686018427387903,
            "max_regs_per_block": 1,
            "max_validators": 64,
            "max_weights_limit": 65535,
            "min_allowed_weights": 0,
            "min_burn": 500000,
            "min_difficulty": 10000000,
            "registration_allowed": True,
            "rho": 10,
            "serving_rate_limit": 50,
            "target_regs_per_interval": 2,
            "tempo": 100,
            "weights_rate_limit": 100,
            "weights_version": 0,
        }

import scalecodec.utils.ss58
import sqlalchemy

from turbobt.simulator import db


class NeuronInfoRuntimeApi:
    def __init__(self, substrate):
        self.substrate = substrate

    async def get_neurons_lite(self, netuid: int, block_hash: str | None):
        async with self.substrate.session_async() as session:
            neurons = await session.execute(
                sqlalchemy.select(db.Neuron).filter_by(
                    netuid=netuid,
                    block=1, # TODO ==
                ),
            )

            return [
                {
                    "active": neuron.active,
                    "coldkey": "0x" + scalecodec.utils.ss58.ss58_decode(neuron.coldkey),
                    "hotkey": "0x" + scalecodec.utils.ss58.ss58_decode(neuron.hotkey),
                    "uid": neuron.uid,
                    "netuid": neuron.netuid,
                    "stake": [
                        (
                            "0x"
                            + scalecodec.utils.ss58.ss58_decode(
                                neuron.coldkey
                            ),  # coldkey?
                            0,
                        ),
                    ],
                    "axon_info": {
                        "ip": neuron.axon_info.ip,
                        "port": neuron.axon_info.port,
                        "protocol": neuron.axon_info.protocol,
                    }
                    # if await neuron.awaitable_attrs.axon_info
                    if False
                    else {
                        "ip": "0.0.0.0",
                        "port": 0,
                        "protocol": 0,
                    },
                    "consensus": neuron.consensus,
                    "dividends": neuron.dividends,
                    "emission": neuron.emission,
                    "incentive": neuron.incentive,
                    "last_update": neuron.last_update,
                    "prometheus_info": {
                        "ip": "0.0.0.0",
                        "port": 0,
                    },
                    "pruning_score": neuron.pruning_score,
                    "rank": neuron.rank,
                    "trust": neuron.trust,
                    "validator_permit": neuron.validator_permit,
                    "validator_trust": neuron.validator_trust,
                }
                for neuron in neurons.scalars()
            ]

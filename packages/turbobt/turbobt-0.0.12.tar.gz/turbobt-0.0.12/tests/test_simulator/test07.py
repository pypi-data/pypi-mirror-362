import turbobt
import bittensor_wallet


async def main():
    wallet = bittensor_wallet.Wallet("luxor-validator", "default")
    # wallet = bittensor_wallet.Wallet("alice", "default")

    # async with turbobt.Bittensor("wss://test.finney.opentensor.ai:443", wallet=wallet) as bt:
    async with turbobt.Bittensor("ws://localhost:9944", wallet=wallet) as bt:
        # subnet = bt.subnet(388)
        subnet = bt.subnet(1)
        neurons = await subnet.list_neurons()

        await subnet.neurons.serve(
            ip="192.168.0.2",
            port=8000,
        )

        neuron = await subnet.get_neuron(wallet.hotkey.ss58_address)

        print(neurons)

        neuron = await bt.subtensor.neuron_info.get_neuron(
            netuid=2,
            uid=1,
        )

        print(neuron)

        # await bt.subtensor.admin_utils.sudo_set_commit_reveal_weights_enabled(
        #     netuid=subnet.netuid,
        #     enabled=True,
        #     wallet=wallet,
        # )

        await subnet.weights.set({
            # 0: 0,
            # 1: 0.8,
        })

        for i in range(10):
            # weights = await subnet.weights.fetch_pending()
            # print(weights)
            neuron = await bt.subtensor.neuron_info.get_neuron(
                netuid=2,
                uid=0,
            )

            print(neuron["weights"])

            await asyncio.sleep(0.1)


import asyncio

asyncio.run(main())
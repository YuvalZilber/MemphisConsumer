import asyncio
import atexit
import contextlib
import glob
import json
import logging
import os
import sys
import uuid
from memphis import Memphis
from memphis.memphis import Consumer
from filelock import FileLock

logger = logging.getLogger(__file__)
my_id = str(uuid.uuid4())[:30]
loop = asyncio.get_event_loop()
f = loop.create_future()

print(sys.argv, file=sys.stderr)
# noinspection PyTypeChecker
args = dict(enumerate(sys.argv[1:]))

debug = args.get(2, "true")


def log(*args, **kwargs):
    if debug.lower() == "true":
        print(*args, **kwargs)


@atexit.register
def close():
    loop.run_until_complete(_close())


def remove_lockfile():
    for file in glob.glob("out/*.lock"):
        os.remove(file)


async def _close():
    await loop.shutdown_asyncgens()


@contextlib.asynccontextmanager
async def open_memphis(**kwargs):
    memphis = Memphis()
    try:
        await memphis.connect(**kwargs)
        yield memphis
    finally:
        await memphis.close()


def process(data_json, file):
    log("consume:", data_json["row"])
    if data_json["last"]:
        print("im the last consumer, last line:", data_json["row"])

    print(", ".join(data_json["row"]), file=file)


async def handle_messages(msgs, output_file):
    with FileLock(output_file.replace(".csv", ".lock")):
        with open(output_file, "a") as file:
            for msg in msgs:
                data_str = msg.get_data().decode()
                data_json = json.loads(data_str)
                process(data_json, file)
                await msg.ack()


async def handle_error(error):
    if hasattr(error, "message") and error.message == "Memphis: TimeoutError":
        log("Nothing new")
    else:
        log("# " + repr(error))


async def main():
    local_path = args[0].replace("^~/", "")

    output_file = f"./out/{local_path}"
    print("output_file =", output_file)
    station = args[1]

    async def handle(msgs, error):
        if msgs:
            await handle_messages(msgs, output_file)
        if error:
            await handle_error(error)

    async with open_memphis(host="localhost", username="root", connection_token="memphis") as memphisConnection:
        consumer: Consumer = await memphisConnection.consumer(
            station_name=station, consumer_name=f"{my_id}", consumer_group=station, max_msg_deliveries=1)
        consumer.consume(handle)

        await asyncio.wait([f])


if __name__ == '__main__':
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt as e:
        log("bye :)", e)

import subprocess
import os
import asyncio
import time
async def read_output(stream):
    output = b""
    while True:
        line = await stream.read(4096)
        if not line:
            break
        output += line

    return output

async def main():
    directory = os.path.join("MoveGenerator", "connect4", "c4solver.exe")

    process = subprocess.Popen([directory, "-", "w"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, )
    print("first")
    
    print("second")
    process.stdin.write("123456712345671234567\n".encode("utf-8"))
    process.stdin.flush()

    time.sleep(10)
    print("Waiting for output...")
    output = await read_output(process.stdout)
    output = output.decode("utf-8")

    process.stdin.close()
    process.stdout.close()
    process.terminate()

    print(output)

asyncio.run(main())
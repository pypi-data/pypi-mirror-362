# ruff: noqa: INP001,D100,D103

import os
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio

import testthing


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def machine() -> AsyncGenerator[testthing.VirtualMachine]:
    image = os.getenv("TEST_IMAGE")
    if not image:
        raise RuntimeError("TEST_IMAGE environment variable must be set")
    private = Path(__file__).parent / "identity"
    private.chmod(0o600)  # ssh will ignore it otherwise
    public = Path(__file__).parent / "identity.pub"
    with testthing.IpcDirectory() as ipc:
        async with testthing.VirtualMachine(
            image, ipc=ipc, identity=(private, public.read_text().strip())
        ) as vm:
            yield vm


@pytest.mark.asyncio(loop_scope="module")
async def test_reboot(machine: testthing.VirtualMachine) -> None:
    await (machine.root / "etc/marker").write_text("hi")
    await (machine.root / "tmp/marker").write_text("hi")
    await machine.reboot()


@pytest.mark.asyncio(loop_scope="module")
async def test_path(machine: testthing.VirtualMachine) -> None:
    textfile = machine.root / "tmp" / "textfile"
    await textfile.write_text("hihi")
    await textfile.write_text("byebye", append=True)
    assert await textfile.read_text() == "hihibyebye"
    await textfile.unlink()


@pytest.mark.asyncio(loop_scope="module")
async def test_cat_os_release(machine: testthing.VirtualMachine) -> None:
    assert "PRETTY_NAME" in await machine.execute("cat", "/etc/os-release")
    assert "PRETTY_NAME" in await machine.execute("cat", "/etc/os-release", direct=True)
    assert "PRETTY_NAME" in await machine.execute("cat /etc/os-release")
    assert "PRETTY_NAME" in await machine.execute("cat", ("/etc/os-release",))


@pytest.mark.asyncio(loop_scope="module")
async def test_script(machine: testthing.VirtualMachine) -> None:
    # We should be able to run shell scripts as well, if we give a single argument
    result = await machine.execute(
        """
        read name
        echo "${GREETING}, ${name}!"
    """,
        environment={"GREETING": "Hello"},
        input="rhubarb\n",
    )
    assert result == "Hello, rhubarb!\n"

    # If we specify multiple arguments then the arguments will be quoted.  With
    # ssh this is double-quoting, but it still ought to produce the same
    # result...
    result = await machine.execute(
        "sh",
        (
            "-c",
            """
                read name
                echo "${GREETING}, ${name}!"
            """,
        ),
        environment={"GREETING": "Hello"},
        input="rhubarb\n",
    )
    assert result == "Hello, rhubarb!\n"


@pytest.mark.asyncio(loop_scope="module")
async def test_check(machine: testthing.VirtualMachine) -> None:
    assert await machine.execute("true") == ""

    with pytest.raises(testthing.SubprocessError):
        await machine.execute("false")

    assert await machine.execute("false", check=False) == ""

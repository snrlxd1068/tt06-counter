# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1

    dut._log.info("Testing Up Counter...")
    dut.ui_in.value = 1  # ui_in[0] set to 1

    expected_values = [1, 2, 3, 0]
    for val in expected_values:
        await ClockCycles(dut.clk, 1)
        # We only care about the lower 2 bits of uo_out
        actual_val = dut.uo_out[1:0].value.integer
        assert actual_val == val
        dut._log.info(f"Up Count: {actual_val}")

    # 4. Test Down Counting (ui_in[0] = 0)
    dut._log.info("Testing Down Counter...")
    dut.ui_in.value = 0  # ui_in[0] set to 0
    
    # Current state is 0, next should be 3, 2, 1, 0
    expected_values = [3, 2, 1, 0]
    for val in expected_values:
        actual_val = dut.uo_out[1:0].value.integer
        assert actual_val == val
        dut._log.info(f"Down Count: {actual_val}")

    dut._log.info("All tests passed!")

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

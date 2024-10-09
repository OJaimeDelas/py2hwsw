# SPDX-FileCopyrightText: 2024 IObundle
#
# SPDX-License-Identifier: MIT


def setup(py_params_dict):
    # user-passed parameters
    params = py_params_dict["iob_system_params"]

    attributes_dict = {
        "version": "0.1",
        #
        # Configuration
        #
        "confs": [
            {
                "name": "AXI_ID_W",
                "descr": "AXI ID bus width",
                "type": "F",
                "val": "4",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_LEN_W",
                "descr": "AXI burst length width",
                "type": "F",
                "val": "8",
                "min": "1",
                "max": "8",
            },
            {
                "name": "AXI_ADDR_W",
                "descr": "AXI address bus width",
                "type": "F",
                "val": "`DDR_ADDR_W" if params["use_extmem"] else "20",
                "min": "1",
                "max": "32",
            },
            {
                "name": "AXI_DATA_W",
                "descr": "AXI data bus width",
                "type": "F",
                "val": "`DDR_DATA_W",
                "min": "1",
                "max": "32",
            },
        ],
    }

    #
    # Ports
    #
    attributes_dict["ports"] = [
        {
            "name": "clk_rst_i",
            "descr": "Clock and reset",
            "signals": [
                {"name": "clk", "direction": "input", "width": "1"},
                {"name": "arst", "direction": "input", "width": "1"},
            ],
        },
        {
            "name": "rs232",
            "descr": "Serial port",
            "signals": [
                {"name": "txd", "direction": "output", "width": "1"},
                {"name": "rxd", "direction": "input", "width": "1"},
            ],
        },
    ]

    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "ps_clk_arstn",
            "descr": "Clock and reset",
            "signals": [
                {"name": "ps_clk", "width": "1"},
                {"name": "ps_arstn", "width": "1"},
            ],
        },
        {
            "name": "ps_clk_rst",
            "descr": "Clock and reset",
            "interface": {
                "type": "clk_rst",
            },
        },
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "interface": {
                "type": "clk_en_rst",
            },
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "interface": {
                "type": "rs232",
            },
        },
        {
            "name": "axi",
            "descr": "AXI interface to connect SoC to memory",
            "interface": {
                "type": "axi",
                "ID_W": "AXI_ID_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LEN_W": "AXI_LEN_W",
            },
        },
        {
            "name": "intercon_m_clk_rst",
            "descr": "AXI interconnect clock and reset inputs",
            "interface": {
                "type": "clk_rst",
                "wire_prefix": "intercon_m_",
            },
        },
        {
            "name": "ps_axi",
            "descr": "AXI bus to connect interconnect and memory",
            "interface": {
                "type": "axi",
                "wire_prefix": "mem_",
                "ID_W": "AXI_ID_W",
                "LEN_W": "AXI_LEN_W",
                "ADDR_W": "AXI_ADDR_W",
                "DATA_W": "AXI_DATA_W",
                "LOCK_W": 1,
            },
        },
    ]

    #
    # Blocks
    #
    attributes_dict["blocks"] = [
        {
            # IOb-SoC Memory Wrapper
            "core_name": "iob_system_mwrap",
            "instance_name": "iob_system_mwrap",
            "instance_description": "IOb-SoC instance",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_en_rst_s": "clk_en_rst",
                "rs232_m": "rs232_int",
                "axi_m": "axi",
            },
            "dest_dir": "hardware/common_src",
            "iob_system_params": params,
        },
        {
            "core_name": "xilinx_axi_interconnect",
            "instance_name": "axi_async_bridge",
            "instance_description": "Interconnect instance",
            "parameters": {
                "AXI_ID_W": "AXI_ID_W",
                "AXI_LEN_W": "AXI_LEN_W",
                "AXI_ADDR_W": "AXI_ADDR_W",
                "AXI_DATA_W": "AXI_DATA_W",
            },
            "connect": {
                "clk_rst_s": "ps_clk_rst",
                "m0_clk_rst": "intercon_m_clk_rst",
                "m0_axi_m": "ps_axi",
                "s0_clk_rst": "ps_clk_rst",
                "s0_axi_s": "axi",
            },
            "num_slaves": 1,
        },
    ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
            // General connections
            assign cke = 1'b1;
            assign arst = ~ps_arstn;
            assign ps_arst = ~ps_arstn;
            """,
        },
    ]

    return attributes_dict
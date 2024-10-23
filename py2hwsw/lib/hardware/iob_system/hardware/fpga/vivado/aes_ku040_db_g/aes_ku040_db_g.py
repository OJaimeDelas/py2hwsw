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
                {"name": "c0_sys_clk_clk_p_i", "width": "1"},
                {"name": "c0_sys_clk_clk_n_i", "width": "1"},
                {"name": "areset_i", "width": "1"},
            ],
        },
        {
            "name": "rs232",
            "descr": "Serial port",
            "signals": [
                {"name": "txd_o", "width": "1"},
                {"name": "rxd_i", "width": "1"},
            ],
        },
    ]
    if params["use_extmem"]:
        attributes_dict["ports"] += [
            {
                "name": "ddr4_pins",
                "descr": "External DDR4 memory interface",
                "signals": [
                    {"name": "c0_ddr4_act_n_o", "width": "1"},
                    {"name": "c0_ddr4_adr_o", "width": "17"},
                    {"name": "c0_ddr4_ba_o", "width": "2"},
                    {"name": "c0_ddr4_bg_o", "width": "1"},
                    {"name": "c0_ddr4_cke_o", "width": "1"},
                    {"name": "c0_ddr4_odt_o", "width": "1"},
                    {"name": "c0_ddr4_cs_n_o", "width": "1"},
                    {"name": "c0_ddr4_ck_t_o", "width": "1"},
                    {"name": "c0_ddr4_ck_c_o", "width": "1"},
                    {"name": "c0_ddr4_reset_n_o", "width": "1"},
                    {"name": "c0_ddr4_dm_dbi_n_io", "width": "4"},
                    {"name": "c0_ddr4_dq_io", "width": "32"},
                    {"name": "c0_ddr4_dqs_c_io", "width": "4"},
                    {"name": "c0_ddr4_dqs_t_io", "width": "4"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["ports"] += [
            {
                "name": "mii",
                "descr": "MII ethernet interface",
                "signals": [
                    {"name": "enet_resetn_o", "width": "1"},
                    {"name": "enet_rx_clk_i", "width": "1"},
                    {"name": "enet_gtx_clk_o", "width": "1"},
                    {"name": "enet_rx_d0_i", "width": "1"},
                    {"name": "enet_rx_d1_i", "width": "1"},
                    {"name": "enet_rx_d2_i", "width": "1"},
                    {"name": "enet_rx_d3_i", "width": "1"},
                    {"name": "enet_rx_dv_i", "width": "1"},
                    # {"name": "enet_rx_err_o", "width": "1"},
                    {"name": "enet_tx_d0_o", "width": "1"},
                    {"name": "enet_tx_d1_o", "width": "1"},
                    {"name": "enet_tx_d2_o", "width": "1"},
                    {"name": "enet_tx_d3_o", "width": "1"},
                    {"name": "enet_tx_en_o", "width": "1"},
                    # {"name": "enet_tx_err_o", "width": "1"},
                ],
            },
        ]

    #
    # Wires
    #
    attributes_dict["wires"] = [
        {
            "name": "clk_en_rst",
            "descr": "Clock, clock enable and reset",
            "signals": {
                "type": "clk_en_rst",
            },
        },
        {
            "name": "rs232_int",
            "descr": "iob-system uart interface",
            "signals": [
                {"name": "rxd_i"},
                {"name": "txd_o"},
                {"name": "rs232_rts", "width": "1"},
                {"name": "high", "width": "1"},
            ],
        },
    ]
    if params["use_extmem"]:
        attributes_dict["wires"] += [
            {
                "name": "axi",
                "descr": "AXI interface to connect SoC to memory",
                "signals": {
                    "type": "axi",
                    "ID_W": "AXI_ID_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LEN_W": "AXI_LEN_W",
                },
            },
            {
                "name": "intercon_clk_rst",
                "descr": "AXI interconnect clock and reset inputs",
                "signals": [
                    {
                        "name": "ddr4_axi_clk" if params["use_extmem"] else "clk",
                        "width": 1,
                    },
                    {"name": "intercon_rst", "width": "1"},
                ],
            },
            {
                "name": "intercon_s0_clk_rst",
                "descr": "Interconnect slave 0 clock reset interface",
                "signals": [
                    {"name": "clk"},
                    {"name": "intercon_s0_arstn", "width": "1"},
                ],
            },
            {
                "name": "intercon_m0_clk_rst",
                "descr": "Interconnect master 0 clock and reset",
                "signals": [
                    {"name": "ddr4_axi_clk" if params["use_extmem"] else "clk"},
                    {"name": "intercon_m0_arstn", "width": "1"},
                ],
            },
            {
                "name": "memory_axi",
                "descr": "AXI bus to connect interconnect and memory",
                "signals": {
                    "type": "axi",
                    "prefix": "mem_",
                    "ID_W": "AXI_ID_W",
                    "LEN_W": "AXI_LEN_W",
                    "ADDR_W": "AXI_ADDR_W - 2",
                    "DATA_W": "AXI_DATA_W",
                    "LOCK_W": 1 if params["use_extmem"] else 2,
                },
            },
            {
                "name": "ddr4_ui_clk_out",
                "descr": "DDR4 user interface clock output",
                "signals": [
                    {"name": "clk"},
                ],
            },
            {
                "name": "ddr4_axi_clk_rst",
                "descr": "ddr4 axi clock and resets",
                "signals": [
                    {"name": "ddr4_axi_clk"},
                    {"name": "intercon_rst"},
                    {"name": "intercon_m0_arstn"},
                ],
            },
        ]
    if not params["use_extmem"]:
        attributes_dict["wires"] += [
            {
                "name": "clk_wizard_out",
                "descr": "Connect clock wizard outputs to iob-system clock and reset",
                "signals": [
                    {"name": "clk"},
                    {"name": "intercon_rst"},
                ],
            },
        ]
    if params["use_ethernet"]:
        attributes_dict["wires"] += [
            # eth clock
            {
                "name": "rxclk_buf_io",
                "descr": "IBUFG io",
                "signals": [
                    {"name": "enet_rx_clk_i"},
                    {"name": "eth_clk", "width": "1"},
                ],
            },
            {
                "name": "oddre1_io",
                "descr": "ODDRE1 io",
                "signals": [
                    {"name": "enet_gtx_clk_o"},
                    {"name": "eth_clk"},
                    {"name": "high"},
                    {"name": "low", "width": "1"},
                    {
                        "name": "enet_resetn_inv",
                        "width": "1",
                    },
                ],
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
            },
            "dest_dir": "hardware/common_src",
            "iob_system_params": params,
        },
    ]
    if params["use_extmem"]:
        attributes_dict["blocks"][-1]["connect"].update({"axi_m": "axi"})
        # DDR4 controller
        attributes_dict["blocks"] += [
            {
                "core_name": "xilinx_axi_interconnect",
                "instance_name": "axi_async_bridge",
                "instance_description": "Interconnect instance",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W - 2",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_rst_s": "intercon_clk_rst",
                    "m0_clk_rst": "intercon_m0_clk_rst",
                    "m0_axi_m": "memory_axi",
                    "s0_clk_rst": "intercon_s0_clk_rst",
                    "s0_axi_s": "axi",
                },
                "num_slaves": 1,
            },
            {
                "core_name": "xilinx_ddr4_ctrl",
                "instance_name": "ddr4_ctrl",
                "instance_description": "DDR4 controller instance",
                "parameters": {
                    "AXI_ID_W": "AXI_ID_W",
                    "AXI_LEN_W": "AXI_LEN_W",
                    "AXI_ADDR_W": "AXI_ADDR_W",
                    "AXI_DATA_W": "AXI_DATA_W",
                },
                "connect": {
                    "clk_rst_i": "clk_rst_i",
                    "ui_clk_o": "ddr4_ui_clk_out",
                    "axi_clk_rst": "ddr4_axi_clk_rst",
                    "axi_s": (
                        "memory_axi",
                        [
                            "{mem_axi_araddr, 2'b0}",
                            "{mem_axi_awaddr, 2'b0}",
                        ],
                    ),
                    "ddr4": "ddr4_pins",
                },
            },
        ]
    if not params["use_extmem"]:
        # Clock wizard
        attributes_dict["blocks"] += [
            {
                "core_name": "xilinx_clock_wizard",
                "instance_name": "clk_250_to_100_MHz",
                "instance_description": "PLL to generate system clock",
                "parameters": {
                    "OUTPUT_PER": 10,
                    "INPUT_PER": 4,
                },
                "connect": {
                    "clk_rst_i": "clk_rst_i",
                    "clk_rst_o": "clk_wizard_out",
                },
            },
        ]
    if params["use_ethernet"]:
        # Eth clock
        attributes_dict["blocks"] += [
            {
                "core_name": "xilinx_ibufg",
                "instance_name": "rxclk_buf",
                "connect": {
                    "io": "rxclk_buf_io",
                },
            },
            {
                "core_name": "xilinx_oddre1",
                "instance_name": "oddre1_inst",
                "connect": {
                    "io": "oddre1_io",
                },
            },
        ]

    #
    # Snippets
    #
    attributes_dict["snippets"] = [
        {
            "verilog_code": """
    // General connections
    assign high = 1'b1;
    assign cke = 1'b1;
    assign arst = ~intercon_s0_arstn;
""",
        },
    ]
    if params["use_ethernet"]:
        attributes_dict["snippets"] += [
            {
                "verilog_code": """
    // Ethernet connections
    assign low = 1'b0;
    assign enet_resetn_inv = ~enet_resetn;
""",
            },
        ]

    return attributes_dict

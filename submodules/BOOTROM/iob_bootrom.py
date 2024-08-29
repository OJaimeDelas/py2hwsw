def setup(py_params_dict):
    VERSION = "0.1"
    # TODO: When csrs is updated, inline the value below on the conf and use it
    # as a parameter for the ROM size.
    BOOTROM_ADDR_W = "12"

    attributes_dict = {
        "original_name": "iob_bootrom",
        "name": "iob_bootrom",
        "version": VERSION,
        "confs": [
            {
                "name": "DATA_W",
                "type": "F",
                "val": "32",
                "min": "?",
                "max": "32",
                "descr": "Data bus width",
            },
            {
                "name": "ADDR_W",
                "type": "F",
                "val": "`IOB_BOOTROM_CSRS_ADDR_W",
                "min": "?",
                "max": "32",
                "descr": "Address bus width",
            },
            # These 2 below are copies of the ones defined in iob-soc.py
            {
                "name": "PREBOOTROM_ADDR_W",
                "type": "F",
                "val": "7",
                "min": "?",
                "max": "24",
                "descr": "Preboot ROM address width",
            },
            {
                "name": "BOOTROM_ADDR_W",
                "type": "F",
                "val": BOOTROM_ADDR_W,
                "min": "?",
                "max": "24",
                "descr": "Bootloader ROM address width",
            },
        ],
        "ports": [
            {
                "name": "clk_en_rst",
                "interface": {
                    "type": "clk_en_rst",
                    "subtype": "slave",
                },
                "descr": "Clock and reset",
            },
            {
                "name": "cbus",
                "interface": {
                    "type": "iob",
                    "subtype": "slave",
                    "port_prefix": "cbus_",
                    "ADDR_W": "`IOB_BOOTROM_CSRS_ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "Front-end control interface",
            },
            {
                "name": "ibus",
                "interface": {
                    "type": "iob",
                    "subtype": "slave",
                    "port_prefix": "ibus_",
                    "DATA_W": "DATA_W",
                    "ADDR_W": "ADDR_W",
                },
                "descr": "Instruction bus",
            },
            {
                "name": "ext_rom_bus",
                "descr": "External ROM signals",
                "signals": [
                    {
                        "name": "ext_rom_en",
                        "direction": "output",
                        "width": "1",
                    },
                    {
                        "name": "ext_rom_addr",
                        "direction": "output",
                        "width": "BOOTROM_ADDR_W",
                    },
                    {
                        "name": "ext_rom_rdata",
                        "direction": "input",
                        "width": "DATA_W",
                    },
                ],
            },
        ],
        "wires": [
            {
                "name": "rom",
                "descr": "",
                "signals": [
                    {"name": "rom_rdata_rd", "width": "DATA_W"},
                    {"name": "rom_rvalid_rd", "width": 1},
                    {"name": "rom_ren_rd", "width": 1},
                    {"name": "rom_rready_rd", "width": 1},
                ],
            },
        ],
        "blocks": [
            {
                "core_name": "csrs",
                "instance_name": "csrs_inst",
                "version": VERSION,
                "csrs": [
                    {
                        "name": "rom",
                        "descr": "ROM access.",
                        "regs": [
                            {
                                "name": "rom",
                                "type": "R",
                                "n_bits": "DATA_W",
                                "rst_val": 0,
                                "addr": -1,
                                "log2n_items": BOOTROM_ADDR_W + " - 2",
                                "autoreg": False,
                                "descr": "Bootloader ROM (read).",
                            },
                        ],
                    }
                ],
                "connect": {
                    "clk_en_rst": "clk_en_rst",
                    "control_if": "cbus",
                    # Register interfaces
                    "rom": "rom",
                },
            },
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_inst",
                "instantiate": False,
            },
            {
                "core_name": "iob_rom_sp",
                "instance_name": "iob_rom_sp_inst",
                "instantiate": False,
            },
        ],
    }
    return attributes_dict

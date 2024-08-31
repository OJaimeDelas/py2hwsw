import sys
import os
import copy

# Add csrs scripts folder to python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

import reg_gen
from iob_csr import create_csr_group

interrupt_csrs = {
    "name": "interrupt_csrs",
    "descr": "Interrupt control and status registers",
    "regs": [
        {
            "name": "status",
            "type": "R",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Interrupts status: active (1), inactive (0).",
        },
        {
            "name": "mask",
            "type": "W",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Interrupts mask: enable (0), disable (1) for each interrupt.",
        },
        {
            "name": "clear",
            "type": "W",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Interrupts clear: clear (1), do not clear (0) for each interrupt.",
        },
    ],
}

fifo_csrs = {
    "name": "fifo_csrs",
    "descr": "FIFO control and status registers",
    "regs": [
        {
            "name": "data",
            "type": "RW",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Read/write data from/to FIFO.",
        },
        {
            "name": "thresh",
            "type": "W",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Interrupt upper level threshold: an interrupt is triggered when the number of words in the FIFO reaches this upper level threshold.",
        },
        {
            "name": "empty",
            "type": "R",
            "n_bits": 1,
            "rst_val": 1,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Empty (1) or non-empty (0).",
        },
        {
            "name": "full",
            "type": "R",
            "n_bits": 1,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Full (1), or non-full (0).",
        },
        {
            "name": "level",
            "type": "R",
            "n_bits": 32,
            "rst_val": 0,
            "log2n_items": 0,
            "autoreg": True,
            "descr": "Number of words in FIFO.",
        },
    ],
}


def setup(py_params_dict):
    params = {
        "name": py_params_dict["instantiator"]["name"] + "_csrs",
        "version": "1.0",
        "csr_if": "iob",
        "csrs": [],
        "autoaddr": True,
        # Overlap Read and Write register addresses
        "rw_overlap": False,
        "build_dir": "",
        # Auto-add interrupt csrs: status, mask, clear
        "interrupt_csrs": False,
        # List of FIFO names. Will auto-add each FIFO csrs: full, empty, level, etc
        "fifo_csrs": [],
    }

    # Update params with values from py_params_dict
    for param in py_params_dict:
        if param in params:
            params[param] = py_params_dict[param]

    assert params["csrs"], print("Error: Register list empty.")

    assert params["build_dir"], print("Error: Register build dir empty.")

    # Copy instantiator confs but remove ADDR_W
    confs = [
        {
            "name": "ADDR_W",
            "type": "P",
            "val": "ND",
            "min": "0",
            "max": "32",
            "descr": "Address bus width",
        },
    ]
    for conf in py_params_dict["instantiator"]["confs"]:
        if conf["name"] != "ADDR_W":
            confs.append(conf)

    attributes_dict = {
        "original_name": "csrs",
        "name": params["name"],
        "version": params["version"],
        "confs": confs,
        "ports": [
            {
                "name": "clk_en_rst",
                "interface": {
                    "type": "clk_en_rst",
                    "subtype": "slave",
                },
                "descr": "Clock, clock enable and reset",
            },
            {
                "name": "control_if",
                "interface": {
                    "type": params["csr_if"],
                    "subtype": "slave",
                    "ADDR_W": "ADDR_W",
                    "DATA_W": "DATA_W",
                },
                "descr": "CSR control interface. Interface type defined by `csr_if` parameter.",
            },
        ],
        "wires": [],
        "blocks": [
            {
                "core_name": "iob_reg",
                "instance_name": "iob_reg_inst",
                "instantiate": False,
            },
            {
                "core_name": "iob_reg_e",
                "instance_name": "iob_reg_e_inst",
                "instantiate": False,
            },
        ],
        "snippets": [],
    }

    # Convert csrs dictionaries to objects
    csrs_obj_list = []
    for group in params["csrs"]:
        csrs_obj_list.append(create_csr_group(**group))

    # Auto-add csrs
    if params["interrupt_csrs"]:
        csrs_obj_list.append(interrupt_csrs)
    for fifo_name in params["fifo_csrs"]:
        local_fifo_csrs = copy.deepcopy(fifo_csrs)
        local_fifo_csrs["name"] = fifo_name + "_" + fifo_csrs["name"]
        for reg in local_fifo_csrs["regs"]:
            reg["name"] = fifo_name + "_" + reg["name"]
        csrs_obj_list.append(local_fifo_csrs)

    attributes_with_csrs = attributes_dict | {
        "csrs": csrs_obj_list,
        "csr_if": params["csr_if"],
        "rw_overlap": params["rw_overlap"],
        "autoaddr": params["autoaddr"],
        "build_dir": params["build_dir"],
    }

    # Generate snippets
    csr_gen_obj, reg_table = reg_gen.generate_csr(attributes_with_csrs)

    # Generate docs
    csr_gen_obj.generate_regs_tex(
        attributes_with_csrs["csrs"],
        reg_table,
        attributes_with_csrs["build_dir"] + "/document/tsrc",
    )

    # Auto-add VERSION macro
    found_version_macro = False
    if attributes_with_csrs["confs"]:
        for macro in attributes_with_csrs["confs"]:
            if macro["name"] == "VERSION":
                found_version_macro = True
    if not found_version_macro:
        attributes_with_csrs["confs"].append(
            {
                "name": "VERSION",
                "type": "M",
                "val": "16'h"
                + reg_gen.version_str_to_digits(attributes_with_csrs["version"]),
                "min": "NA",
                "max": "NA",
                "descr": "Product version. This 16-bit macro uses nibbles to represent decimal numbers using their binary values. The two most significant nibbles represent the integral part of the version, and the two least significant nibbles represent the decimal part. For example V12.34 is represented by 0x1234.",
            }
        )

    # Add ports for registers
    attributes_dict["ports"] += csr_gen_obj.gen_ports(reg_table)

    # TODO: Append csr_if to config_build.mk ?
    # file2create.write(f"CSR_IF={python_module.csr_if}\n\n")

    # Set correct address width macro
    attributes_dict["confs"][0]["val"] = csr_gen_obj.core_addr_w

    return attributes_dict

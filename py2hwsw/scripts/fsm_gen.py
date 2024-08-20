#!/usr/bin/env python3


def generate_fsm(core):
    """Generate verilog code with the fsm of this module.
    returns: Generated verilog code
    """
    if core.fsm != None:
        return core.fsm.verilog_code + "\n"

    return ""


def generate_fsm_snippet(core):
    """Write verilog snippet ('.vs' file) with the fsm of this core.
    This snippet may be included manually in verilog modules if needed.
    """
    code = generate_fsm(core)
    out_dir = core.build_dir + "/hardware/src"
    with open(f"{out_dir}/{core.name}_fsm.vs", "w+") as f:
        f.write(code)

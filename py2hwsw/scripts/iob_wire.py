from dataclasses import dataclass, field
from typing import List

import if_gen
from iob_base import find_obj_in_list, convert_dict2obj_list, fail_with_msg
from iob_signal import iob_signal, iob_signal_reference, get_real_signal


@dataclass
class iob_wire:
    """Class to represent a wire in an iob module"""

    name: str = ""
    # interface to auto-generate with if_gen.py
    interface: if_gen.interface = None
    descr: str = "Default description"
    # Only set the wire if this Verilog macro is defined
    if_defined: str = ""
    # List of signals belonging to this wire
    # (each signal is similar to a Verilog wire)
    signals: List = field(default_factory=list)
    # Reference to a global signal connected to this one
    global_wire = None

    def __post_init__(self):
        if not self.name:
            fail_with_msg("Wire name is not set", ValueError)

        if self.interface:
            self.signals += if_gen.get_signals(
                self.interface.type,
                "",
                self.interface.mult,
                self.interface.widths,
                self.interface.wire_prefix,
            )

            # Remove signal direction information
            for signal in self.signals:
                # Skip signal references
                if isinstance(signal, iob_signal_reference):
                    continue
                if signal.direction:
                    signal.direction = ""


def create_wire(core, *args, signals=[], interface=None, **kwargs):
    """Creates a new wire object and adds it to the core's wire list
    param core: core object
    """
    # Ensure 'wires' list exists
    core.set_default_attribute("wires", [])
    # Check if there are any references to signals in other wires/ports
    replace_duplicate_signals_by_references(core.wires + core.ports, signals)
    # Convert user signal dictionaries into 'iob_signal' objects
    sig_obj_list = convert_dict2obj_list(signals, iob_signal)
    # Convert user interface dictionary into 'if_gen.interface' object
    interface_obj = if_gen.dict2interface(interface) if interface else None
    wire = iob_wire(*args, signals=sig_obj_list, interface=interface_obj, **kwargs)
    core.wires.append(wire)


def get_wire_signal(core, wire_name: str, signal_name: str):
    """Return a signal reference from a given wire.
    param core: core object
    param wire_name: name of wire in the core's local wire list
    param signal_name: name of signal in the wire's signal list
    """
    wire = find_obj_in_list(core.wires, wire_name) or find_obj_in_list(
        core.ports, wire_name
    )
    if not wire:
        fail_with_msg(f"Could not find wire/port '{wire_name}'!")

    signal = find_obj_in_list(wire.signals, signal_name, process_func=get_real_signal)
    if not signal:
        fail_with_msg(
            f"Could not find signal '{signal_name}' of wire/port '{wire_name}'!"
        )

    return iob_signal_reference(signal=signal)


def replace_duplicate_signals_by_references(wires, signals):
    """Ensure that given list of 'signals' does not contain duplicates of other signals
    in the given 'wires' list, by replacing the duplicates with references to the
    original.
    param wires: list of wires with (original) signals
    param signals: list of new signals to be processed. If this list has a signal with
    the same name as another signal in the wires list, then this signal is replaced by a
    reference to the original.
    """
    for idx, signal in enumerate(signals):
        original_signal = find_signal_in_wires(wires, signal["name"])
        if not original_signal:
            continue
        original_signal = get_real_signal(original_signal)
        # print(f"[DEBUG] Replacing signal '{signal['name']}' by reference to original.")
        # Verify that new signal has same parameters as the original_signal
        for key, value in signal.items():
            if original_signal.__dict__[key] != value:
                fail_with_msg(
                    f"Signal '{signal['name']}' has different '{key}' than the original signal!"
                )
        # Replace signal by a reference to the original
        signals[idx] = iob_signal_reference(signal=original_signal)


def find_signal_in_wires(wires, signal_name):
    """Search for a signal in given list of wires"""
    for wire in wires:
        signal = find_obj_in_list(
            wire.signals, signal_name, process_func=get_real_signal
        )
        if signal:
            return signal
    return None

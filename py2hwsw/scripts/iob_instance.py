from typing import Dict

from iob_base import iob_base


class iob_instance(iob_base):
    """Class to describe a module's (Verilog) instance"""

    def __init__(
        self,
        *args,
        instance_name: str = None,
        parameters: Dict = {},
        **kwargs,
    ):
        """Build a (Verilog) instance
        param parameters: Verilog parameter values for this instance
                          Key: Verilog parameter name, Value: Verilog parameter value
        """
        self.set_default_attribute(
            "instance_name",
            instance_name or self.__class__.__name__ + "_inst",
            str,
            descr="Name of the instance",
        )
        self.set_default_attribute(
            "description",
            "Default description",
            str,
            descr="Description of the instance",
        )
        # Verilog parameter values
        self.set_default_attribute(
            "parameters", parameters, Dict, descr="Verilog parameter values"
        )
        # Only use this instance in Verilog if this Verilog macro is defined
        self.set_default_attribute(
            "if_defined",
            None,
            str,
            descr="Only use this instance in Verilog if this Verilog macro is defined",
        )
        # Select if should intantiate inside another Verilog module.
        # May be False if this is a software only module.
        self.set_default_attribute(
            "instantiate",
            True,
            bool,
            descr="Select if should intantiate the module inside another Verilog module.",
        )

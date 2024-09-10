def setup(py_params_dict):
    attributes_dict = {
        "original_name": "iob_or",
        "name": "iob_or",
        "version": "0.1",
        "confs": [
            {
                "name": "W",
                "type": "P",
                "val": "21",
                "min": "1",
                "max": "32",
                "descr": "IO width",
            },
        ],
        "ports": [
            """
            a -s a W input
            Input port

            b -s b W input
            Input port

            y -s y W output
            Output port
            """,
        ],
        "snippets": [{"verilog_code": "   assign y_o = a_i | b_i;"}],
    }

    return attributes_dict

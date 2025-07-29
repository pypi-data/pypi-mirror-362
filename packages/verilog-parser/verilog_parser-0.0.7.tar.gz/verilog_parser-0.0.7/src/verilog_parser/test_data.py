# SPDX-FileCopyrightText: 2024-2025 Thomas Kramer
# SPDX-FileCopyrightText: 2018-2021 T. {Benz, Kramer}
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os.path


def verilog_netlist() -> str:
    """
    Get content of an example Verilog netlist.
    :return:
    """
    verilog_file = os.path.join(os.path.dirname(__file__), '../../test_data/simple_nl_ys.v')
    with open(verilog_file) as f:
        data = f.read()
    return data

#!/usr/bin/env python3
# Copyright 2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this report except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import pprint
from collections import namedtuple

from reader import click_odb, click

import odb
import utl


def filter_net(net: odb.dbNet) -> bool:
    # wire is the physical implementation of a net.
    # if a net has no wire. there is no problem for it being unannotated
    return net.getWire() is not None


@click.option("--corner")
@click.option("--checks-report", "checks_report")
@click.command()
@click_odb
def main(reader, corner, checks_report):
    Net = namedtuple("Net", "name bterms")
    BTerm = namedtuple("BTerm", "name type")

    db = reader.db
    block = db.getChip().getBlock()
    nets = block.getNets()

    report_content = []
    with open(checks_report, "r") as f:
        report_content = f.readlines()

    annotation_report_start = "report_parasitic_annotation -report_unannotated\n"
    annotation_report_end = (
        "===========================================================================\n"
    )
    start_index = report_content.index(annotation_report_start)
    end_index = report_content.index(annotation_report_end, start_index)

    print("Unannotated report:")
    pprint.pprint(report_content[start_index:end_index])

    # Sample report:
    # Found 324 unannotated drivers.
    #  analog_io[0]
    #  analog_io[10]
    #  analog_io[11]
    # Found 68 partially unannotated drivers.
    #  wbs_adr_i[0]
    #   mprj/wbs_adr_i[31]
    #  wbs_adr_i[10]
    #   mprj/wbs_adr_i[21]
    #  wbs_adr_i[11]
    # ....

    reported_nets = [
        line.rstrip().lstrip()
        for line in report_content[start_index:end_index]
        if re.match(r" \S+", line)
    ]
    nets_with_wire = [net for net in nets if filter_net(net)]
    print("Reported nets:")
    pprint.pprint(reported_nets)
    unannotated_with_wire = [
        Net(
            name=net.getName(),
            bterms=[
                BTerm(bterm.getName(), bterm.getIoType()) for bterm in net.getBTerms()
            ],
        )
        for net in nets_with_wire
        if (net.getName() in reported_nets)
    ]
    print("Filtered nets:")
    pprint.pprint(unannotated_with_wire)
    utl.metric_integer(
        f"timing__unannotated_net__count__corner:{corner}", len(reported_nets)
    )
    utl.metric_integer(
        f"timing__unannotated_net_filtered__count__corner:{corner}",
        len(unannotated_with_wire),
    )
    utl.metric_float(
        f"timing__unannotated_net__percent__corner:{corner}",
        round(len(reported_nets) / len(nets) * 100, 2),
    )
    utl.metric_float(
        f"timing__unannotated_net_filtered__percent__corner:{corner}",
        round(len(unannotated_with_wire) / len(nets_with_wire) * 100, 2),
    )
    pprint.pprint(f"Nets: {len(nets)}")
    pprint.pprint(f"Nets with wire: {len(nets_with_wire)}")
    pprint.pprint(f"Unannotated with wire: {len(unannotated_with_wire)}")
    print("done")


if __name__ == "__main__":
    main()

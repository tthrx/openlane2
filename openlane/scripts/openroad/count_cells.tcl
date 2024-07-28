# Copyright 2024 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
foreach lib $::env(_LIBS) {
    read_liberty $lib
}
read_verilog $::env(CURRENT_NETLIST)
link_design $::env(DESIGN_NAME)

set buffer_count 0
set clock_gate_count 0
set hier_count 0
set inverter_count 0
set macro_count 0
set memory_cell_count 0
set cells [get_cells *]
foreach cell [get_cells *] {
    if { [get_property $cell is_buffer] } {
        set buffer_count [expr $buffer_count + 1]
    }
    if { [get_property $cell is_clock_gate] } {
        set clock_gate_count [expr $clock_gate_count + 1]
    }
    if { [get_property $cell is_hierarchical] } {
        set hier_count [expr $hier_count + 1]
    }
    if { [get_property $cell is_inverter] } {
        set inverter_count [expr $inverter_count + 1]
    }
    if { [get_property $cell is_macro] } {
        set macro_count [expr $macro_count + 1]
    }
    if { [get_property $cell is_memory_cell] } {
        set memory_cell_count [expr $memory_cell_count + 1]
    }
}

puts "buffer $buffer_count"
puts "clock_gate $clock_gate_count"
puts "hierarchical $hier_count"
puts "inverter $inverter_count"
puts "macro $macro_count"
puts "memory_cell $memory_cell_count"


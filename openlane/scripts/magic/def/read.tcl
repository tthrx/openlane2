# Copyright 2022 Efabless Corporation
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

# LEF
puts "> lef read $::env(TECH_LEF)"
lef read $::env(TECH_LEF)
if { [info exist ::env(MACRO_LEFS)] } {
    foreach lef_file $::env(MACRO_LEFS) {
        puts "> lef read $lef_file"
        lef read $lef_file
    }
}
if { [info exist ::env(EXTRA_LEFS)] } {
    foreach lef_file $::env(EXTRA_LEFS) {
        puts "> lef read $lef_file"
        lef read $lef_file
    }
}
# if { [info exist ::mag_read_cell_lefs] && $::mag_read_cell_lefs } {
#     foreach lef_file $::env(CELL_LEFS) {
#         puts "> lef read $lef_file"
#         lef read $lef_file
#     }
# }

# DEF
set def_read_args [list]
lappend def_read_args $::env(CURRENT_DEF)
if { $::env(MAGIC_DEF_NO_BLOCKAGES) } {
    lappend def_read_args -noblockage
}
if { $::env(MAGIC_DEF_LABELS) } {
    lappend def_read_args -labels
}

puts "> def read $def_read_args"
def read {*}$def_read_args
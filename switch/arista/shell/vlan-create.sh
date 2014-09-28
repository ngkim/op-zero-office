#!/bin/bash

source "$MNG_ROOT/include/print.sh"

SWITCH_HOME=$MNG_ROOT/switch/arista/
source "$SWITCH_HOME/switch.cfg"

MODE="SWITCH-VLAN-CREATE"

VLAN_ID=37

$SWITCH_HOME/vlan-create.expect $ARISTA_SW $ARISTA_ADM $ARISTA_ADM_PASS $VLAN_ID

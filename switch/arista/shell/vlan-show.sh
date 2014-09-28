#!/bin/bash

source "$MNG_ROOT/include/print.sh"

SWITCH_HOME=$MNG_ROOT/switch/arista/
EXPECT_HOME=$MNG_ROOT/switch/arista/expect

source "$SWITCH_HOME/switch.cfg"

MODE="SWITCH-VLAN-CREATE"

VLAN_ID=25

$EXPECT_HOME/vlan-show.expect $ARISTA_SW $ARISTA_ADM $ARISTA_ADM_PASS $VLAN_ID

#!/bin/bash

VM_LIST=`virsh list | awk '$1 ~ /^[0-9]+$/{print $2}'`

get_mac() {
	vm=$1
	ITF=$2

	MAC=`virsh domiflist $vm | awk '$1 ~ /'$ITF'/ {print $5}'`
	
	echo $MAC
}

get_br() {
	vm=$1
	ITF=$2

	BR_NAME=`virsh domiflist $vm | awk '$1 ~ /'$ITF'/ {print $3}'`

	echo $BR_NAME
}

get_br_dev_list() {
	BR_NAME=$1

	BR_LIST=`ls /sys/class/net/$BR_NAME/brif`

	echo $BR_LIST
}

get_veth_in_qbr() {
	dev_tap=$1
	# should set qbr_dev_list before calling get_veth_in_qbr
	for dev in $qbr_dev_list; do
		if [ "$dev" != "$dev_tap" ]; then
			dev_qvb=$dev
		fi
	done
	
	echo $dev_qvb
}

get_dev_id() {
	dev_tap=$1

	echo $dev_tap | sed 's/tap//'
}

get_dev_qvo_name() {
	dev_id=$1

	echo "qvo${dev_id}"
}

get_ovs_list_ports() {
	ovs=$1

	ovs-vsctl list-ports $ovs
}

blue=$(tput setaf 4)
red=$(tput setaf 1)
normal=$(tput sgr0)

# store dev_qvo to check if it's in br-int
list_dev_qvo=""
for vm in $VM_LIST; do
	printf "${red}$vm\n"
	IF_LIST=`virsh domiflist $vm | awk '$1 ~ /^tap/ {print $1}'`
	for iftap in $IF_LIST; do
		dev_id=$(get_dev_id $iftap)
		MAC=$(get_mac $vm $iftap)
		qbr=$(get_br $vm $iftap)
		qbr_dev_list=$(get_br_dev_list $qbr) 
		dev_qvb=$(get_veth_in_qbr $iftap)
		dev_qvo=$(get_dev_qvo_name $dev_id)
		list_dev_qvo="$list_dev_qvo $dev_qvo"

		printf "\t${blue}DEV_TAP= ${normal}$iftap ${blue}BR_Q= ${normal}$qbr ${blue}DEV_QVB= ${normal}$dev_qvb ${blue}DEV_QVO= ${normal}$dev_qvo\n"
	done
done

if [[ "$HOST" =~ ^user.* ]]; then
    echo "yes"
fi

dev_list_contains_port() {
	port=$1	

	for dev in $list_dev_qvo; do
		if [ $dev == $port ]; then
			echo "$dev"
			break
		fi
	done
}

print_dev_qvo_in_br_int() {
	port=$1

	dev_qvo=$(dev_list_contains_port $port)
	dev_qvo=$(echo $dev_qvo | tr -d '\n' | tr -d ' ')

	char_cnt=$(echo $dev_qvo | wc -m)
	if [ $char_cnt -gt 1 ]; then
		printf "\t$dev_qvo\n"
	fi
}

print_dev_int_in_br_int() {
	port=$1

	if [[ $port =~ ^[int] ]]; then
		printf "\t$port\n"
	fi
}

print_dev_phy_in_br() {
	port=$1

	if [[ $port =~ ^[phy] ]]; then
		printf "\t$port\n"
	fi
}

list_dev_phy_in_br() {
	port=$1

	if [[ $port =~ ^[phy] ]]; then
		printf "\t$port\n"
	fi
}

ovs="br-int"
printf "${red}$ovs${normal}\n"
port_list=$(get_ovs_list_ports $ovs)
for port in $port_list; do
	print_dev_qvo_in_br_int $port
	print_dev_int_in_br_int $port
done

OVS_LIST=`ovs-vsctl list-br`
for ovs in $OVS_LIST; do
	if [ "$ovs" == "br-int" ]; then
		continue;
	fi
	printf "${red}$ovs${normal}\n"
	port_list=$(get_ovs_list_ports $ovs)
	for port in $port_list; do
		printf "\t$port\n"
	done
done

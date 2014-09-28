#!/bin/bash

ORN=221.145.180.78
UTM=221.145.180.96

echo "run UTM"
ssh $UTM ./test.sh &
echo "run ping"
ssh $ORN ping 192.168.1.2 &> /dev/null &
PING_PID=$!
echo "sleep"
sleep 5
echo "kill ping"
kill $PING_PID
echo "scp"
scp $UTM:br0.dump .

#!/bin/bash
echo "WARNING: This scripts overrides the content of /etc/dnsmasq.conf"
echo "If you have installed dnsmasq before, make sure you backup the 
content of you config file. If you don't know what I'm talking about, 
you'll probably can ignore this."
echo "=> Press enter to proceed or <Ctrl>+<C> to abort..."
read
apt-get update
apt-get install dnsmasq
echo 'listen-address=192.168.100.1' > /etc/dnsmasq.conf
echo 'dhcp-range=192.168.100.20,192.168.100.254,6h' >> /etc/dnsmasq.conf
systemctl restart dnsmasq


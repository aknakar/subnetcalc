#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Subnetcalc.py
#
# An app that calculates network address, broadcast address, wildcard mask, and
# number of hosts for a given subnet.
#
# AUTHOR: aknakar
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import random
import sys

def ip_addr_valid(ip):

	#Check to see whether an IP address is valid, i.e. not a reserved or broadcast IP address.

	octet_list = ip.split('.')
	if (len(octet_list) == 4) and (1 <= int(octet_list[0]) <= 223) and (int(octet_list[0]) != 127) and (int(octet_list[0]) != 169 or int(octet_list[1]) != 254) and (0 <= int(octet_list[1]) <= 255 and 0 <= int(octet_list[2]) <= 255 and 0 <= int(octet_list[3]) <= 255):
		return True
	else:
		return False


def sub_mask_valid(mask):

	#Check to see whether a subnet mask is valid.

	octet_list = mask.split('.')
	mask = [0,128,192,224,240,248,252,254,255]
	if (len(octet_list) == 4) and (int(octet_list[0]) in mask) and (int(octet_list[1]) in mask) and (int(octet_list[2]) in mask) and (int(octet_list[3]) in mask) and (int(octet_list[0]) == 255) and int(octet_list[0]) >= int(octet_list[1]) >= int(octet_list[2]) >= int(octet_list[3]):
		return True
	else:
		return False



def ip_to_binary(ip):

	#Convert a subnet mask to a 32-bit binary number.

	octet_list = ip.split('.')
	bin_list = []
	for num in octet_list:
		bin = f'{int(num):08b}'
		bin_list.append(bin)
	return ''.join(bin_list)


def num_hosts(bin_num):

	#Calculate the number of hosts allowed on the subnet.

	return((2**bin_num.count('0'))-2)


def wild_card(mask):
	
	#Calculate a wild-card address based on a subnet mask.
	
	mask_oct = mask.split('.')
	wild_list = []
	for oct in mask_oct:
		wild_list.append(str(255-int(oct)))
	return '.'.join(wild_list)


def net_brd_addr(ip, mask):
	
	#Calculate network address and broadcast address based on IP address and subnet mask.

		#Convert mask to binary
	mask_bin = ip_to_binary(mask)
	
	
		#Convert IP address to binary
	ip_bin = ip_to_binary(ip)

	num_zeros = mask_bin.count('0')
	num_ones = 32 - num_zeros

	net_addr_bin = ip_bin[:num_ones] + '0' * num_zeros
	brd_addr_bin = ip_bin[:num_ones] + '1' * num_zeros
	
	net_bin_octs = [net_addr_bin[i:i+8] for i in range(0,32,8)]
	brd_bin_octs = [brd_addr_bin[i:i+8] for i in range(0,32,8)]
	
	net_addr_octs = []
	for oct in net_bin_octs:
		oct0 = str(int(oct,2))
		net_addr_octs.append(oct0)
	net_addr = '.'.join(net_addr_octs)

	brd_adr_octs = []
	for oct in brd_bin_octs:
		oct0 = str(int(oct,2))
		brd_adr_octs.append(oct0)
	brd_addr = '.'.join(brd_adr_octs)

	return [net_addr, brd_addr]	


def random_ip(ip,mask):
	net_addr = net_brd_addr(ip,mask)[0]
	brd_addr = net_brd_addr(ip,mask)[1]
	
	
	rand_addr = []
	for indexn, net_oct in enumerate(net_addr):
		for indexb, brd_oct in enumerate(brd_addr):
			if indexn==indexb:
				if brd_oct == net_oct:
					rand_addr.append(brd_oct)
				else:
					rand_addr.append(str(random.randint(int(net_oct), int(brd_oct))))
	return ''.join(rand_addr)
	

ip = input("Give me an IP address: ")
if ip_addr_valid(ip) == True:
	print("That address is valid!")
else:
	print("That address is either a broadcast or reserved IP address. Try again.")
	sys.exit()
mask = input("Now, give me a subnet mask: ")
if sub_mask_valid(mask) == True:
	print("That subnet mask is valid!")
else:
	print("That is not a subnet mask. Try again.")
	sys.exit()
print("\n%\nThe network address for this subnet is " + net_brd_addr(ip,mask)[0])
print("The broadcast address for this subnet is " + net_brd_addr(ip,mask)[1])
print("The wildcard mask for this " + wild_card(mask))
print("There is space for " + str(num_hosts(ip_to_binary(mask))) + " hosts on this subnet")
print("There are " + str(int(ip_to_binary(mask).count('1'))) + " mask bits in this subnet mask.")
yn = input("Would you like for me to generate a random IP address within this subnet for you? (y/n): ")
if yn == "y":
	print("Your random IP is " + str(random_ip(ip,mask)))
	print([x for x in 'GOODBYE'])
else:
	print("OK.")
	print([x for x in 'GOODBYE'])

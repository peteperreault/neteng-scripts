#! /usr/bin/env python

# Audits network device (i.e. routers, switches & firewalls) running configurations, writes to file the removal of non-standard and implementation of standardized configurations.  Configurations are in text files generated by another script such as RANCID.

import glob, re, os

# Variables
 # path to current configuration files
path = '/Group/configs'
 # path to configuration updates
path2 = '/configfiles'
ntp1 = '10.1.1.1'
ntp2 = '10.2.2.2'
snmp_com1 = 'foo1'
snmp_com2 = 'foo2'

# Regex
ntp_re = re.compile('ntp server (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
snmp_com_re = re.compile('snmp-server community (\S*)')
clk_re = re.compile('^clock (summer-time|timezone)')

def clk_func():
	# Checks clock configurations
	global clk_zone_check, clk_dst_check
	if clk_re.match(line):
		if 'timezone' in clk_re.match(line).group(1):
			clk_zone_check = True
		if clk_re.match(line).group(1) == 'summer-time':
			clk_dst_check = True

def snmp_com_func():
	# Checks snmp community strings
	global snmp_com1_check, snmp_com2_check
	if snmp_com_re.match(line):
		if snmp_com_re.match(line).group(1) == snmp_com1:
			snmp_com1_check = True
                elif snmp_com_re.match(line).group(1) == snmp_com2:
                        snmp_com2_check = True
		else:
			cnf.write(' no %s\n' % snmp_com_re.match(line).group(0))

def ntp_func():
	# Checks ntp server configuration
	global ntp1_check, ntp2_check
	if ntp_re.match(line):
		if ntp_re.match(line).group(1) == ntp1:
			ntp1_check = True
		elif ntp_re.match(line).group(1) == ntp2:
			ntp2_check = True
		else:
			cnf.write(' no %s\n' % ntp_re.match(line).group(0))

def cnf_func():
	# Writes new configurations to file
	global ntp1_check, ntp2_check, snmp_com1_check, snmp_com2_check, clk_zone_check, clk_dst_check
	if not clk_zone_check:
		cnf.write('clock timezone EST -5\n')
	if not clk_dst_check:
		cnf.write('clock summer-time EDT recurring\n')
	if not snmp_com1_check:
		cnf.write('snmp-server community %s ro\n' % snmp_com1)
	if not ntp1_check:
		cnf.write('ntp server %s\n' % ntp1)
	if not ntp2_check:
		cnf.write('ntp server %s\n' % ntp2)

for filename in glob.glob('%s/*' % path):
	host = os.path.basename(filename)
	ntp1_check = ntp2_check = snmp_com1_check = snmp_com2_check = False
	clk_zone_check = clk_dst_check = False
	if os.path.isfile(filename):	
		f = open(filename, "r")
		cnf = open('%s/%s' % (path2, host), "w")
       		cnf.write('!%s - configuration file\n' % host)
		for line in f:
			clk_func()
			snmp_com_func()
			ntp_func()
		cnf_func()
	f.close()

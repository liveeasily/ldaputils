#!/usr/bin/python

ENTRY_MAP = {
	"1":"dn",
	"2":"cn",
	"3":"displayname",
	"4":"mail",
	"5":"objectclass",
	"6":"sn",
	"7":"uid",
}

def parse_email(email):
	entry = {
		"dn":None,
		"cn":None,
		"displayname":None,
		"mail":email,
		"objectclass":"inetOrgPerson",
		"sn":None,
		"uid":None,
		"userpassword":"{SSHA}7UaECTjJ1qpaqlD21aTMvoDx/PiZPE7/"
	}

	try:
		account, domain = email.split("@")
	except ValueError:
		print "Your email is not vaild."
		return None

	# dn
	entry["dn"] = "cn=%s, ou=members, dc=wrs, dc=com" % account

	# cn
	entry["cn"] = account

	try:
		first_name, last_name = account.split(".")
	except ValueError:
		return entry

	first_name = first_name.capitalize()
	last_name = last_name.capitalize()

	# display name
	entry["displayname"] = "%s %s" % (first_name, last_name)

	# sn
	entry["sn"] = last_name

	# uid
	entry["uid"] = account

	return entry


def print_select(entry):
	print "0. I like this! :)"
	print "1. dn: ", entry["dn"]
	print "2. cn: ", entry["cn"]
	print "3. displayname: ", entry["displayname"]
	print "4. mail: ", entry["mail"]
	print "5. objectclass: ", entry["objectclass"]
	print "6. sn: ", entry["sn"]
	print "7. uid: ", entry["uid"]

def modify_entry(entry, select):
	key = ENTRY_MAP[select]
	new_value = raw_input("Input new value for %s: " % key)
	entry[key] = new_value
	return entry	

def make_ldif(entry):
	f = file("addmember.ldif", "w+")
	keys = entry.keys()
	for key in keys:
		f.write("%s: %s\n" %(key, entry[key]))
	f.close()
	return f	

if __name__ == '__main__':
	email = raw_input("Input email(ex:sunjae.kim@windriver.com): ")
	entry = parse_email(email)

	while True:
		print_select(entry)
		select = raw_input("Enter number: ")
		if select == '0':
			break
		else:
			entry = modify_entry(entry, select)
	
	ldif = make_ldif(entry)

	cmd = "ldapadd -x -D \"cn=admin,dc=wrs,dc=com\" -W -f %s" % ldif.name
	print cmd

	import os
	if os.system(cmd) == 0:
		print "Succeed to add a new member! Initial password is \"1234\"."

	

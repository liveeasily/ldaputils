#!/usr/bin/python

def parse_email(email):
	entry = {
		"cn":None,
		"displayName":None,
		"Email":email,
		"objectClass":"inetOrgPerson",
		"Password":"1234"
	}

	try:
		account, domain = email.split("@")
	except ValueError:
		print "Your email is not vaild."
		return None

	# cn
	entry["cn"] = account

	log(account)
	try:
		first_name, last_name = account.split(".")
	except ValueError:
		return entry

	first_name = first_name.capitalize()
	last_name = last_name.capitalize()

	# display name
	entry["displayName"] = "%s %s" % (first_name, last_name)

	return entry

if __name__ == '__main__':
	email = raw_input("E-mail(ex:sunjae.kim@windriver.com): ")
	entry = parse_email(email)
	print entry

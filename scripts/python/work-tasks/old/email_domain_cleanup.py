#!/usr/bin/env python

# puts the relevant CVS files in a folder "emailcleanup" on your home directory. This can be changed by changing
# emailcleanup_path
# works by changing to projects/advantage/dev and going to Ipython shell (where User model is loaded) and
# just cut and paste (%paste)

import os

homepath = os.getenv("HOME")

emailcleanup_path = homepath + "/emailcleanup"


#get user objects, easier to work with
all_user_objs = User.objects.all()




#get all inactive users
inactive_users = []
for user in all_user_objs:
    try:
        a = user.active
        if not a:
            inactive_users.append(user)
    except:
        pass


#get all active users that haven't logged in in a year
active_but_old_users = []
import datetime
now = datetime.datetime.now()
yearago = now - datetime.timedelta(days=365)
for user in all_user_objs:
    if user.type == "A":
                continue
    try:
        a = user.active
        if a:
            if user.last_auth_date < yearago:
                active_but_old_users.append(user)
    except:
        pass


#make strings for inactive
inactivestrings = ["Username, \"Full name\", \"Clinics\", \"Last logon\"\n"]
for u in inactive_users:
    string = "\"" + u.username + "\", "
    string += "\"" + u.first_name + " " + u.last_name + "\", "
    staffobj = u.clinics.all()
    clinics = []
    for obj in staffobj:
        clinics.append(obj.clinic.name)
    clinic_string = ", ".join(clinics)
    string += "\"" + clinic_string + "\", "
    if u.last_auth_date:
        string += "\"" + u.last_auth_date.strftime('%m/%d/%Y') + "\"\n"
    else:
        string += "\"never logged in\"\n"
    s = string.encode('ascii','ignore')
    inactivestrings.append(s)
inactivestring = "".join(inactivestrings)


#make strings for active
notrecentstrings = ["Username, \"Full name\", \"Clinics they still work at\", \"Last logon\"\n"]
for u in active_but_old_users:
    string = "\""
    string += u.username + "\", "
    string += "\"" + u.first_name + " " + u.last_name + "\", "
    staffobj = u.clinics.all()
    clinics = []
    for obj in staffobj:
        if not obj.active:
            continue
        clinics.append(obj.clinic.name)
    clinic_string = ", ".join(clinics)
    string += "\"" + clinic_string + "\", "
    if u.last_auth_date:
        string += "\"" + u.last_auth_date.strftime('%m/%d/%Y') + "\"\n"
    else:
        string += "\"never logged in\"\n"
    s = string.encode('ascii','ignore')
    notrecentstrings.append(s)
notrecentstring = "".join(notrecentstrings)



inactive_path   = emailcleanup_path + '/inactiveusers.txt'
not_recent_path = emailcleanup_path + '/not_recent_users.txt'

def write_to_file(filepath, content):
    f = file(filepath, 'w')
    f.write(content)
    f.close()

if not os.path.isdir(emailcleanup_path):
    os.mkdir(emailcleanup_path)


write_to_file(inactive_path, inactivestring)

write_to_file(not_recent_path, notrecentstring)



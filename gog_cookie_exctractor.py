import sqlite3 as db
import sys
import datetime
import os

connection = db.connect(sys.argv[1])
cursor = connection.cursor()

cursor.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies WHERE host LIKE '%gog.com%'")

file = open('gog-cookies.dat', 'w')
file.write("#LWP-Cookies-2.0\n")
for row in cursor.fetchall():
    if row[4] in ["gog-al", "gog_lc", "gog_set", "gog_us", "galaxy-login-al", "galaxy-login-s", "galaxy-login-tsa"]:
        domain_dot = 'domain_dot;' if row[0][0] == '.' else ''
        secure = 'secure;' if bool(row[2]) else ''
        file.write(f"Set-Cookie3: {row[4]}=\"{row[5]}\";path=\"{row[1]}\";domain=\"{row[0]}\";path_spec;{domain_dot}{secure}expires=\"{datetime.datetime.fromtimestamp(row[3]).strftime('%Y-%m-%d %H:%M:%SZ')}\";HttpOnly=None;version=0\n")

file.close()
connection.close()

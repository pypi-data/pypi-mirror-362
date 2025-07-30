import socket

def add_host_alias(app,  host, domain, hosts_file='/etc/hosts'):
    ip = socket.gethostbyname(host)
    with open(hosts_file, "a") as hosts:
        hosts.write("{0} {1}\n".format(ip, domain))
        hosts.write("{0} {1}.{2}\n".format(ip, app, domain))

import requests

from syncloudlib.integration.installer import wait_for_platform_web, wait_for_installer
from syncloudlib.http import wait_for_rest
from syncloudlib.integration.ssh import run_scp, run_ssh
from requests.adapters import HTTPAdapter 
import socket

class Device:

    def __init__(self, domain, device_user, device_password, redirect_user, redirect_password,
                 ssh_env_vars):
        self.domain = domain
        self.device_user = device_user
        self.device_password = device_password
        self.redirect_user = redirect_user
        self.redirect_password = redirect_password
        self.ssh_env_vars = ssh_env_vars
        self.ssh_password = 'syncloud'
        self.session = None

    def deactivate(self):
        run_ssh(self.domain, 'rm /var/snap/platform/common/platform.db', password=self.ssh_password)

    def activate(self, channel="stable"):
        ip = socket.gethostbyname(self.domain)
        run_ssh(self.domain, 'echo "{0} auth.{1}" >> /etc/hosts'.format(ip, self.domain), password=self.ssh_password, retries=10)
        run_ssh(self.domain, '/snap/platform/current/bin/upgrade-snapd.sh {0}'.format(channel), password=self.ssh_password, retries=10)
        run_ssh(self.domain, 'snap refresh platform --channel={0}'.format(channel), password=self.ssh_password, retries=10)

        wait_for_rest(requests.session(), "https://{0}/rest/id".format(self.domain), 200, 10)

        response = requests.post('https://{0}/rest/activate/managed'.format(self.domain),
                                 json={'redirect_email': self.redirect_user,
                                       'redirect_password': self.redirect_password,
                                       'domain': self.domain,
                                       'device_username': self.device_user,
                                       'device_password': self.device_password}, verify=False)
        if response.status_code == 200:
            self.activated()
            self.login()
        return response

    def activate_custom(self, channel="stable"):
        ip = socket.gethostbyname(self.domain)
        run_ssh(self.domain, 'echo "{0} auth.{1}" >> /etc/hosts'.format(ip, self.domain), password=self.ssh_password, retries=10)
        run_ssh(self.domain, '/snap/platform/current/bin/upgrade-snapd.sh {0}'.format(channel), password=self.ssh_password, retries=10)
        run_ssh(self.domain, 'snap refresh platform --channel={0}'.format(channel), password=self.ssh_password, retries=10)

        wait_for_rest(requests.session(), "https://{0}/rest/id".format(self.domain), 200, 10)
        response = requests.post('https://{0}/rest/activate/custom'.format(self.domain),
                                 json={'domain': self.domain,
                                       'device_username': self.device_user,
                                       'device_password': self.device_password}, verify=False)
        if response.status_code == 200:
            self.activated()
            self.login()
        return response

    def activated(self):
        self.ssh_password = self.device_password

    def login(self, retries=5):
        session = requests.session()
        session.mount('https://{0}'.format(self.domain), HTTPAdapter(max_retries=retries)) 
        retry = 0
        while True:
            try:
                session.post('https://{0}/rest/login'.format(self.domain), verify=False, allow_redirects=False,
                             json={'username': self.device_user, 'password': self.device_password})
                response = session.get('https://{0}/rest/user'.format(self.domain), verify=False,
                                       allow_redirects=False)
                if response.status_code == 200:
                    self.session = session
                    return session
            except Exception as e:
                print(str(e))
                print('retry {0} of {1}'.format(retry, retries))
            retry += 1
            if retry > retries:
                raise Exception('cannot login')

    def app_remove(self, app, attempts=200):
        response = self.session.post('https://{0}/rest/app/remove'.format(self.domain), json={'app_id': app},
                                     verify=False, allow_redirects=False)

        wait_for_installer(self.session, self.domain, attempts=attempts)
        return response

    def app_install(self, app, attempts=200):
        response = self.session.post('https://{0}/rest/app/install'.format(self.domain), json={'app_id': app},
                                     verify=False, allow_redirects=False)

        wait_for_installer(self.session, self.domain, attempts=attempts)
        return response

    def run_ssh(self, cmd, retries=0, throw=True, env_vars='', debug=True, sleep=1):
        ssh_env_vars = self.ssh_env_vars + ' ' + env_vars
        return run_ssh(self.domain, cmd, password=self.ssh_password, env_vars=ssh_env_vars, retries=retries,
                       throw=throw, debug=debug, sleep=sleep)

    def scp_from_device(self, dir_from, dir_to, throw=False):
        return run_scp('-r root@{0}:{1} {2}'.format(self.domain, dir_from, dir_to), password=self.ssh_password,
                       throw=throw)

    def scp_to_device(self, dir_from, dir_to, throw=False):
        return run_scp('-r {0} root@{1}:{2}'.format(dir_from, self.domain, dir_to), password=self.ssh_password,
                       throw=throw)

    def http_get(self, url):
        return self.session.get('https://{0}{1}'.format(self.domain, url), allow_redirects=False, verify=False)

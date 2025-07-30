from syncloudlib.integration.ssh import run_ssh
import re


class LosetupEntry:
    def __init__(self, device, file):
        self.file = file
        self.device = device

    def is_deleted(self):
        return '(deleted)' in self.file


class MountEntry:
    def __init__(self, device):
        self.device = device


def loop_device_cleanup(host, dev_file, password):
    print('cleanup')
    for mount in parse_mount(run_ssh(host, 'mount', password=password)):
        if dev_file == mount.device:
            run_ssh(host, 'umount {0}'.format(mount.device), throw=False, password=password)

    for loop in parse_losetup(run_ssh(host, 'losetup', password=password)):
        if loop.file == dev_file or loop.is_deleted():
            run_ssh(host, 'losetup -d {0}'.format(loop.device), throw=False, password=password)

    run_ssh(host, 'losetup', password=password)

    for loop in run_ssh(host, 'dmsetup ls', password=password).splitlines():
        if 'loop0p1' in loop:
            run_ssh(host, 'sudo dmsetup remove loop0p1', password=password)
        if 'loop0p2' in loop:
            run_ssh(host, 'sudo dmsetup remove loop0p2', password=password)

    run_ssh(host, 'rm -rf {0}'.format(dev_file), throw=False, password=password)


def parse_losetup(output):
    entries = []
    for line in output.splitlines():
        match = re.match(r'(.*[0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+(.*)\s+([0-9]+)\s+([0-9]+)', line.strip())
        if match:
            entry = LosetupEntry(match.group(1).strip(), match.group(6).strip())
            entries.append(entry)
    return entries


def parse_mount(output):
    entries = []
    for line in output.splitlines():
        match = re.match(r'(.*)\son\s.*', line.strip())
        if match:
            entry = MountEntry(match.group(1).strip())
            entries.append(entry)
    return entries


def loop_device_add(host, fs, dev_file, password):
    print('adding loop device')
    run_ssh(host, 'dd if=/dev/zero bs=1M count=10 of={0}'.format(dev_file), password=password)
    loop = run_ssh(host, 'losetup -f --show {0}'.format(dev_file), password=password)
    run_ssh(host, 'mkfs.{0} {1}'.format(fs, loop), password=password)
    return loop 

from syncloudlib.integration.loop import parse_losetup, parse_mount


def test_parse_losetup_output():
    output = '''
/dev/loop27         0      0         0  0 /tmp/disk                                          0     512
/dev/loop17         0      0         1  1 /var/lib/snapd/snaps/testapp_x1.snap               0     512
/dev/loop8          0      0         1  1 /var/lib/snapd/snaps/gnome-3-28-1804_161.snap      0     512
/dev/loop25         0      0         0  0 /tmp/disk (deleted)                                0     512
/dev/loop15         0      0         1  1 /var/lib/snapd/snaps/core20_1081.snap              0     512
'''
    entries = parse_losetup(output)
    assert len(entries) == 5
    assert entries[0].device == '/dev/loop27'
    assert entries[0].file == '/tmp/disk'
    assert not entries[0].is_deleted()
    assert entries[3].device == '/dev/loop25'
    assert entries[3].file == '/tmp/disk (deleted)'
    assert entries[3].is_deleted()


def test_parse_mount_output():
    output = '''
/var/lib/snapd/snaps/platform_x1.snap on /snap/platform/x1 type squashfs (ro,nodev,relatime,x-gdu.hide)
/var/lib/snapd/snaps/testapp_x1.snap on /snap/testapp/x1 type squashfs (ro,nodev,relatime,x-gdu.hide)
/dev/loop27 on /tmp/test type ext4 (rw,relatime)
/dev/loop28 on /tmp/test type ext4 (rw,relatime)
'''
    entries = parse_mount(output)
    assert len(entries) == 4
    assert entries[2].device == '/dev/loop27'
    assert entries[3].device == '/dev/loop28'

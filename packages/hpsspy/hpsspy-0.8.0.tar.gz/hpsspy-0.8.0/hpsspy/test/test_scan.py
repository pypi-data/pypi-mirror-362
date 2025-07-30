# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""
hpsspy.test.test_scan
~~~~~~~~~~~~~~~~~~~~~

Test the functions in the scan subpackage.
"""
import pytest
import json
import re
from logging import DEBUG
from importlib.resources import files
from ..scan import (validate_configuration, compile_map, files_to_hpss,
                    find_missing, process_missing, extract_directory_name,
                    iterrsplit, scan_disk, scan_hpss, physical_disks, _options)
from .test_os import mock_call, MockFile


@pytest.fixture
def test_config():
    """Provide access to configuration file.
    """
    class TestConfig(object):
        """Simple class to set config_file attributes.
        """
        def __init__(self):
            self.config_name = str(files('hpsspy').joinpath('test', 't', 'test_scan.json'))
            with open(self.config_name, 'rb') as config_file:
                self.config = json.loads(config_file.read().decode())

    return TestConfig()


def test_iterrsplit():
    """Test reverse re-joining a string.
    """
    results = ['d', 'c_d', 'b_c_d', 'a_b_c_d']
    for i, s in enumerate(iterrsplit('a_b_c_d', '_')):
        assert s == results[i]


def test_compile_map(test_config):
    """Test compiling regular expressions in the JSON configuration file.
    """
    new_map = compile_map(test_config.config, 'data')
    assert new_map['__exclude__'] == frozenset(['README.html'])
    for conf in test_config.config['data']:
        if conf != '__exclude__':
            for nm in new_map[conf]:
                assert nm[0].pattern in test_config.config['data'][conf]
                assert nm[1] == test_config.config['data'][conf][nm[0].pattern]
    #
    # Catch bad compiles
    #
    test_config.config['redux']['d1'] = {'d1/(r\\d{5,4})/.*$': 'd1/d1_\\1.tar'}
    with pytest.raises(re.error) as err:
        new_map = compile_map(test_config.config, 'redux')
    assert err.value.colno == 9


def test_files_to_hpss(test_config):
    """Test conversion of JSON files to directory dictionary.
    """
    hpss_map, config = files_to_hpss(test_config.config_name, 'data')
    assert config['root'] == '/temporary'
    for key in hpss_map['d2']:
        assert key[0].pattern in test_config.config['data']['d2']
        assert key[1] == test_config.config['data']['d2'][key[0].pattern]
    hpss_map, config = files_to_hpss('desi.json', 'datachallenge')
    desi_map = {"dc2/batch/.*$": "dc2/batch.tar",
                "dc2/([^/]+\\.txt)$": "dc2/\\1",
                "dc2/templates/[^/]+$": "dc2/templates/templates_files.tar"
                }
    for key in hpss_map['dc2']:
        assert key[0].pattern in desi_map
        assert key[1] == desi_map[key[0].pattern]
    hpss_map, config = files_to_hpss('foo.json', 'dr8')
    assert 'casload' in hpss_map


def test_physical_disks():
    """Test physical disk path setup.
    """
    release_root = '/foo/bar/baz/data'
    config = {'root': '/foo/bar/baz'}
    pd = physical_disks(release_root, config)
    assert pd == (release_root,)
    config['physical_disks'] = None
    pd = physical_disks(release_root, config)
    assert pd == (release_root,)
    config['physical_disks'] = False
    pd = physical_disks(release_root, config)
    assert pd == (release_root,)
    config['physical_disks'] = []
    pd = physical_disks(release_root, config)
    assert pd == (release_root,)
    config['physical_disks'] = ['baz']
    pd = physical_disks(release_root, config)
    assert pd == (release_root,)
    config['physical_disks'] = ['baz0', 'baz1', 'baz2']
    pd = physical_disks(release_root, config)
    assert set(pd) == set(['/foo/bar/baz0/data',
                           '/foo/bar/baz1/data',
                           '/foo/bar/baz2/data'])
    config['physical_disks'] = ['/foo/bar0/baz',
                                '/foo/bar1/baz',
                                '/foo/bar2/baz']
    pd = physical_disks(release_root, config)
    assert set(pd) == set(['/foo/bar0/baz/data',
                           '/foo/bar1/baz/data',
                           '/foo/bar2/baz/data'])


def test_physical_disks_with_symlinks(monkeypatch, mock_call):
    """Test physical disk path setup with a symlink.
    """
    il0 = mock_call([True, False, False])
    rl0 = mock_call(['../baz1/data'])
    monkeypatch.setattr('os.path.islink', il0)
    monkeypatch.setattr('os.readlink', rl0)
    release_root = '/foo/bar/baz/data'
    config = {'root': '/foo/bar/baz'}
    config['physical_disks'] = ['baz0', 'baz1', 'baz2']
    pd = physical_disks(release_root, config)
    assert set(pd) == set(['/foo/bar/baz1/data',
                           '/foo/bar/baz2/data'])
    il1 = mock_call([True, False, False])
    rl1 = mock_call(['../../bar1/baz/data'])
    monkeypatch.setattr('os.path.islink', il1)
    monkeypatch.setattr('os.readlink', rl1)
    config['physical_disks'] = ['/foo/bar0/baz',
                                '/foo/bar1/baz',
                                '/foo/bar2/baz']
    pd = physical_disks(release_root, config)
    assert set(pd) == set(['/foo/bar1/baz/data',
                           '/foo/bar2/baz/data'])


def test_validate_configuration_no_file(caplog):
    """Test the configuration file validator with a missing file.
    """
    status = validate_configuration('foo.bar')
    assert status == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == "foo.bar might not be a JSON file!"
    assert caplog.records[1].levelname == 'CRITICAL'
    assert caplog.records[1].message == "foo.bar does not exist. Try again."


def test_validate_configuration_invalid_file(caplog):
    """Test the configuration file validator with an invalid file.
    """
    invalid = str(files('hpsspy.test').joinpath('t', 'invalid_file'))
    status = validate_configuration(invalid)
    assert status == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == f"{invalid} might not be a JSON file!"
    assert caplog.records[1].levelname == 'CRITICAL'
    assert caplog.records[1].message == f"{invalid} is not valid JSON."


def test_validate_configuration_valid_file(caplog, test_config):
    """Test the configuration file validator with a valid file.
    """
    status = validate_configuration(test_config.config_name)
    assert status == 0


def test_validate_configuration_partial_valid_file(caplog, tmp_path, test_config):
    """Test the configuration file validator with a valid file but missing some pieces.
    """
    c = test_config.config.copy()
    del c['__config__']
    tmp = tmp_path / 'missing_config.json'
    with tmp.open('w') as fd:
        json.dump(c, fd)
    status = validate_configuration(str(tmp))
    assert status == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert caplog.records[0].message == f"{tmp} does not contain a '__config__' section."


def test_validate_configuration_another_partial_valid_file(caplog, tmp_path, test_config):
    """Test the configuration file validator with a valid file but missing some other pieces.
    """
    c = test_config.config.copy()
    del c['__config__']['physical_disks']
    tmp = tmp_path / 'missing_physical.json'
    with tmp.open('w') as fd:
        json.dump(c, fd)
    status = validate_configuration(str(tmp))
    assert status == 0
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == f"{tmp} '__config__' section does not contain an entry for 'physical_disks'."


def test_validate_configuration_yet_another_partial_valid_file(caplog, tmp_path, test_config):
    """Test the configuration file validator with a valid file but missing some other pieces.
    """
    c = test_config.config.copy()
    del c['redux']['__exclude__']
    tmp = tmp_path / 'missing_exclude.json'
    with tmp.open('w') as fd:
        json.dump(c, fd)
    status = validate_configuration(str(tmp))
    assert status == 0
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[0].message == "Section 'redux' should at least have an '__exclude__' entry."


def test_validate_configuration_bad_regex(caplog, tmp_path, test_config):
    """Test the configuration file validator with an invalid regular expression.
    """
    c = test_config.config.copy()
    c['redux']['d1'] = {'d1/(r\\d{5,4})/.*$': 'd1/d1_\\1.tar'}
    tmp = tmp_path / 'bad_regex.json'
    with tmp.open('w') as fd:
        json.dump(c, fd)
    status = validate_configuration(str(tmp))
    assert status == 1
    assert caplog.records[0].levelname == 'CRITICAL'
    assert caplog.records[0].message == "Regular Expression error detected in section 'redux'!"


def test_extract_directory_name():
    """Test conversion of HTAR file name back into directory name.
    """
    d = extract_directory_name(('images/fpc_analysis/' +
                                'protodesi_images_fpc_analysis_' +
                                'stability_dither-33022.tar'))
    assert d == 'stability_dither-33022'
    d = extract_directory_name(('buzzard/buzzard_v1.6_desicut/8/' +
                                'buzzard_v1.6_desicut_8_7.tar'))
    assert d == '7'
    d = extract_directory_name('foo/bar/batch.tar')
    assert d == 'batch'
    d = extract_directory_name('batch.tar')
    assert d == 'batch'


def test_options(monkeypatch):
    """Test command-line parsing.
    """
    monkeypatch.setattr('sys.argv', ['missing_from_hpss', '--test', '--verbose',
                                     'config', 'release'])
    options = _options()
    assert options.test
    assert options.verbose
    assert options.config == 'config'


def test_scan_hpss_cached(caplog):
    """Test scan_hpss() using an existing cache.
    """
    caplog.set_level(DEBUG)
    cache = str(files('hpsspy.test').joinpath('t', 'hpss_cache.csv'))
    hpss_files = scan_hpss('/hpss/root', cache)
    assert hpss_files['foo'][0] == 1
    assert hpss_files['bar'][1] == 3
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == f"Found cache file {cache}."


def test_scan_hpss(monkeypatch, caplog, tmp_path, mock_call):
    """Test scan_hpss() using an existing cache.
    """
    d = MockFile(True, 'subdir')
    f = MockFile(False, 'name')
    ff = MockFile(False, 'subname')
    ld = mock_call([[d, f], [ff]])
    i = mock_call([False])
    monkeypatch.setattr('hpsspy.os._os.listdir', ld)
    monkeypatch.setattr('hpsspy.os._os.islink', i)
    caplog.set_level(DEBUG)
    cache = tmp_path / 'temp_hpss_cache.csv'
    hpss_files = scan_hpss('/hpss/root', str(cache))
    # print(hpss_files)
    assert hpss_files['/path/name'][0] == 12345
    assert hpss_files['/path/subname'][1] == 54321
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == "No HPSS cache file, starting scan at /hpss/root."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "Scanning HPSS directory /hpss/root."
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "Scanning HPSS directory /hpss/root/subdir."
    expected_csv = """Name,Size,Mtime
/path/name,12345,54321
/path/subname,12345,54321
"""
    with cache.open() as csv:
        data = csv.read()
    assert data == expected_csv
    assert ld.args[0] == ('/hpss/root', )
    assert ld.args[1] == ('/hpss/root/subdir', )
    assert i.args[0] == ('/hpss/root/subdir', )


def test_scan_disk_cached(monkeypatch, caplog, mock_call):
    """Test the scan_disk() function using an existing cache.
    """
    m = mock_call([True])
    monkeypatch.setattr('os.path.exists', m)
    caplog.set_level(DEBUG)
    assert scan_disk(['/foo', '/bar'], 'cache_file')
    assert m.args[0] == ('cache_file', )
    assert caplog.records[0].levelname == 'DEBUG'
    assert caplog.records[0].message == "Using existing file cache: cache_file"


def test_scan_disk(monkeypatch, caplog, tmp_path, mock_call):
    """Test the scan_disk() function.
    """
    f = MockFile(False, 'name')
    ff = MockFile(False, 'subname')
    m = mock_call([[('/foo', ['subdir'], ['name']),
                    ('/foo/subdir', [], ['subname'])],
                   [('/bar', ['subdir'], ['name']),
                    ('/bar/subdir', [], ['subname'])]])
    # i = mock_call([False, False, False, False])
    s = mock_call([f, f, ff, f, ff])
    monkeypatch.setattr('os.walk', m)
    # monkeypatch.setattr('os.path.islink', i)
    monkeypatch.setattr('os.stat', s)
    caplog.set_level(DEBUG)
    cache = tmp_path / 'cache_file.csv'
    foo = scan_disk(['/foo', '/bar'], str(cache), overwrite=True)
    assert foo
    assert m.args[0] == ('/foo', )
    assert m.args[1] == ('/bar', )
    assert s.args[0] == (str(cache), )
    assert s.args[1] == ('/foo/name', )
    assert s.args[2] == ('/foo/subdir/subname', )
    assert s.args[3] == ('/bar/name', )
    assert s.args[4] == ('/bar/subdir/subname', )
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == "No disk cache file, starting scan."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "Starting os.walk at /foo."
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "Scanning disk directory /foo."
    assert caplog.records[3].levelname == 'DEBUG'
    assert caplog.records[3].message == "Scanning disk directory /foo/subdir."
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == "Starting os.walk at /bar."
    assert caplog.records[5].levelname == 'DEBUG'
    assert caplog.records[5].message == "Scanning disk directory /bar."
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == "Scanning disk directory /bar/subdir."
    expected_csv = """Name,Size,Mtime
name,12345,54321
subdir/subname,12345,54321
name,12345,54321
subdir/subname,12345,54321
"""
    with cache.open() as csv:
        data = csv.read()
    assert data == expected_csv


def test_scan_disk_exception(monkeypatch, caplog, tmp_path, mock_call):
    """Test the scan_disk() function, throwing an exception.
    """
    err = OSError(12345, 'foobar', 'foo.txt')
    f = MockFile(False, 'name')
    ff = MockFile(False, 'subname')
    m = mock_call([[('/foo', ['subdir'], ['name']),
                    ('/foo/subdir', [], ['subname'])],
                   [('/bar', ['subdir'], ['name']),
                    ('/bar/subdir', [], ['subname'])]], raises=err)
    # i = mock_call([False, False, False, False])
    s = mock_call([f, f, ff, f, ff])
    monkeypatch.setattr('os.walk', m)
    # monkeypatch.setattr('os.path.islink', i)
    monkeypatch.setattr('os.stat', s)
    caplog.set_level(DEBUG)
    cache = tmp_path / 'cache_file.csv'
    foo = scan_disk(['/foo', '/bar'], str(cache), overwrite=True)
    assert not foo
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == "No disk cache file, starting scan."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "Starting os.walk at /foo."
    assert caplog.records[2].levelname == 'ERROR'
    assert caplog.records[2].message == "Exception encountered while traversing /foo!"
    assert caplog.records[3].levelname == 'ERROR'
    assert caplog.records[3].message == "foobar"


def test_scan_disk_stat_exception(monkeypatch, caplog, tmp_path, mock_call):
    """Test the scan_disk() function, throwing an exception on os.stat.
    """
    err = PermissionError(13, 'Permission denied', '/bar/subdir/subname')
    f = MockFile(False, 'name')
    ff = MockFile(False, 'subname')
    m = mock_call([[('/foo', ['subdir'], ['name']),
                    ('/foo/subdir', [], ['subname'])],
                   [('/bar', ['subdir'], ['name']),
                    ('/bar/subdir', [], ['subname'])]])
    # i = mock_call([False, False, False, False])
    s = mock_call([f, f, ff, f, ff], raises=[None, None, None, None, err])
    monkeypatch.setattr('os.walk', m)
    # monkeypatch.setattr('os.path.islink', i)
    monkeypatch.setattr('os.stat', s)
    caplog.set_level(DEBUG)
    cache = tmp_path / 'cache_file.csv'
    foo = scan_disk(['/foo', '/bar'], str(cache), overwrite=True)
    assert foo
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == "No disk cache file, starting scan."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "Starting os.walk at /foo."
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "Scanning disk directory /foo."
    assert caplog.records[3].levelname == 'DEBUG'
    assert caplog.records[3].message == "Scanning disk directory /foo/subdir."
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == "Starting os.walk at /bar."
    assert caplog.records[5].levelname == 'DEBUG'
    assert caplog.records[5].message == "Scanning disk directory /bar."
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == "Scanning disk directory /bar/subdir."
    assert caplog.records[7].levelname == 'ERROR'
    assert caplog.records[7].message == "Permission denied: /bar/subdir/subname"


def test_scan_disk_weird_filename(monkeypatch, caplog, tmp_path, mock_call):
    """Test the scan_disk() function, with an oddball filename.
    """
    f = MockFile(False, 'name')
    ff = MockFile(False, 'subname')
    m = mock_call([[('/foo', ['subdir'], ['name']),
                    ('/foo/subdir', [], ['subname'])],
                   [('/bar', ['subdir'], ['name']),
                    ('/bar/subdir', [], ['Vpeak60_subhalos_id-\udcecd-upid.h5'])]])
    # i = mock_call([False, False, False, False])
    s = mock_call([f, f, ff, f, ff])
    monkeypatch.setattr('os.walk', m)
    # monkeypatch.setattr('os.path.islink', i)
    monkeypatch.setattr('os.stat', s)
    caplog.set_level(DEBUG)
    cache = tmp_path / 'cache_file.csv'
    foo = scan_disk(['/foo', '/bar'], str(cache), overwrite=True)
    assert foo
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == "No disk cache file, starting scan."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "Starting os.walk at /foo."
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "Scanning disk directory /foo."
    assert caplog.records[3].levelname == 'DEBUG'
    assert caplog.records[3].message == "Scanning disk directory /foo/subdir."
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == "Starting os.walk at /bar."
    assert caplog.records[5].levelname == 'DEBUG'
    assert caplog.records[5].message == "Scanning disk directory /bar."
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == "Scanning disk directory /bar/subdir."
    assert caplog.records[7].levelname == 'ERROR'
    assert caplog.records[7].message == (r"Could not write b'/bar/subdir/Vpeak60_subhalos_id-\xed\xb3\xacd-upid.h5'"
                                         " to cache file due to unusual characters!")
    assert caplog.records[8].levelname == 'ERROR'
    assert caplog.records[8].message == (r"Message was: 'utf-8' codec can't encode character '\udcec'"
                                         " in position 27: surrogates not allowed.")


def test_find_missing(test_config, tmpdir, caplog):
    """Test comparison of disk files to HPSS files.
    """
    caplog.set_level(DEBUG)
    hpss_map = compile_map(test_config.config, 'data')
    hpss_files = {'data_files.tar': (1000, 1552494004),
                  'd1/batch.tar': (1000, 1552494004),
                  'd1/SINGLE_FILE.txt': (100, 1552494004)}
    disk_files_cache = str(files('hpsspy.test').joinpath('t', 'test_scan_disk_cache.csv'))
    missing_files = tmpdir.join('missing_files_data.json')
    status = find_missing(hpss_map, hpss_files, disk_files_cache, str(missing_files),
                          report=10, limit=1)
    assert status
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == 'README.html is excluded.'
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "pattern_used[r'[^/]+$'] += 1"
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "r[1] = r'data_files.tar'"
    assert caplog.records[3].levelname == 'DEBUG'
    assert caplog.records[3].message == 'foo.txt in data_files.tar.'
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == "pattern_used[r'[^/]+$'] += 1"
    assert caplog.records[5].levelname == 'DEBUG'
    assert caplog.records[5].message == "r[1] = r'data_files.tar'"
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == 'bar.txt in data_files.tar.'
    assert caplog.records[7].levelname == 'DEBUG'
    assert caplog.records[7].message == r"pattern_used[r'd1/([^/]+\.txt)$'] += 1"
    assert caplog.records[8].levelname == 'DEBUG'
    assert caplog.records[8].message == r"r[1] = r'd1/\1'"
    assert caplog.records[9].levelname == 'DEBUG'
    assert caplog.records[9].message == 'd1/SINGLE_FILE.txt in d1/SINGLE_FILE.txt.'

    assert caplog.records[10].levelname == 'DEBUG'
    assert caplog.records[10].message == "pattern_used[r'd1/spectro/data/.*$'] += 1"
    assert caplog.records[11].levelname == 'DEBUG'
    assert caplog.records[11].message == "r[1] = r'AUTOMATED'"
    assert caplog.records[12].levelname == 'DEBUG'
    assert caplog.records[12].message == "d1/spectro/data/raw1.txt is backed up by some other automated process."
    assert caplog.records[13].levelname == 'DEBUG'
    assert caplog.records[13].message == "pattern_used[r'd1/spectro/data/.*$'] += 1"
    assert caplog.records[14].levelname == 'DEBUG'
    assert caplog.records[14].message == "r[1] = r'AUTOMATED'"
    assert caplog.records[15].levelname == 'DEBUG'
    assert caplog.records[15].message == "d1/spectro/data/raw2.txt is backed up by some other automated process."

    assert caplog.records[16].levelname == 'DEBUG'
    assert caplog.records[16].message == "pattern_used[r'd1/batch/.*$'] += 1"
    assert caplog.records[17].levelname == 'DEBUG'
    assert caplog.records[17].message == "r[1] = r'd1/batch.tar'"
    assert caplog.records[18].levelname == 'DEBUG'
    assert caplog.records[18].message == "d1/batch/a.txt in d1/batch.tar."
    assert caplog.records[19].levelname == 'WARNING'
    assert caplog.records[19].message == 'd1/batch/a.txt is newer than d1/batch.tar, marking as missing!'
    assert caplog.records[20].levelname == 'DEBUG'
    assert caplog.records[20].message == "pattern_used[r'd1/batch/.*$'] += 1"
    assert caplog.records[21].levelname == 'DEBUG'
    assert caplog.records[21].message == "r[1] = r'd1/batch.tar'"
    assert caplog.records[22].levelname == 'DEBUG'
    assert caplog.records[22].message == "d1/batch/b.txt in d1/batch.tar."
    assert caplog.records[23].levelname == 'WARNING'
    assert caplog.records[23].message == 'd1/batch/b.txt is newer than d1/batch.tar, marking as missing!'

    assert caplog.records[24].levelname == 'DEBUG'
    assert caplog.records[24].message == "pattern_used[r'd2/(batch|fiberassign)/.*$'] += 1"
    assert caplog.records[25].levelname == 'DEBUG'
    assert caplog.records[25].message == r"r[1] = r'd2/d2_\1.tar'"
    assert caplog.records[26].levelname == 'DEBUG'
    assert caplog.records[26].message == "d2/fiberassign/a.txt in d2/d2_fiberassign.tar."

    assert caplog.records[27].levelname == 'INFO'
    assert caplog.records[27].message == "       10 files scanned."

    assert caplog.records[28].levelname == 'DEBUG'
    assert caplog.records[28].message == "pattern_used[r'd2/(batch|fiberassign)/.*$'] += 1"
    assert caplog.records[29].levelname == 'DEBUG'
    assert caplog.records[29].message == r"r[1] = r'd2/d2_\1.tar'"
    assert caplog.records[30].levelname == 'DEBUG'
    assert caplog.records[30].message == "d2/fiberassign/b.txt in d2/d2_fiberassign.tar."

    assert caplog.records[31].levelname == 'DEBUG'
    assert caplog.records[31].message == "pattern_used[r'd2/spectro/redux/([0-9a-zA-Z_-]+)/preproc/.*$'] += 1"
    assert caplog.records[32].levelname == 'DEBUG'
    assert caplog.records[32].message == "r[1] = r'EXCLUDE'"
    assert caplog.records[33].levelname == 'DEBUG'
    assert caplog.records[33].message == "d2/spectro/redux/specprod/preproc/excluded.txt is excluded from backups."

    assert caplog.records[34].levelname == 'WARNING'
    assert caplog.records[34].message == 'Directory d3 is not described in the configuration!'

    assert caplog.records[35].levelname == 'WARNING'
    assert caplog.records[35].message == 'Directory d4 is not configured!'

    assert caplog.records[36].levelname == 'INFO'
    assert caplog.records[36].message == "Pattern 'd1/templates/[^/]+$' was never used, maybe files have been removed from disk?"

    assert caplog.records[45].levelname == 'DEBUG'
    assert caplog.records[45].message == "data_files.tar is a valid backup."
    assert caplog.records[46].levelname == 'DEBUG'
    assert caplog.records[46].message == "d1/SINGLE_FILE.txt is a valid backup."
    assert caplog.records[47].levelname == 'INFO'
    assert caplog.records[47].message == "d1/batch.tar is 10000 bytes."
    assert caplog.records[48].levelname == 'DEBUG'
    assert caplog.records[48].message == "Adding d1/batch.tar to missing backups."
    assert caplog.records[49].levelname == 'INFO'
    assert caplog.records[49].message == "d2/d2_fiberassign.tar is 2147483648 bytes."
    assert caplog.records[50].levelname == 'ERROR'
    assert caplog.records[50].message == "HPSS file d2/d2_fiberassign.tar would be too large, skipping backup!"
    assert caplog.records[51].levelname == 'INFO'
    assert caplog.records[51].message == "2 files selected for backup."

    # assert False
    with open(missing_files) as j:
        missing = json.load(j)
    assert tuple(missing.keys()) == ('d1/batch.tar', )
    assert missing['d1/batch.tar']['files'] == ['d1/batch/a.txt', 'd1/batch/b.txt']
    assert missing['d1/batch.tar']['size'] == 10000
    assert missing['d1/batch.tar']['newer']
    assert missing['d1/batch.tar']['exists']


def test_find_missing_missing_files(test_config, tmpdir, caplog):
    """Test comparison of disk files to HPSS files, with unconfigured files.
    """
    caplog.set_level(DEBUG)
    hpss_map = compile_map(test_config.config, 'data')
    hpss_files = {'data_files.tar': (1000, 1552494004),
                  'd1/batch.tar': (1000, 1552494004),
                  'd1/SINGLE_FILE.txt': (100, 1552494004)}
    disk_files_cache = str(files('hpsspy.test').joinpath('t', 'test_scan_disk_cache_missing.csv'))
    missing_files = tmpdir.join('missing_files_data.json')
    status = find_missing(hpss_map, hpss_files, disk_files_cache, str(missing_files),
                          report=10, limit=1)
    assert not status
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == 'README.html is excluded.'
    assert caplog.records[1].levelname == 'ERROR'
    assert caplog.records[1].message == "d2/botch/file1.txt is not mapped to any file on HPSS!"
    assert caplog.records[2].levelname == 'ERROR'
    assert caplog.records[2].message == "d2/botch/file2.txt is not mapped to any file on HPSS!"
    assert caplog.records[13].levelname == 'CRITICAL'
    assert caplog.records[13].message == "Not all files would be backed up with this configuration!"


def test_find_missing_multiple_files(test_config, tmpdir, caplog):
    """Test comparison of disk files to HPSS files, with multiple matches to files.
    """
    caplog.set_level(DEBUG)
    hpss_map = compile_map(test_config.config, 'data')
    hpss_files = {'data_files.tar': (1000, 1552494004),
                  'd1/batch.tar': (1000, 1552494004),
                  'd1/SINGLE_FILE.txt': (100, 1552494004)}
    disk_files_cache = str(files('hpsspy.test').joinpath('t', 'test_scan_disk_cache_multiple.csv'))
    missing_files = tmpdir.join('missing_files_data.json')
    status = find_missing(hpss_map, hpss_files, disk_files_cache, str(missing_files),
                          report=10, limit=1)
    assert not status
    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == 'README.html is excluded.'
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "pattern_used[r'd5/spectro/redux/preproc/.*$'] += 1"
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "r[1] = r'EXCLUDE'"
    assert caplog.records[3].levelname == 'DEBUG'
    assert caplog.records[3].message == "d5/spectro/redux/preproc/excluded.txt is excluded from backups."
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == "pattern_used[r'd5/spectro/redux/([0-9a-zA-Z_-]+)/[^/]+$'] += 1"
    assert caplog.records[5].levelname == 'DEBUG'
    assert caplog.records[5].message == r"r[1] = r'd2/spectro/redux/\1/\1_files.tar'"
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == "d5/spectro/redux/preproc/excluded.txt in d2/spectro/redux/preproc/preproc_files.tar."
    assert caplog.records[7].levelname == 'ERROR'
    assert caplog.records[7].message == "d5/spectro/redux/preproc/excluded.txt is mapped to multiple files on HPSS!"
    assert caplog.records[8].levelname == 'INFO'
    assert caplog.records[8].message == "d2/spectro/redux/preproc/preproc_files.tar is 50 bytes."
    assert caplog.records[9].levelname == 'DEBUG'
    assert caplog.records[9].message == "Adding d2/spectro/redux/preproc/preproc_files.tar to missing backups."
    assert caplog.records[10].levelname == 'INFO'
    assert caplog.records[10].message == "1 files selected for backup."
    assert caplog.records[11].levelname == 'CRITICAL'
    assert caplog.records[11].message == "Some files would be backed up more than once with this configuration!"


def test_process_missing(monkeypatch, caplog, mock_call):
    """Test conversion of missing files into HPSS commands.
    """
    missing_cache = str(files('hpsspy.test').joinpath('t', 'missing_cache.json'))
    getcwd = mock_call(['/working/directory', '/working/directory'])
    chdir = mock_call([None, None, None, None, None])
    isdir = mock_call([True, False, True, True, False])
    htar = mock_call([('out', ''), ('out', 'err'), ('out', ''), ('out', '')])
    hsi = mock_call(['OK', 'OK', 'OK', 'OK', 'OK', 'OK'])
    listdir = mock_call([('01', '02')])
    monkeypatch.setenv('HPSS_DIR', '/usr/local')
    monkeypatch.setattr('os.getcwd', getcwd)
    monkeypatch.setattr('os.chdir', chdir)
    monkeypatch.setattr('os.path.isdir', isdir)
    monkeypatch.setattr('os.listdir', listdir)
    monkeypatch.setattr('hpsspy.scan.htar', htar)
    monkeypatch.setattr('hpsspy.os._os.hsi', hsi)
    monkeypatch.setattr('hpsspy.scan.hsi', hsi)
    caplog.set_level(DEBUG)
    process_missing(missing_cache, '/disk/root', '/hpss/root')
    assert chdir.args[0] == ('/disk/root/files', )
    assert chdir.args[1] == ('/disk/root/', )
    assert isdir.args[0] == ('/disk/root/files/test_basic_htar', )
    assert isdir.args[1] == ('/disk/root/dir_set/XX', )
    assert isdir.args[2] == ('/disk/root/dir_set/01', )
    assert isdir.args[3] == ('/disk/root/dir_set/02', )
    assert isdir.args[4] == ('/disk/root/bad_dir/test_basic_htar', )
    assert listdir.args[0] == ('/disk/root/dir_set', )
    assert caplog.records[0].levelname == 'DEBUG'
    assert caplog.records[0].message == f"Processing missing files from {missing_cache}."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "os.chdir('/disk/root/files')"
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "makedirs('/hpss/root/files', mode='2770')"
    assert caplog.records[3].levelname == 'INFO'
    assert caplog.records[3].message == "htar('-cvf', '/hpss/root/files/test_basic_htar.tar', '-H', 'crc:verify=all', 'test_basic_htar')"
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == 'out'

    assert caplog.records[5].levelname == 'DEBUG'
    Lfile = caplog.records[5].message
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == "os.chdir('/disk/root/')"
    assert caplog.records[7].levelname == 'DEBUG'
    assert caplog.records[7].message == "makedirs('/hpss/root', mode='2770')"
    assert caplog.records[8].levelname == 'INFO'
    assert caplog.records[8].message == f"htar('-cvf', '/hpss/root/test_basic_files.tar', '-H', 'crc:verify=all', '-L', '{Lfile}')"
    assert caplog.records[9].levelname == 'DEBUG'
    assert caplog.records[9].message == 'out'
    assert caplog.records[10].levelname == 'WARNING'
    assert caplog.records[10].message == 'err'
    assert caplog.records[11].levelname == 'DEBUG'
    assert caplog.records[11].message == f"os.remove('{Lfile}')"

    assert caplog.records[12].levelname == 'DEBUG'
    assert caplog.records[12].message == "os.chdir('/disk/root/dir_set')"
    assert caplog.records[13].levelname == 'DEBUG'
    assert caplog.records[13].message == "makedirs('/hpss/root/dir_set', mode='2770')"
    assert caplog.records[14].levelname == 'INFO'
    assert caplog.records[14].message == f"htar('-cvf', '/hpss/root/dir_set/test_dir_set_XX.tar', '-H', 'crc:verify=all', '01', '02')"
    assert caplog.records[15].levelname == 'DEBUG'
    assert caplog.records[15].message == 'out'

    assert caplog.records[16].levelname == 'DEBUG'
    assert caplog.records[16].message == "makedirs('/hpss/root/big_file', mode='2770')"
    assert caplog.records[17].levelname == 'INFO'
    assert caplog.records[17].message == ("hsi('put', '/disk/root/big_file/test_basic_file.dump',"
                                          " ':', '/hpss/root/big_file/test_basic_file.dump')")
    assert caplog.records[18].levelname == 'DEBUG'
    assert caplog.records[18].message == "OK"

    assert caplog.records[19].levelname == 'ERROR'
    assert caplog.records[19].message == "Could not find directories corresponding to bad_dir/test_basic_htar.tar!"

    assert caplog.records[20].levelname == 'DEBUG'
    assert caplog.records[20].message == "os.chdir('/working/directory')"

    assert hsi.args[0] == ('mkdir', '-p', '-m', '2770', '/hpss/root/files')
    assert hsi.args[1] == ('mkdir', '-p', '-m', '2770', '/hpss/root')
    assert hsi.args[2] == ('mkdir', '-p', '-m', '2770', '/hpss/root/dir_set')
    assert hsi.args[3] == ('mkdir', '-p', '-m', '2770', '/hpss/root/big_file')
    assert hsi.args[4] == ('put', '/disk/root/big_file/test_basic_file.dump', ':', '/hpss/root/big_file/test_basic_file.dump')

    assert htar.args[0] == ('-cvf', '/hpss/root/files/test_basic_htar.tar', '-H', 'crc:verify=all', 'test_basic_htar')
    assert htar.args[1] == ('-cvf', '/hpss/root/test_basic_files.tar', '-H', 'crc:verify=all', '-L', Lfile)
    assert htar.args[2] == ('-cvf', '/hpss/root/dir_set/test_dir_set_XX.tar', '-H', 'crc:verify=all', '01', '02')


def test_process_missing_test_mode(monkeypatch, caplog, mock_call):
    """Test conversion of missing files into HPSS commands in test mode.
    """
    missing_cache = str(files('hpsspy.test').joinpath('t', 'missing_cache.json'))
    getcwd = mock_call(['/working/directory', '/working/directory'])
    chdir = mock_call([None, None, None, None, None])
    isdir = mock_call([True, False, True, True, False])
    htar = mock_call([('out', ''), ('out', 'err'), ('out', ''), ('out', '')])
    hsi = mock_call(['OK', 'OK', 'OK', 'OK', 'OK', 'OK'])
    listdir = mock_call([('01', '02')])
    monkeypatch.setenv('HPSS_DIR', '/usr/local')
    monkeypatch.setattr('os.getcwd', getcwd)
    monkeypatch.setattr('os.chdir', chdir)
    monkeypatch.setattr('os.path.isdir', isdir)
    monkeypatch.setattr('os.listdir', listdir)
    monkeypatch.setattr('hpsspy.scan.htar', htar)
    monkeypatch.setattr('hpsspy.os._os.hsi', hsi)
    monkeypatch.setattr('hpsspy.scan.hsi', hsi)
    caplog.set_level(DEBUG)
    process_missing(missing_cache, '/disk/root', '/hpss/root', dirmode='2775', test=True)
    assert chdir.args[0] == ('/disk/root/files', )
    assert chdir.args[1] == ('/disk/root/', )
    assert isdir.args[0] == ('/disk/root/files/test_basic_htar', )
    assert isdir.args[1] == ('/disk/root/dir_set/XX', )
    assert isdir.args[2] == ('/disk/root/dir_set/01', )
    assert isdir.args[3] == ('/disk/root/dir_set/02', )
    assert isdir.args[4] == ('/disk/root/bad_dir/test_basic_htar', )
    assert listdir.args[0] == ('/disk/root/dir_set', )
    assert caplog.records[0].levelname == 'DEBUG'
    assert caplog.records[0].message == f"Processing missing files from {missing_cache}."
    assert caplog.records[1].levelname == 'DEBUG'
    assert caplog.records[1].message == "os.chdir('/disk/root/files')"
    assert caplog.records[2].levelname == 'DEBUG'
    assert caplog.records[2].message == "makedirs('/hpss/root/files', mode='2775')"
    assert caplog.records[3].levelname == 'INFO'
    assert caplog.records[3].message == "htar('-cvf', '/hpss/root/files/test_basic_htar.tar', '-H', 'crc:verify=all', 'test_basic_htar')"
    assert caplog.records[4].levelname == 'DEBUG'
    assert caplog.records[4].message == 'Test mode, skipping htar command.'

    assert caplog.records[5].levelname == 'DEBUG'
    Lfile = caplog.records[5].message
    assert caplog.records[6].levelname == 'DEBUG'
    assert caplog.records[6].message == 'test_file3.txt\ntest_file4.sha256sum\n'

    assert caplog.records[7].levelname == 'DEBUG'
    assert caplog.records[7].message == "os.chdir('/disk/root/')"
    assert caplog.records[8].levelname == 'DEBUG'
    assert caplog.records[8].message == "makedirs('/hpss/root', mode='2775')"
    assert caplog.records[9].levelname == 'INFO'
    assert caplog.records[9].message == f"htar('-cvf', '/hpss/root/test_basic_files.tar', '-H', 'crc:verify=all', '-L', '{Lfile}')"
    assert caplog.records[10].levelname == 'DEBUG'
    assert caplog.records[10].message == 'Test mode, skipping htar command.'
    assert caplog.records[11].levelname == 'DEBUG'
    assert caplog.records[11].message == f"os.remove('{Lfile}')"

    assert caplog.records[12].levelname == 'DEBUG'
    assert caplog.records[12].message == "os.chdir('/disk/root/dir_set')"
    assert caplog.records[13].levelname == 'DEBUG'
    assert caplog.records[13].message == "makedirs('/hpss/root/dir_set', mode='2775')"
    assert caplog.records[14].levelname == 'INFO'
    assert caplog.records[14].message == f"htar('-cvf', '/hpss/root/dir_set/test_dir_set_XX.tar', '-H', 'crc:verify=all', '01', '02')"
    assert caplog.records[15].levelname == 'DEBUG'
    assert caplog.records[15].message == 'Test mode, skipping htar command.'

    assert caplog.records[16].levelname == 'DEBUG'
    assert caplog.records[16].message == "makedirs('/hpss/root/big_file', mode='2775')"
    assert caplog.records[17].levelname == 'INFO'
    assert caplog.records[17].message == ("hsi('put', '/disk/root/big_file/test_basic_file.dump',"
                                          " ':', '/hpss/root/big_file/test_basic_file.dump')")
    assert caplog.records[18].levelname == 'DEBUG'
    assert caplog.records[18].message == "Test mode, skipping hsi command."

    assert caplog.records[19].levelname == 'ERROR'
    assert caplog.records[19].message == "Could not find directories corresponding to bad_dir/test_basic_htar.tar!"

    assert caplog.records[20].levelname == 'DEBUG'
    assert caplog.records[20].message == "os.chdir('/working/directory')"

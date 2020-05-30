# coding: utf-8
# Module: tests
# Created on: 27.01.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

from __future__ import print_function
import os
import sys
import unittest
import shutil
import time
from collections import defaultdict
import mock

cwd = os.path.dirname(os.path.abspath(__file__+"/../../"))
configdir = os.path.join(cwd, 'config')


# Fake test objects

def fake_log(msg, level=0):
    if not isinstance(msg, str):
        raise TypeError('log message must be of str type!')


class FakeAddon(object):
    def __init__(self, id_='test.addon'):
        self._id = id_
        self._settings = {}

    def getAddonInfo(self, info_id):
        if info_id == 'path':
            return cwd
        elif info_id == 'profile':
            return configdir
        elif info_id == 'id':
            return self._id
        elif info_id == 'version':
            return '0.0.1'
        else:
            return ''

    def getSetting(self, setting_id):
        return self._settings.get(setting_id, '')

    def setSetting(self, setting_id, value):
        self._settings[setting_id] = value

    def getLocalizedString(self, id_):
        return {32000: u'Привет, мир!', 32001: u'Я тебя люблю.'}[id_]


class FakeWindow(object):
    def __init__(self, id_=-1):
        self._contents = defaultdict(str)

    def getProperty(self, key):
        return self._contents[key]

    def setProperty(self, key, value):
        self._contents[key] = value

    def clearProperty(self, key):
        del self._contents[key]

# Mock Kodi Python API

mock_xbmcaddon = mock.MagicMock()
mock_xbmcaddon.Addon.side_effect = FakeAddon

mock_xbmc = mock.MagicMock()
mock_xbmc.LOGDEBUG = 0
mock_xbmc.LOGNOTICE = 2
mock_xbmc.translatePath.side_effect = lambda path: path
mock_xbmc.log = fake_log

mock_xbmcgui = mock.MagicMock()
mock_xbmcgui.Window = FakeWindow

sys.modules['xbmcaddon'] = mock_xbmcaddon
sys.modules['xbmc'] = mock_xbmc
sys.modules['xbmcgui'] = mock_xbmcgui

# Import our module being tested
sys.path.append(os.path.join(cwd, 'plugin.googledrive'))
sys.path.append(os.path.join(cwd, 'script.module.clouddrive.common'))

from resources.lib.provider.googledrive import GoogleDrive

# Begin tests

class AddonTestCase(unittest.TestCase):
    def test_gdrive_process_files(self):
        """
        Test addon settings normalization
        """
        gdrive = GoogleDrive()

        files = {u'files': [{u'mimeType': u'application/vnd.google-apps.folder', u'hasThumbnail': False, u'owners': [{u'permissionId': u'10773356246826176512'}], u'name': u'Photos - unsown', u'modifiedTime': u'2020-05-28T05:20:29.542Z', u'parents': [u'0AIFL1ZwF1rkjUk9PVA'], u'id': u'1929tbJai-HeSBke9HT3jmdIjiAbj23xDCmFknz4HnCM', u'trashed': False}, {u'mimeType': u'application/vnd.google-apps.folder', u'hasThumbnail': False, u'owners': [{u'permissionId': u'10773356246826176512'}], u'name': u'Archive', u'modifiedTime': u'2019-03-25T00:32:24.059Z', u'parents': [u'0AIFL1ZwF1rkjUk9PVA'], u'id': u'1ZJC-WI9BusSMDIKLtPrX7o-mufjB4VhY', u'trashed': False}, {u'mimeType': u'video/mp4', u'hasThumbnail': True, u'owners': [{u'permissionId': u'00075374721629811014'}], u'description': u'[Star] [test]', u'modifiedTime': u'2018-03-06T08:07:50.984Z', u'thumbnailLink': u'https://lh3.googleusercontent.com/0x52uJgUJvpIeA1xvtrwBKK6jvj7H-Qur0ox5VfutpsH4Vl4Ow0GG5-cZkOj-1b-ks6Vhru8od3Q=s220', u'videoMediaMetadata': {u'width': 1920, u'durationMillis': u'6965958', u'height': 1040}, u'parents': [u'0AIFL1ZwF1rkjUk9PVA'], u'size': u'3655839996', u'id': u'18cvSs9r93ysjiyt7YG6AoNWUzaUksBUnnA', u'trashed': False, u'name': u'Back.to.the.Future.1985.1080p.BluRay.x264-NODLABS.mkv'}], u'kind': u'drive#fileList'}
        parameters = {'q': "'root' in parents and not trashed", 'fields': 'files(id,name,modifiedTime,size,mimeType,description,hasThumbnail,thumbnailLink,owners(permissionId),parents,trashed,imageMediaMetadata(width),videoMediaMetadata),kind,nextPageToken', 'spaces': 'drive', 'prettyPrint': 'false'}

        items = gdrive.process_files(files, parameters)
        self.assertEqual(len(items), 3)

if __name__ == '__main__':
    unittest.main()

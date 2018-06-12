#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 theloop Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
from icx.wallet import Wallet
from icx.custom_error import FilePathIsWrong, PasswordIsNotAcceptable, NoPermissionToWriteFile, FileExists, NotAKeyStoreFile
from icx.utils import validate_key_store_file

TEST_DIR = os.path.dirname(os.path.abspath("tests/keystore_file/test_keystore.txt"))


class TestCreateWalletAndKeystoreFile(unittest.TestCase):

    def setUp(self):
        # Remove used file.
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")
        if os.path.isfile(file_path):
            os.remove(file_path)

    def test0(self):
        """ Case to create wallet successfully.
        """
        # Given
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        try:
            # When
            wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

            # Then
            prefix = wallet1.address[0:2]
            self.assertEqual(prefix, "hx")

        except FilePathIsWrong:
            self.assertFalse(True)
        except PasswordIsNotAcceptable:
            self.assertFalse(True)
        except NoPermissionToWriteFile:
            self.assertFalse(True)

        # Remove used file.
        os.remove(file_path)

    def test1(self):
        """ Case to enter a directory that does not exist.
        """
        # Given
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, 'unknown', "test_keystore.txt")

        try:
            # When
            wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        # Then
        except FilePathIsWrong:
            self.assertTrue(True)

    def test2(self):
        """ Case to enter a invalid password.
        """
        # Given
        password = "123 4"
        file_path = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

        try:
            # When
            wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        # Then
        except PasswordIsNotAcceptable:
            self.assertTrue(True)

    def test3(self):
        """ Case to enter a directory without permission to write file.
        """
        # Given
        password = "Adas21312**"
        file_path = os.path.join("/", "test_keystore.txt")

        try:
            # When
            wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        # Then
        except NoPermissionToWriteFile:
            self.assertTrue(True)

    def test4(self):
        """ Case to overwrite keystore file.
        """
        # Given
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        try:
            wallet2, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        # Then
        except FileExists:  # Raise exception that file exists.
            self.assertTrue(True)

            # Remove used file.
            os.remove(file_path)

    def test5(self):
        """ Case to enter the file, not a key_store_file.
        """
        # Given
        file_path = os.path.join(TEST_DIR, "not_a_key_store_file.txt")

        try:
            # When
            validate_key_store_file(file_path)

        # Then
        except NotAKeyStoreFile:
            self.assertTrue(True)

    def test6(self):
        """ Case to save the file in the correct format.
        """
        # Given
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        wallet1, _ = Wallet.create_keystore_file_of_wallet(file_path, password)

        # Then
        self.assertTrue(validate_key_store_file(file_path))


if __name__ == "__main__":
    unittest.main()

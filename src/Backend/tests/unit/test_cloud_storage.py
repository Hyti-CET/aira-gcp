# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module for tests for cloud storage.
"""
import unittest.mock

import hypothesis
import pytest
from hypothesis import strategies as st

from api.adapters.google import CloudStorage


@hypothesis.given(file_name=st.text())
@pytest.mark.asyncio
@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
    max_examples=1,
)
async def test_should_download(file_name: str, cloud_storage: CloudStorage) -> None:
    """
    tests it should download.
    """
    with unittest.mock.patch("builtins.open", unittest.mock.mock_open()):
        resp = await cloud_storage.download("test", file_name)
    assert cloud_storage.client.download_blob_to_file.call_count >= 1
    assert f"{cloud_storage.audio_path}/{file_name}" == resp


@pytest.mark.asyncio
async def test_should_upload_by_text(cloud_storage: CloudStorage) -> None:
    """
    tests it should upload by text.
    """
    file_name = "test-file.csv"
    resp = await cloud_storage.upload_by_text(file_name, b"test")
    blob = cloud_storage.client.bucket.return_value.blob.return_value
    assert blob.upload_from_string.call_count == 1
    assert resp == "test/test"


@pytest.mark.asyncio
async def test_should_upload_by_file_name(cloud_storage: CloudStorage) -> None:
    """
    tests it should upload by file_name.
    """
    file_name = "test-file.csv"
    with unittest.mock.patch("os.remove", unittest.mock.Mock()):
        resp = await cloud_storage.upload_by_file("test", file_name)
    blob = cloud_storage.client.bucket.return_value.blob.return_value
    assert blob.upload_from_filename.call_count == 1
    assert resp == "test/test"

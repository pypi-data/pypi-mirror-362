# -*- coding: utf-8 -*-
# Copyright (c) 2025-2025 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dataclasses import dataclass

from .base import BaseConstraint
from .constraint_builder import Path, where


class _Rule:
    @property
    def input_file_read(self) -> BaseConstraint:
        return where(
            os.getuid() == 0,
            Path.exists() & Path.is_file(),
            Path.exists() & Path.is_file() & ~Path.has_soft_link() &
            Path.is_readable() & ~Path.is_writable_to_group_or_others() &
            Path.is_consistent_to_current_user() & Path.is_size_reasonable(),
            description="current user is root"
        )

    @property
    def input_file_exec(self) -> BaseConstraint:
        return where(
            os.getuid() == 0,
            Path.exists() & Path.is_file(),
            Path.exists() & Path.is_file() & ~Path.has_soft_link() &
            Path.is_executable() & ~Path.is_writable_to_group_or_others() &
            Path.is_consistent_to_current_user() & Path.is_size_reasonable(),
            description="current user is root"
        )

    @property
    def input_dir_traverse(self) -> BaseConstraint:
        return where(
            os.getuid() == 0,
            Path.exists() & Path.is_dir(),
            Path.exists() & Path.is_dir() & ~Path.has_soft_link() & Path.is_readable() &
            Path.is_executable() & ~Path.is_writable_to_group_or_others() &
            Path.is_consistent_to_current_user(),
            description="current user is root"
        )

    @property
    def output_path_create(self) -> BaseConstraint:
        return ~Path.exists() & ~Path.is_name_too_long()

    @property
    def output_path_overwrite(self) -> BaseConstraint:
        return where(
            os.getuid() == 0,
            Path.exists() & Path.is_file(),
            Path.exists() & Path.is_file() & ~Path.has_soft_link() &
            Path.is_writable() & ~Path.is_writable_to_group_or_others() &
            Path.is_consistent_to_current_user(),
            description="current user is root"
        )

    @property
    def output_path_write(self) -> BaseConstraint:
        return where(
            Path.exists(),
            self.output_path_overwrite,
            ~Path.is_name_too_long() & Path.has_writable_parent_dir()
        )

    @property
    def output_path_append(self) -> BaseConstraint:
        return self.output_path_overwrite

    @property
    def output_dir(self) -> BaseConstraint:
        return where(
            os.getuid() == 0,
            Path.exists() & Path.is_dir(),
            Path.exists() & Path.is_dir() & ~Path.has_soft_link() &
            Path.is_writable() & ~Path.is_writable_to_group_or_others() &
            Path.is_consistent_to_current_user(),
            description="current user is root"
        )


Rule = _Rule()

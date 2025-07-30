# This file is part of async-mc-launcher-core (https://github.com/JaydenChao101/async-mc-launcher-core)
# SPDX-FileCopyrightText: Copyright (c) 2025 JaydenChao101 <jaydenchao@proton.me> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from typing import Literal, TypedDict
from .shared_types import ClientJson, ClientJsonLibrary


class _ForgeInstallProcessor(TypedDict, total=False):
    sides: list[Literal["client", "server"]]
    jar: str
    classpath: list[str]
    args: list[str]


class _ForgeInstallProfileInstall(TypedDict, total=False):
    profileName: str
    target: str
    path: str
    version: str
    filePath: str
    welcome: str
    minecraft: str
    mirrorList: str
    logo: str


class ForgeInstallProfile(TypedDict, total=False):
    spec: int
    profile: str
    version: str
    minecraft: str
    serverJarPath: str
    data: dict[str, dict[Literal["client", "server"], str]]
    processors: list[_ForgeInstallProcessor]
    libraries: list[ClientJsonLibrary]
    icon: str
    logo: str
    mirrorList: str
    welcome: str
    install: _ForgeInstallProfileInstall
    versionInfo: ClientJson

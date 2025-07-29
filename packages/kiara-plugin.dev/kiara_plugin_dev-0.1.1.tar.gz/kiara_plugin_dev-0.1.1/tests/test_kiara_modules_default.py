#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kiara_plugin.dev` package."""

import pytest  # noqa

import kiara_plugin.dev


def test_assert():
    assert kiara_plugin.dev.get_version() is not None

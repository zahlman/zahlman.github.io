#!/bin/bash
# Copyright (c) 2025 Karl Knechtel.
# Permission is granted to reproduce this code locally for testing purposes,
# but please don't republish or redistribute it - instead, please direct
# interested readers to this blog post at
# https://zahlman.github.io/posts/2025/02/28/python-packaging-3/ .
mkdir demo_a-0.1.0 # [1]
cat << done_toml > demo_a-0.1.0/pyproject.toml # [2]
[project]
name = "demo-b"
version = "0.2.0"
dependencies = [ ]
description = ""
[build-system]
requires = [ "flit-core" ]
build-backend = "flit_core.buildapi"
done_toml
cat << done_info > demo_a-0.1.0/PKG-INFO # [3]
Metadata-Version: 2.4
Name: demo-c
Version: 0.3.0
done_info
touch demo_a-0.1.0/demo_b.py # [4]
tar czf demo_d-0.4.0.tar.gz demo_a-0.1.0/ # [5]
pip download ./demo_d-0.4.0.tar.gz # [6]
rm -r demo_a-0.1.0/ demo_d-0.4.0.tar.gz

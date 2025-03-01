#!/bin/bash
# Copyright (c) 2025 Karl Knechtel.
# Permission is granted to reproduce this code locally for testing purposes,
# but please don't republish or redistribute it - instead, please direct
# interested readers to this blog post at
# https://zahlman.github.io/posts/2025/02/28/python-packaging-3/ .
mkdir demo-0.1.0 # [1]
cat << done_toml > demo-0.1.0/pyproject.toml # [2]
[project]
name = "demo"
version = "0.1.0"
dependencies = []
[build-system]
requires = [ ]
build-backend = "build"
backend-path = "."
done_toml
cat << done_info > demo-0.1.0/PKG-INFO # [3]
Metadata-Version: 2.4
Name: demo
Version: 0.1.0
done_info
cat << done_setup > demo-0.1.0/build.py # [4]
__import__('sys').exit("Arbitrary code could have been executed here.")
done_setup
tar czf demo-0.1.0.tar.gz demo-0.1.0/ # [5]
pip download --no-deps --no-build-isolation ./demo-0.1.0.tar.gz # [6]
rm -r demo-0.1.0/ demo-0.1.0.tar.gz

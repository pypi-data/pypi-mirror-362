#!/usr/bin/env bash

version=$1

git tag -f -a v$version -m "release $version"
git push --tags

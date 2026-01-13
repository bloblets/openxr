#!/bin/sh

# Symlink distrobox shims
./distrobox-shims.sh

# Update the container and install packages
dnf update -y
grep -v '^#' ./fedora-example.packages | xargs dnf install -y
dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-(rpm -E %fedora).noarch.rpm
dnf swap -y ffmpeg-free ffmpeg --allowerasing

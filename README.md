# Envision OCI

This repository provides an OCI container image for building and running **Envision** in a consistent, reproducible environment. The image is based on Fedora and is designed to be used with **Podman** and **Distrobox**.

## Usage

Pull the container image:


podman pull ghcr.io/bloblets/fedora-envision:latest

Create a Distrobox environment:

distrobox create -i ghcr.io/bloblets/fedora-envision:latest -n envision

Enter the environment:

distrobox enter envision

Install Envision:

sudo install-envision

Requirements

    Podman

    Distrobox

All required dependencies for building and running Envision are included in the container.

from enum import StrEnum


class BaseImage(StrEnum):
    python_3_10 = "python:3.10.17-slim"
    python_3_11 = "python:3.11.12-slim"
    python_3_12 = "python:3.12.10-slim"

    node_lts = "node:lts-alpine"

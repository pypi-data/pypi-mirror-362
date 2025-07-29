# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
Formatted as described on [https://keepachangelog.com](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## [0.2.0] (2025-01-08)

## Changed

- dropped juliacall in favor of [Remote BMI](https://github.com/eWaterCycle/remotebmi), an OpenAPI based alternative for grpc4bmi ([#12](https://github.com/eWaterCycle/ewatercycle-wflowjl/pull/12)).
  - this means that the model now runs inside a container, isolating it from your Python environment.

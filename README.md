# xiaomi_mijia_ptx
Support for Xiaomi Miio PTX Touch Switch

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/volshebniks/xiaomi_mijia_ptx)](https://github.com/volshebniks/xiaomi_mijia_ptx/releases)
![GitHub Release Date](https://img.shields.io/github/release-date/volshebniks/xiaomi_mijia_ptx)
[![GitHub](https://img.shields.io/github/license/volshebniks/xiaomi_mijia_ptx)](LICENSE)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/volshebniks/xiaomi_mijia_ptx/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/volshebniks/xiaomi_mijia_ptx)](https://github.com/volshebniks/xiaomi_mijia_ptx/issues)

[![Donate](https://img.shields.io/badge/donate-Coffee-yellow.svg)](https://https://www.buymeacoffee.com/RlnBV9r)
[![Donate](https://img.shields.io/badge/donate-Yandex-red.svg)](https://money.yandex.ru/to/41001566881198)


The 'xiaomi_mijia_ptx' component is a Home Assistant custom switch for Support for Xiaomi Miio PTX Touch Switch.

## Table of Contents

* [Installation](#installation)
  * [Manual Installation](#manual-installation)
  * [Installation via HACS](#installation-via-hacs)
* [Configuration](#configuration)
  * [Configuration Parameters](#configuration-parameters)
* [State and Attributes](#state-and-attributes)
  * [State](#state)
  * [Attributes](#attributes)
  * [Notes about unit of measurement](#notes-about-unit-of-measurement)

## Installation

### MANUAL INSTALLATION

1. Download the `xiaomi_mijia_ptx.zip` file from the
   [latest release](https://github.com/volshebniks/xiaomi_mijia_ptx/releases/latest).
2. Unpack the release and copy the `custom_components/xiaomi_mijia_ptx/` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Configure the `xiaomi_mijia_ptx` switch.
4. Restart Home Assistant.

### INSTALLATION VIA HACS

1. Ensure that [HACS](https://custom-components.github.io/hacs/) is installed.
2. Add https://github.com/volshebniks/xiaomi_mijia_ptx ti custom repositiries
3. Configure the `xiaomi_mijia_ptx` switch.
4. Restart Home Assistant.

## Configuration

xiaomi_mijia_ptx  can be configured  in configuration.yaml


### configuration.yaml

Add `xiaomi_mijia_ptx` switch in your `configuration.yaml`.

```yaml
# Example configuration.yaml entry

switch:
  - platform: xiaomi_mijia_ptx
    host: YOUR_DEVICE_IP_ADRESS
    token: YOUR_DEVICE_TOKEN
    model: 090615.switch.switch01
    name:  xiaomi_smart_switch
```

### CONFIGURATION PARAMETERS

|Attribute |Optional|Description
|:----------|----------|------------
| `host` | No | Your switch ip address
|`token` | No | Your switch secret token
| `model` | No | May be '090615.switch.switch01' or '090615.switch.switch02' or '090615.switch.switch03' or '090615.switch.xswitch01' or '090615.switch.xswitch02' or '090615.switch.xswitch03'
| `name` | No | Name switch


Tested with 1 key and 3 keys switch

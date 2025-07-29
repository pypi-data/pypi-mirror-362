# eGauge open source Python code

This repository is a collection of Python packages that have been
released by eGauge Systems LLC as open source (MIT license).  These
are released in the hope that they may be useful for other developers.
Please see LICENSE for details.  eGauge Systems LLC reserves the
rights to add, modify, or remove code from this repository or the
entire repository without notice.

## egauge.pyside.terminal Support

To use module `egauge.pyside.terminal`, be sure to install the package
with the `pyside` extra dependencies:

```sh
pip install egauge-python[pyside]
```

## Example Programs

Example programs can be found in the `egauge.examples` module.  If you
want to run these programs, ensure that all dependencies are installed
by running the command:

```sh
pip install egauge-python[examples]
```

The following examples are available:

 * `test_capture`: Illustrates the use of the
   `egauge.webapi.device.Capture` class to capture waveform data.

 * `test_ctid_decoder`: Illustrates how the `egauge.ctid.Decoder` can be
   used to decode CTid information from a waveform.

 * `test_ctid`: Illustrates how the `egauge.webapi.device.CTidInfo`
    class can be used to control a meter to scan CTid information from
    a sensor, make the sensor blink the indicator LED, and so on.

 * `test_local`: Illustrates how the `egauge.webapi.device.Local`
   class can be used to fetch and display the locally acquired
   measurements of a meter.

 * `test_register`: Illustrates how the `egauge.webapi.device.Register`
   class can be used to fetch and display the register data of a
   meter.

Before running these programs, set the following environment variables
for your preferred test device:

 * `EGDEV`: URL of the test device (e.g., "http://eGaugeXXXXX.local" or
   "http://eGaugeXXXX.d.egauge.net")
 * `EGUSR`: Username to authenticate with (e.g., "owner")
 * `EGPWD`: Password to authenticate with (e.g., "super-secret-pw")

For example, the test program that illustrates the use of the register
data interface can be run with the command:

```
    python -m egauge.examples.test_register
```

## Overview of available modules

### egauge.webapi

The classes in this module provide access to eGauge web services.  The
APIs may be available on eGauge devices and/or as cloud-based web
services.

### egauge.webapi.device

The classes in this module provide access to APIs implemented on
eGauge devices.

### egauge.webapi.cloud

The classes in this module provide access to APIs implemented by
eGauge cloud services.

### egauge.ctid

The classes in this module support manufacturing CTid® sensors.  CTid®
is patented technology and shall be used in accordance with the
licensing agreements governing its use.

### egauge.pyside

The classes in this module support QT6-based graphical
user-interfaces.

## Source Code Conventions

Source code should be formatted with `ruff format` using a maximum
line-length of 79 characters.  The formatter can be installed with
`pip install ruff`.

Source code should be validated with `ruff check` and `pyright`.  The
latter can be installed with `pip install pyright`.

To do these things automatically before committing a change, install
the pre-commit hooks with:

```sh
    pip install pre-commit
    pre-commit install
```

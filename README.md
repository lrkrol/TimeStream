# TimeStream
[Lab Streaming Layer](https://github.com/sccn/labstreaminglayer) app that simply broadcasts a n LSL stream of time stamps, in two channels:

* Channel 1: Time in seconds taken from Python's `time.time()`.
* Channel 2: Calculated time in seconds between the current and previous submitted sample.

Useful when an external application cannot be synchronised with LSL, but logs data in its own format using the same system's time stamp.


## Usage:
Make sure to have pylsl installed; execute `pip install pylsl` or see the [liblsl-Python GitHub page](https://github.com/labstreaminglayer/liblsl-Python).

Run `TimeStream.py` and enter the requested sampling rate and chunk size. Alternatively, run `TimeStream.py` with additional arguments `--rate` and/or `--chunksize` to skip manual input, e.g.

`python .\TimeStream.py --rate 100`

starts a stream at 100 Hz, using default chunk size 32.
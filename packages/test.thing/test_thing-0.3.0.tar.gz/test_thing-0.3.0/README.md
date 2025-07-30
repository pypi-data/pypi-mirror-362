# test.thing

WIP.

## Goals.

 - one-file copypastelib
 - easy to hook up to pytest
 - future-oriented, built on systemd features in the guest (credentials, ssh-over-vsock, etc)
   - might limit usefulness for testing older OSes but we can add
     [workarounds](workarounds/) as required
 - works without networking configured in guest
 - supporting the existing features of [cockpit-bots](https://github.com/cockpit-project/bots)

## Try it

You can `pip install test.thing` which will put an executable called `tt` in
your path. This is sort of like the existing cockpit-bots `vm-run`.

You can also take a look at [`test/test_example.py`](test/test_example.py) and
run `TEST_IMAGE=/path/to/image.qcow2 pytest`.  This was originally tested with
the [examples images from
composefs-rs](https://github.com/containers/composefs-rs/tree/main/examples).

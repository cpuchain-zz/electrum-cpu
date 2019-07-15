# Kivy GUI

The Kivy GUI is used with Electrum on Android devices.
To generate an APK file, follow these instructions.

## Android binary with Docker

✗ _This script does not produce reproducible output (yet!).
   Please help us remedy this._

This assumes an Ubuntu (x86_64) host, but it should not be too hard to adapt to another
similar system. The docker commands should be executed in the project's root
folder.

0. Install Python 3.7 (required)

    ```
    $ sudo add-apt-repository -y ppa:deadsnakes/ppa
    $ sudo apt-get update
    $ sudo apt-get install -y build-essential libpython3.7 libpython3.7-dev libpython3.7-minimal libpython3.7-stdlib python3.7 python3.7-dev python3.7-distutils python3.7-lib2to3 python3.7-minimal python3.7-venv python3.7-doc binfmt-support cmake gettext
    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python3.7 get-pip.py && rm get-pip.py
    ```

1. Install Docker

    ```
    $ curl -fsSL https://get.docker.com/ | sudo sh
    $ sudo usermod -aG docker $USER
    $ sudo curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ sudo chmod +x /usr/local/bin/docker-compose
    ```

2. Build image

    ```
    $ sudo docker build -t electrum-android-builder-img electrum/gui/kivy/tools
    ```

3. Build locale files

    ```
    $ python3.7 ./contrib/pull_locale
    ```

4. Prepare pure python dependencies

    ```
    $ ./contrib/make_packages
    ```

5. Build binaries

    ```
    $ sudo docker run -it --rm \
        --name electrum-android-builder-cont \
        -v $PWD:/home/user/wspace/electrum \
        -v ~/.keystore:/home/user/.keystore \
        --workdir /home/user/wspace/electrum \
        electrum-android-builder-img \
        ./contrib/make_apk
    ```
    This mounts the project dir inside the container,
    and so the modifications will affect it, e.g. `.buildozer` folder
    will be created.

5. The generated binary is in `./bin`.



## FAQ

### I changed something but I don't see any differences on the phone. What did I do wrong?
You probably need to clear the cache: `rm -rf .buildozer/android/platform/build/{build,dists}`


### How do I deploy on connected phone for quick testing?
Assuming `adb` is installed:
```
$ adb -d install -r bin/Electrum-*-debug.apk
$ adb shell monkey -p org.electrum.electrum 1
```


### How do I get an interactive shell inside docker?
```
$ sudo docker run -it --rm \
    -v $PWD:/home/user/wspace/electrum \
    --workdir /home/user/wspace/electrum \
    electrum-android-builder-img
```


### How do I get more verbose logs for the build?
See `log_level` in `buildozer.spec`


### How can I see logs at runtime?
This should work OK for most scenarios:
```
adb logcat | grep python
```
Better `grep` but fragile because of `cut`:
```
adb logcat | grep -F "`adb shell ps | grep org.electrum.electrum | cut -c14-19`"
```


### Kivy can be run directly on Linux Desktop. How?
Install Kivy.

Build atlas: `(cd electrum/gui/kivy/; make theming)`

Run electrum with the `-g` switch: `electrum -g kivy`

### debug vs release build
If you just follow the instructions above, you will build the apk
in debug mode. The most notable difference is that the apk will be
signed using a debug keystore. If you are planning to upload
what you build to e.g. the Play Store, you should create your own
keystore, back it up safely, and run `./contrib/make_apk release`.

See e.g. [kivy wiki](https://github.com/kivy/kivy/wiki/Creating-a-Release-APK)
and [android dev docs](https://developer.android.com/studio/build/building-cmdline#sign_cmdline).

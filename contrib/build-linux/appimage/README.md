AppImage binary for Electrum
============================

✓ _This binary should be reproducible, meaning you should be able to generate
   binaries that match the official releases._

This assumes an Ubuntu host, but it should not be too hard to adapt to another
similar system. The host architecture should be x86_64 (amd64).
The docker commands should be executed in the project's root folder.

We currently only build a single AppImage, for x86_64 architecture.
Help to adapt these scripts to build for (some flavor of) ARM would be welcome,
see [issue #5159](https://github.com/spesmilo/electrum/issues/5159).


1. Install Docker

    ```
    $ curl -fsSL https://get.docker.com/ | sudo sh
    $ sudo usermod -aG docker $USER
    $ sudo curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    $ sudo chmod +x /usr/local/bin/docker-compose
    ```

2. Build image

    ```
    $ sudo docker build -t electrum-appimage-builder-img contrib/build-linux/appimage
    ```

3. Build binary

    ```
    $ sudo docker run -it \
        --name electrum-appimage-builder-cont \
        -v $PWD:/opt/electrum-cpu \
        --rm \
        --workdir /opt/electrum-cpu/contrib/build-linux/appimage \
        electrum-appimage-builder-img \
        ./build.sh
    ```

4. The generated binary is in `./dist`.


## FAQ

### How can I see what is included in the AppImage?
Execute the binary as follows: `./electrum*.AppImage --appimage-extract`

# This project build a dockerfile to run [disccofan](https://github.com/sgazagnes/disccofan)
## Its last built was in July 15th, 2024.

# How to Build

- Inside dockerfile directory run
```
./0.build-docker-host.sh
```

# How to Run

- Disable ssh service on host machine;
    + On ubuntu and other Debian based systems probably you need to run
    ```
    sudo service ssh stop
    ```
- Inside [dockerfiles directory](./dockerfiles/) run:
```
./run-docker-host.sh
```
- **Inside the running container**, put the desired network interface in parameters `btl_tcp_if_include` and `oob_tcp_if_include` (You can use the script [init_container.sh](https://github.com/niltonlqjr/docker-disccofan/blob/main/scripts/init_container.sh), that is copied to `/home/mpi/`, during the docker build, to do this);
- Finally, you can use disccofan as you wish.


## Third-Party Media & Credits

The image used for testing purposes in this repository [dos_wp_bw.jpg](test_image/dos_wp_bw.png) is an official promotional artwork for the video game **Divinity: Original Sin 2** and is the sole intellectual property of **Larian Studios**. 

Its inclusion in this project is strictly for **academic, non-commercial, and educational purposes** (image processing evaluation). This usage complies with the [Larian Studios' Fan Content Policy](https://larian.com/fan-content-policy).

Please note that while the source code of this application is distributed under the project's open-source license, this license **does not extend** to any third-party copyrighted assets, which remain under their respective owners' copyright.

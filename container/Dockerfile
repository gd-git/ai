FROM debian
RUN apt-get update; apt-get upgrade; apt-get install -y  --no-install-recommends \
    ed vim less vim curl lynx podman fuse-overlayfs slirp4netns lsb-release uidmap libcap2-bin 

RUN apt-get install -y  --no-install-recommends xserver-xephyr xfce4 xfce4-terminal git

RUN apt-get install -y ssh sshfs

# podman in podman bug ! see https://samuel.forestier.app/blog/security/podman-rootless-in-podman-rootless-the-debian-way

RUN chmod 0755 /usr/bin/newuidmap /usr/bin/newgidmap && \
    setcap cap_setuid=ep /usr/bin/newuidmap && \
    setcap cap_setgid=ep /usr/bin/newgidmap 

RUN adduser user && \
	echo "user:1001:64535" > /etc/subuid && \
    echo "user:1001:64535" > /etc/subgid && \
    echo 'user:user' | chpasswd && \
    echo 'root:root' | chpasswd

USER user


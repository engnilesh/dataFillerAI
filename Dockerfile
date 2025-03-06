FROM python:3.10.12

USER root

RUN set -ex; \
    apt-get update; \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN chmod +r requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

# Set up a non-root user
ARG USERNAME=datafiller
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN mkdir -p /home/$USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME

# Switch to non-root user
USER $USERNAME

# Set workdir and create application and data directories
RUN mkdir -p /home/$USERNAME/app \
    && mkdir -p /home/$USERNAME/data
WORKDIR /home/$USERNAME/app

ENTRYPOINT ["tail", "-f", "/dev/null"]
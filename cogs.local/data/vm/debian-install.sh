#/bin/sh

# Post-installation script for Debian6 VM.

# Add the public key to /root/.ssh/authorized_keys.
mkdir /root/.ssh
chmod go-rwx /root/.ssh
cp identity.pub /root/.ssh/authorized_keys


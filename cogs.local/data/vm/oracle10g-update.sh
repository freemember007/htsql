#/bin/sh

# Post-installation script for the oracle10g VM.
set -ex

## Update the hostname.
#echo oracle10g-vm >/etc/hostname

# Enable HTTPS for APT repositories.
apt-get -q update
apt-get -qy install apt-transport-https

# Register the Oracle repository.
echo "deb https://oss.oracle.com/debian/ unstable main non-free" >/etc/apt/sources.list.d/oracle.list
wget -q https://oss.oracle.com/el4/RPM-GPG-KEY-oracle -O- | apt-key add -
apt-get -q update

# Install the Oracle 10g Express Edition.
apt-get -qy --force-yes install oracle-xe-universal

# Clean APT cache.
apt-get clean

# Fix the problem when the configuration script eats the last
# character of the password if it is 'n': replace IFS="\n" with IFS=$'\n'.
sed -i -e s/IFS=\"\\\\n\"/IFS=\$\'\\\\n\'/ /etc/init.d/oracle-xe

# Configure the server; provide the answers for the following questions:
# The HTTP port for Oracle Application Express: 8080
# A port for the database listener: 1521
# The password for the SYS and SYSTEM database accounts: admin
# Start the server on boot: yes
/etc/init.d/oracle-xe configure <<END
8080
1521
admin
admin
y
END

# Load Oracle environment variables so that we could run `sqlplus`.
. /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin/oracle_env.sh

# Increase the number of connections.
echo "ALTER SYSTEM SET PROCESSES=200 SCOPE=SPFILE;" | \
sqlplus -S -L sys/admin AS SYSDBA

# Set Oracle environment variables on login.
cat <<END >>/root/.bashrc

. /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/bin/oracle_env.sh
END


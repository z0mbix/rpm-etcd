rpm-etcd
========

An RPM spec file to build and install etcd.

**Requirements:**

This requires the **rpmdevtools** package

**Create the RPM:**

Check the release version you want to package from the etcd github release page: [https://github.com/coreos/etcd/releases](https://github.com/coreos/etcd/releases)

Then run the build script to download and create the RPM:

    $ export ETCD_VERSION=0.4.6 ETCD_RELEASE=1 ./build-rpm.sh

This should create **~/rpmbuild/RPMS/x86_64/etcd-0.4.6-1.x86_64.rpm**

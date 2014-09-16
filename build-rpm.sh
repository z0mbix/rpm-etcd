#!/usr/bin/env bash
#
# EPEL repo required for golang package
#

usage () {
  echo
  echo 'Example usage:'
  echo
  echo 'ETCD_VERSION=0.4.6 ETCD_RELEASE=1 ./build-rpm.sh'
  echo
  echo 'This should create ~/rpmbuild/RPMS/x86_64/etcd-0.4.6-1.x86_64.rpm'
}

if [[ $(id -u) == 0 ]]; then
  echo "Don't create RPMs as root"
  exit 1
fi

if [[ -z $ETCD_VERSION ]] || [[ -z $ETCD_RELEASE ]]; then
  echo 'You must specify the etcd version to download and package with ETCD_VERSION=x.x.x'
  echo 'and the RPM release with ETCD_RELEASE=n'
  usage
  exit 1
fi

rpm -qv rpmdevtools || yum install -y rpmdevtools

rpmdev-setuptree || exit 1

if [[ ! -f ~/rpmbuild/SOURCES/etcd-v${ETCD_VERSION}-linux-amd64.tar.gz ]]; then
  wget https://github.com/coreos/etcd/releases/download/v${ETCD_VERSION}/etcd-v${ETCD_VERSION}-linux-amd64.tar.gz \
    -O ~/rpmbuild/SOURCES/etcd-v${ETCD_VERSION}-linux-amd64.tar.gz
fi

cp etcd.spec ~/rpmbuild/SPECS/etcd.spec
cp etcd.initd ~/rpmbuild/SOURCES/etcd.initd
cp etcd.sysconfig ~/rpmbuild/SOURCES/etcd.sysconfig
cp etcd.nofiles.conf ~/rpmbuild/SOURCES/etcd.nofiles.conf
cp etcd.logrotate ~/rpmbuild/SOURCES/etcd.logrotate

rpmbuild -bb ~/rpmbuild/SPECS/etcd.spec

# Copyright 2013, Nathan Milford
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To Install:
# You will need go from http://repo.milford.io.
#
# sudo yum -y install rpmdevtools go && rpmdev-setuptree
# wget https://raw.github.com/nmilford/rpm-etcd/master/etcd.spec -O ~/rpmbuild/SPECS/etcd.spec
# wget https://github.com/coreos/etcd/releases/download/v0.3.0/etcd-v0.3.0-linux-amd64.tar.gz -O ~/rpmbuild/SOURCES/etcd-v0.3.0-linux-amd64.tar.gz
# wget https://raw.github.com/nmilford/rpm-etcd/master/etcd.initd -O ~/rpmbuild/SOURCES/etcd.initd
# wget https://raw.github.com/nmilford/rpm-etcd/master/etcd.sysconfig -O ~/rpmbuild/SOURCES/etcd.sysconfig
# wget https://raw.github.com/nmilford/rpm-etcd/master/etcd.nofiles.conf -O ~/rpmbuild/SOURCES/etcd.nofiles.conf
# wget https://raw.github.com/nmilford/rpm-etcd/master/etcd.logrotate -O ~/rpmbuild/SOURCES/etcd.logrotate
# rpmbuild -bb ~/rpmbuild/SPECS/etcd.spec

%define debug_package %{nil}
%define etcd_user  %{name}
%define etcd_group %{name}
%define etcd_data  %{_localstatedir}/lib/%{name}
%define etcd_version %(echo $ETCD_VERSION)
%define etcd_release %(echo $ETCD_RELEASE)

Name:      etcd
Version:   %{etcd_version}
Release:   %{etcd_release}
Summary:   A highly-available key value store for shared configuration and service discovery.
License:   Apache 2.0
URL:       https://github.com/coreos/etcd
Group:     System Environment/Daemons
Source0:   https://github.com/coreos/%{name}/releases/download/v%{version}/%{name}-v%{version}-linux-amd64.tar.gz
Source1:   %{name}.initd
Source2:   %{name}.sysconfig
Source3:   %{name}.nofiles.conf
Source4:   %{name}.logrotate
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Packager:  Nathan Milford <nathan@milford.io>
Requires(pre): shadow-utils
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Requires:      golang >= 1.1

%description
A highly-available key value store for shared configuration and service
discovery. etcd is inspired by zookeeper and doozer, with a focus on:

* Simple: curl'able user facing API (HTTP+JSON)
* Secure: optional SSL client cert authentication
* Fast: benchmarked 1000s of writes/s per instance
* Reliable: Properly distributed using Raft

Etcd is written in Go and uses the raft consensus algorithm to manage a
highly-available replicated log.

%prep
%setup -n %{name}-v%{version}-linux-amd64

%build
rm -rf %{buildroot}

echo  %{buildroot}

%install
install -d -m 755 %{buildroot}/%{_sbindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/etcd    %{buildroot}/%{_sbindir}
install    -m 755 %{_builddir}/%{name}-v%{version}-linux-amd64/etcdctl %{buildroot}/%{_sbindir}

install -d -m 755 %{buildroot}/usr/share/doc/%{name}-v%{version}
install    -m 644 %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcd.md    %{buildroot}/%{_defaultdocdir}/%{name}-v%{version}
install    -m 644 %{_builddir}/%{name}-v%{version}-linux-amd64/README-etcdctl.md %{buildroot}/%{_defaultdocdir}/%{name}-v%{version}

install -d -m 755 %{buildroot}/%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}/%{_localstatedir}/lib/%{name}

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{name}.initd        %{buildroot}/%{_initrddir}/%{name}

install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/%{name}.sysconfig    %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate    %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

install -d -m 755 %{buildroot}/%{_sysconfdir}/security/limits.d/
install    -m 644 %_sourcedir/%{name}.nofiles.conf %{buildroot}/%{_sysconfdir}/security/limits.d/%{name}.nofiles.conf

%clean
rm -rf %{buildroot}

%pre
getent group %{etcd_group} >/dev/null || groupadd -r %{etcd_group}
getent passwd %{etcd_user} >/dev/null || /usr/sbin/useradd --comment "etcd Daemon User" --shell /bin/bash -M -r -g %{etcd_group} --home %{etcd_data} %{etcd_user}

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%files
%defattr(-,root,root)
%{_sbindir}/etc*
%{_defaultdocdir}/%{name}-v%{version}/*.md
%attr(0755,%{etcd_user},%{etcd_group}) %dir %{_localstatedir}/log/%{name}
%attr(0755,%{etcd_user},%{etcd_group}) %dir %{_localstatedir}/lib/%{name}
%{_initrddir}/etcd
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/security/limits.d/etcd.nofiles.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Tue Sep 16 2014 David Wooldridge <zombie@zombix.org> 0.4.6
* Mon Feb 10 2014 Nathan Milford <nathan@milford.io> 0.3.0
* Sat Dec 28 2013 Nathan Milford <nathan@milford.io> 0.2.0
* Thu Dec 05 2013 Nathan Milford <nathan@milford.io> 0.2.0-rc1
* Mon Aug 12 2013 Nathan Milford <nathan@milford.io> 0.1.0-1
- Initial spec.

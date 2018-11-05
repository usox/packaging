%define debug_package %{nil}
%define hhvm_home %{_sysconfdir}/hhvm
%define hhvm_user hhvm
%define hhvm_group hhvm
%define release 1
%define version #VERSION#
%define _rpmdir /var/out

Summary: HHVM virtual machine, runtime, and JIT for the PHP language
Name: hhvm
Version: %{version}
Release: %{release}
BuildArch: x86_64
Group: Applications/Internet
URL: http://www.hhvm.com/
Vendor: Facebook.
Packager: Daniel Jakob <dev@usox.org>

Source0: %{name}-%{version}.tar.gz

License: GPL

%if 0%{?fedora} >= 18
BuildRequires: libsq3-devel
%endif

Requires: glog

BuildRequires: libzip-devel
BuildRequires: double-conversion-devel
BuildRequires: lz4-devel
BuildRequires: libc-client-devel
BuildRequires: jemalloc-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: make
BuildRequires: cmake3
BuildRequires: libtool
BuildRequires: cpp
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: binutils-devel
BuildRequires: bzip2-devel
BuildRequires: curl-devel
BuildRequires: expat-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: gd-devel
BuildRequires: glog-devel
BuildRequires: ImageMagick-devel
BuildRequires: libcap-devel
BuildRequires: libcurl-devel
BuildRequires: libdwarf-devel
BuildRequires: libedit-devel
BuildRequires: libevent-devel
BuildRequires: libicu-devel
BuildRequires: libmcrypt-devel
BuildRequires: libmemcached-devel
BuildRequires: libsodium-devel
BuildRequires: libxslt-devel
BuildRequires: libxml2-devel
BuildRequires: libyaml-devel
BuildRequires: mysql-devel
BuildRequires: pam-devel
BuildRequires: pcre-devel
BuildRequires: ocaml
BuildRequires: oniguruma-devel
BuildRequires: openldap-devel
BuildRequires: readline-devel
BuildRequires: tbb-devel
BuildRequires: zlib-devel
BuildRequires: glibc-devel
BuildRequires: libnotify-devel
BuildRequires: unixODBC-devel
BuildRequires: libvpx-devel
BuildRequires: openssl-devel
BuildRequires: fribidi-devel
BuildRequires: gmp-devel
BuildRequires: fastlz-devel
BuildRequires: gperf
BuildRequires: libatomic
BuildRequires: postgresql95-devel
BuildRequires: sqlite-devel
BuildRequires: numactl-devel

Provides: hhvm

%description
HHVM is an open-source virtual machine designed for executing programs written in Hack and PHP. HHVM uses a just-in-time (JIT) compilation approach to achieve superior performance while maintaining the development flexibility that PHP provides.

%prep
%autosetup -n %{name}-%{version}

%build
%{__rm} -rf %{buildroot}
export CMAKE_PREFIX_PATH=%{buildroot}%{_prefix}
cmake3 . \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DMYSQL_UNIX_SOCK_ADDR=/var/lib/mysql/mysql.sock \
  -DPGSQL_INCLUDE_DIR=/usr/pgsql-9.5/include/ \
  -DPGSQL_LIBRARY=/usr/pgsql-9.5/lib/libpq.so \
  -DENABLE_EXTENSION_PGSQL=On
make -j$(($(nproc --all)+1))

%install
%{__make} install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}%{_localstatedir}/log/hhvm
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/hhvm
%{__mkdir} -p %{buildroot}%{_sysconfdir}/hhvm
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__mkdir} -p %{buildroot}/usr/share/hhvm/hdf
%{__mkdir} -p %{buildroot}/etc/tmpfiles.d
%{__mkdir} -p %{buildroot}/var/lib/hhvm/sessions
%{__mkdir} -p %{buildroot}/var/cache/hhvm
%{__install} -m 644 -p /home/rpmbuilder/rpmbuild/SOURCES/dist/php.ini %{buildroot}%{_sysconfdir}/hhvm/php.ini
%{__install} -m 644 -p /home/rpmbuilder/rpmbuild/SOURCES/dist/hhvm.service %{buildroot}%{_unitdir}/hhvm.service
%{__install} -m 644 -p /home/rpmbuilder/rpmbuild/SOURCES/dist/static.mime-types.hdf %{buildroot}%{_datadir}/hhvm/hdf/static.mime-types.hdf
%{__install} -m 644 -p /home/rpmbuilder/rpmbuild/SOURCES/dist/hhvm.conf %{buildroot}/etc/tmpfiles.d/hhvm.conf
%{__install} -m 644 -p /home/rpmbuilder/rpmbuild/SOURCES/dist/hhvm-proxygen.service %{buildroot}%{_unitdir}/hhvm-proxygen.service


%{__rm} -rf %{buildroot}/usr/lib/libzip.a
%{__rm} -rf %{buildroot}/usr/lib/libzip.so
%{__rm} -rf %{buildroot}/usr/include
%{__rm} -rf %{buildroot}/usr/lib64
%{__rm} -rf %{buildroot}/usr/share/doc/
%{__rm} -rf %{buildroot}/usr/lib/libpcre.a
%{__rm} -rf %{buildroot}/usr/lib/libpcreposix.a
%{__rm} -rf %{buildroot}/usr/lib/libpcrecpp.a
%{__rm} -rf %{buildroot}/usr/bin/pcregrep
%{__rm} -rf %{buildroot}/usr/bin/pcretest
%{__rm} -rf %{buildroot}/usr/bin/pcrecpp_unittest
%{__rm} -rf %{buildroot}/usr/bin/pcre_scanner_unittest
%{__rm} -rf %{buildroot}/usr/bin/pcre_stringpiece_unittest

%files
%defattr(-,root,root,-)
/usr/bin/hhvm
/usr/bin/hh_server
/usr/bin/hh_client
/usr/bin/hh_parse
/usr/bin/hphpize
/usr/bin/hhvm-repo-mode
/usr/bin/hhvm-gdb
/usr/bin/hackfmt
/usr/bin/hh_single_compile
%dir /etc/hhvm
%dir /etc/tmpfiles.d
%config(noreplace) /etc/hhvm/php.ini
%config(noreplace) /etc/tmpfiles.d/hhvm.conf
%{_unitdir}/hhvm.service
%{_unitdir}/hhvm-proxygen.service
%dir /usr/share/hhvm
%dir /usr/share/hhvm/hdf
%config /usr/share/hhvm/hdf/static.mime-types.hdf
%attr(755, hhvm, hhvm) /var/cache/hhvm
%attr(755, hhvm, hhvm) /var/log/hhvm
%attr(775, hhvm, hhvm) /var/run/hhvm
%attr(775, hhvm, hhvm) /var/lib/hhvm
%attr(775, hhvm, hhvm) /var/lib/hhvm/sessions


%clean
%{__rm} -rf %{buildroot}


%pre
getent group %{hhvm_group} >/dev/null || groupadd -r %{hhvm_group}
getent passwd %{hhvm_user} >/dev/null || \
    useradd -r -g %{hhvm_group} -s /sbin/nologin \
    -d %{hhvm_home} -c "hhvm user"  %{hhvm_user}
exit 0

%post
# Register the HHVM service
/usr/bin/systemctl preset hhvm.service >/dev/null 2>&1 ||:
/usr/bin/systemctl preset hhvm-proxygen.service >/dev/null 2>&1 ||:

# print site info
    cat <<BANNER
----------------------------------------------------------------------

Thank you for using hhvm!

Please find the official documentation for HHVM here:
* http://www.hhvm.com/

----------------------------------------------------------------------
BANNER

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:

%changelog

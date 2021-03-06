#
# $Id: sfcb.spec.in,v 1.16 2007/03/16 13:54:44 mihajlov Exp $
#
# Package spec for sblim-sfcb
#

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}

Summary: Small Footprint CIM Broker
Name: sblim-sfcb
Version: 1.3.2
Release: 0
Group: Systems Management/Base
License: EPL
URL: http://www.sblim.org
Source0: ftp://dl.sourceforge.net/pub/s/sb/sblim/%{name}-%{version}.tar.bz2
Provides: cimserver
BuildRequires: curl-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
Requires: curl
Requires: zlib
Requires: openssl
Requires: pam

%Description
Small Footprint CIM Broker (sfcb) is a CIM server conforming to the
CIM Operations over HTTP protocol.
It is robust, with low resource consumption and therefore specifically 
suited for embedded and resource constrained environments.
sfcb supports providers written against the Common Manageability
Programming Interface (CMPI).

%Package schema
Summary: CIM Schema Files
License: Distributed Management Task Force
Group: Systems Management/Base
Requires: %{name}
URL: http://www.dmtf.org

%Description schema
Distributed Management Task Force (DMTF) Common Information Model (CIM)
Schema files that can be used with the Small Footprint CIM Broker.

%prep

%setup -T -b 0 -n %{name}-%{version}

export PATCH_GET=0
#%patch0 -p1

%build

%configure --enable-debug --enable-ssl --enable-pam --enable-ipv6
make

%install

if [ `id -ur` != 0 ]
then
# paranoia check 
	rm -rf $RPM_BUILD_ROOT 
fi

make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install-cimschema

# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a

echo "%defattr(-,root,root)" > _pkg_list

find $RPM_BUILD_ROOT/%{_datadir}/sfcb -type f | grep -v $RPM_BUILD_ROOT/%{_datadir}/sfcb/CIM >> _pkg_list
sed s?$RPM_BUILD_ROOT??g _pkg_list > _pkg_list_2
mv -f _pkg_list_2 _pkg_list
echo "%config %{_sysconfdir}/sfcb/*" >> _pkg_list
echo "%config %{_sysconfdir}/pam.d/*" >> _pkg_list
echo "%doc %{_datadir}/doc/*" >> _pkg_list
echo "%doc %{_datadir}/man/man1/*" >> _pkg_list
echo "%{_sysconfdir}/init.d/sfcb" >> _pkg_list
echo "%{_localstatedir}/lib/sfcb" >> _pkg_list
echo "%{_bindir}/*" >> _pkg_list
echo "%{_sbindir}/*" >> _pkg_list
echo "%{_libdir}/*.so*" >> _pkg_list

echo =======================================
cat _pkg_list

%clean
if [ `id -ur` != 0 ]
then
# paranoia check 
	rm -rf $RPM_BUILD_ROOT 
fi

%post 
%{_datadir}/sfcb/genSslCert.sh %{_sysconfdir}/sfcb
/sbin/ldconfig
exit 0

%postun -p /sbin/ldconfig

%post schema
sfcbrepos -f 2> /dev/null
exit 0

%files schema
%defattr(-,root,root)
%{_datadir}/sfcb/CIM

%files -f _pkg_list

%changelog

* Fri Feb 09 2007  <mihajlov@dyn-9-152-143-45.boeblingen.de.ibm.com> - 1.2.1-0
- Updated for 1.2.1 content, enabled SSL, indications

* Wed Aug 31 2005  <mihajlov@dyn-9-152-143-45.boeblingen.de.ibm.com> - 0.9.0b-0
- Support for man pages added

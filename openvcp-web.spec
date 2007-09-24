Summary:	VServer Control Panel Web interface
Name:		openvcp-web
Version:	0.3
Release:	0.4
License:	GPL
Group:		Applications/WWW
Source0:	http://files.openvcp.org/%{name}-%{version}.tar.gz
# Source0-md5:	2d9733679fbb0b3a5f1b028d551043a1
Source1:	%{name}-apache.conf
Patch0:		%{name}-conf.patch
Patch1:		%{name}-actions.patch
URL:		http://www.openvcp.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	php-common >= 3:5.0.0
Requires:	php-gd
Requires:	php-gettext
Requires:	php-gnutls
Requires:	php-mysql
Requires:	php-sockets
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(auth)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
VServer Control Panel Web interface.

%prep
%setup -q -n %{name}-%{version}-rc2
%patch0 -p1
%patch1 -p1

# Replace short open tag <? with full <?php
find -type f -print0 | xargs -0 perl -pi -e 's/<\?($|\s)/<?php\1/g'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/cache/openvcp-web}

install core/openvcp.conf $RPM_BUILD_ROOT%{_sysconfdir}

# That way we won't miss any new files on package update
cp -a index.php core mods themes $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/core/{cache,.htaccess,mysql.sql,openvcp.conf}

ln -sf /var/cache/openvcp-web $RPM_BUILD_ROOT%{_appdir}/core/cache
ln -sf %{_sysconfdir}/openvcp.conf $RPM_BUILD_ROOT%{_appdir}/core/openvcp.conf

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc AUTHORS INSTALL README core/mysql.sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openvcp.conf
%{_appdir}
%dir %attr(770,http,http) /var/cache/openvcp-web

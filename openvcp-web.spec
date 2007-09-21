Summary:	VServer Control Panel Web interface
Name:		openvcp-web
Version:	0.3
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://files.openvcp.org/%{name}-%{version}.tar.gz
# Source0-md5:	2d9733679fbb0b3a5f1b028d551043a1
URL:		http://www.openvcp.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires(triggerpostun):	sed >= 4.0
# see SOURCES/webapps.README for description and complete listing
#Requires:	webserver(access)
#Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
#Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
#%define		_appdir		%{_datadir}/%{_webapp}

# in case _sysconfdir is not in webapps dir, run this replace pattern
# before copy-pasting to your spec: :%s#%{_sysconfdir}#%{_webapps}/%{_webapp}#g

%description
VServer Control Panel Web interface.

%prep
%setup -q

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
#install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

# %webapp_* macros usage extracted from /usr/lib/rpm/macros.build:
#
# Usage:
#   %%webapp_register HTTPD WEBAPP
#   %%webapp_unregister HTTPD WEBAPP

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
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
#%{_appdir}

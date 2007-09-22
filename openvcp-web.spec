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
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(auth)
Requires:	php >= 5.0
Requires:	php-gd
Requires:	php-mysql
Requires:	php-socket
Requires:	php-gettext
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

cat > httpd.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	RewriteEngine On
	RewriteRule ^openvcp(.*)$ index.php$1

	Order Deny,Allow
	Deny from all
	Allow from localhost
</Directory>

<Directory %{_appdir}/core>
	Order Deny,Allow
	Deny from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/cache/openvcp-web}

install core/openvcp.conf $RPM_BUILD_ROOT%{_sysconfdir}

# That way we won't miss any new files on package update
cp -a index.php core mods themes $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/core/{cache,.htaccess,mysql.sql,openvcp.conf}

ln -sf /var/cache/openvcp-web $RPM_BUILD_ROOT%{_appdir}/core/cache
ln -sf %{_sysconfdir}/openvcp.conf $RPM_BUILD_ROOT%{_appdir}/core/openvcp.conf

install httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

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
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%{_appdir}
%dir %attr(770,httpd,httpd) /var/cache/openvcp-web

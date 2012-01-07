# TODO
# - check_bpi checker package
# - this piece of shit is insecure, don't use it in enviroment you don't trust:
#     config_functions/fix_config.php allows you to write config file, which is
#     included to any page of nagios bpi
#     why it's even "featured" upload of nagios.org? ah yes,
#     exchange.nagios.org itself is similar shit.
# - it doesn't even check for errors for simple file operation:
#     file_put_contents(CONFIGFILE, $new);
#     print "<p>File successfully written!</p>";
Summary:	Nagios Business Process Intelligence Featured Popular
Name:		nagios-bpi
Version:	1.0
Release:	0.7
License:	GPL v2
Group:		Applications/WWW
Source0:	http://assets.nagios.com/downloads/exchange/nagiosbpi/nagiosbpi.zip
# Source0-md5:	a0b6d7ce21ee8903278a4d2f2f89f285
Patch0:		paths.patch
URL:		http://exchange.nagios.org/directory/Addons/Components/Nagios-Business-Process-Intelligence/details
BuildRequires:	unzip
Requires:	nagios-cgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		nagiosbpi
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		appdir		%{_datadir}/nagios/%{_webapp}

%description
Nagios Business Process Intelligence is an advanced grouping tool that
allows you to set more complex dependencies to determine groups
states. Nagios BPI provides an interface to effectively view the
'real' state of the network. Rules for group states can be determined
by the user, and parent-child relationships are easily identified when
you need to 'drill down' on a problem. This tool can also be used in
conjunction with a check plugin to allow for notifications through
Nagios.

%prep
%setup -q -n nagiosbpi
%patch0 -p1

echo '<?php
die();
// this file shouldnt even exist, it has no authorization and it writes config file!
require "config_functions/fix_config.php";
' > fix_config.php

rmdir tmp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{appdir}}
cp -a *.php *.js *.css constants.conf $RPM_BUILD_ROOT%{appdir}
cp -a config_functions functions images $RPM_BUILD_ROOT%{appdir}

# relocate
cp -a bpi.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL TODO
%dir %attr(770,root,http) %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bpi.conf
%{appdir}

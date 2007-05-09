Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Name:		python-paramiko
Version:	1.7
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://www.lag.net/paramiko/download/paramiko-%{version}.tar.gz
# Source0-md5:	68d7b2a3648669c0d2a2fa6b8905b7d5
URL:		http://www.lag.net/paramiko/
BuildRequires:	python-devel >= 2.2
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A module for python 2.2 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -l pl.UTF-8
Moduł dla języka Python 2.2 (lub wyższego) implementujący protokół
SSH2 dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych)
połączeń ze zdalnymi maszynami.

%prep
%setup  -q -n paramiko-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/*
%{py_sitescriptdir}/paramiko

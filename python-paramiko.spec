Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Name:		python-paramiko
Version:	1.7.1
Release:	2
License:	LGPL
Group:		Libraries/Python
Source0:	http://www.lag.net/paramiko/download/paramiko-%{version}.tar.gz
# Source0-md5:	de6405406897fad04fa5fdf56952ea75
URL:		http://www.lag.net/paramiko/
BuildRequires:	python-Crypto >= 1.9
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
Requires:	python-Crypto
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A module for python 2.3 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -l pl.UTF-8
Moduł dla języka Python 2.3 (lub wyższego) implementujący protokół
SSH2 dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych)
połączeń ze zdalnymi maszynami.

%prep
%setup  -q -n paramiko-%{version}

%build
%{__python} setup.py build
find demos -name '*.py' -type f -exec sed -i -e 's|#!.*python.*|#!%{_bindir}/python|g' "{}" ";"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean
install demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README docs/*
%{py_sitescriptdir}/paramiko
%dir %{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}/*

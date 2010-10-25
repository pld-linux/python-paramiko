#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

%define 	module	paramiko
Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Name:		python-%{module}
Version:	1.7.6
Release:	3
License:	LGPL
Group:		Libraries/Python
Source0:	http://www.lag.net/paramiko/download/%{module}-%{version}.tar.gz
# Source0-md5:	fa144ab46f1dc639b05ab948c30efac4
URL:		http://www.lag.net/paramiko/
BuildRequires:	python-Crypto >= 1.9
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%pyrequires_eq	python-modules
Requires:	python-Crypto
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A module for Python 2.3 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -l pl.UTF-8
Moduł dla języka Python 2.3 (lub wyższego) implementujący protokół
SSH2 dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych)
połączeń ze zdalnymi maszynami.

%package apidocs
Summary:	paramiko API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki paramiko
Group:		Documentation

%description apidocs
API and internal documentation for paramiko library.

%prep
%setup  -q -n %{module}-%{version}

find demos -name '*.py' -type f | xargs sed -i -e '1s|#!.*python.*|#!%{_bindir}/python|'

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*
%endif


#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	tests	# do not perform "make test"

%define 	module	paramiko
Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Name:		python-%{module}
Version:	1.9.0
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:        http://pypi.python.org/packages/source/p/paramiko/paramiko-%{version}.tar.gz
# Source0-md5:	b78472021ff6586dd61ad6972032f54f
URL:            https://github.com/paramiko/paramiko/
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

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

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

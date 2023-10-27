#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	paramiko
Summary:	SSH2 protocol for Python 2
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie 2
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.12.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/paramiko/
Source0:	https://github.com/paramiko/paramiko/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	9fed2b771bf8afa91b74a5536de3c670
Patch0:		paramiko-mock.patch
URL:		https://github.com/paramiko/paramiko/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyNaCl >= 1.0.1
BuildRequires:	python-bcrypt >= 3.1.3
BuildRequires:	python-cryptography >= 2.5
BuildRequires:	python-mock
BuildRequires:	python-pyasn1 >= 0.1.7
BuildRequires:	python-pytest >= 4.4.2
BuildRequires:	python-pytest-relaxed
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyNaCl >= 1.0.1
BuildRequires:	python3-bcrypt >= 3.1.3
BuildRequires:	python3-cryptography >= 2.5
BuildRequires:	python3-pyasn1 >= 0.1.7
BuildRequires:	python3-pytest >= 4.4.2
BuildRequires:	python3-pytest-relaxed
BuildRequires:	python3-six
%endif
%endif
%if %{with doc}
BuildRequires:	python3-alabaster >= 0.7.12
BuildRequires:	sphinx-pdg-3 >= 1.4
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A module for Python 2.6 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -l pl.UTF-8
Moduł dla języka Python 2.6 (lub wyższego) implementujący protokół
SSH2 dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych)
połączeń ze zdalnymi maszynami.

%package -n python3-%{module}
Summary:	SSH2 protocol for Python 3
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
A module for Python 3.2 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -n python3-%{module} -l pl.UTF-8
Moduł dla języka Python 3.2 (lub wyższego) implementujący protokół
SSH2 dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych)
połączeń ze zdalnymi maszynami.

%package apidocs
Summary:	API documentation for paramiko module
Summary(pl.UTF-8):	Dokumentacja API modułu paramiko
Group:		Documentation

%description apidocs
API documentation for paramiko module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu paramiko.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

# Windows-specific modules, break tests by using Windows-specific ctypes API
%{__rm} paramiko/{win_pageant,_winapi}.py

%build
%if %{with python2}
%py_build

%if %{with tests}
# note: slow tests are broken
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests -m 'not slow'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests -m 'not slow'
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html sites/docs sites/docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*.py

%py_postclean
%endif

%if %{with python3}
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc NEWS NOTES README.rst TODO sites/www/changelog.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc NEWS NOTES README.rst TODO sites/www/changelog.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc sites/docs/_build/html/{_static,api,*.html,*.js}
%endif

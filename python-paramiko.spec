#
# Conditional build:
%bcond_without	apidocs	# API docs packaging
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	paramiko
Summary:	SSH2 protocol for Python 2
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie 2
Name:		python-%{module}
Version:	1.17.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/paramiko/
Source0:	https://pypi.python.org/packages/b8/60/f83c7f27d15560c731fb7f39f308b5d056785a0cbb0b5c87ee3767b0db4c/paramiko-%{version}.tar.gz
# Source0-md5:	45df29f2c569ff7d780eff8948f401d6
URL:		https://github.com/paramiko/paramiko/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-Crypto >= 2.1
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-ecdsa >= 0.11
%endif
%if %{with python3}
BuildRequires:	python3-Crypto >= 2.1
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-ecdsa >= 0.11
%endif
Requires:	python-Crypto >= 2.1
Requires:	python-ecdsa >= 0.11
Requires:	python-modules >= 1:2.6
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
Requires:	python3-Crypto >= 2.1
Requires:	python3-ecdsa >= 0.11
Requires:	python3-modules >= 1:3.2

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

find demos -name '*.py' -type f | xargs sed -i -e '1s|#!.*python.*|#!%{_bindir}/python|'

# Windows-specific modules, break tests by using Windows-specific ctypes API
%{__rm} paramiko/{win_pageant,_winapi}.py

%build
%if %{with python2}
%py_build
%{?with_tests:LC_ALL=C.UTF-8 %{__python} test.py}
%endif

%if %{with python3}
%py3_build
%{?with_tests:LC_ALL=C.UTF-8 %{__python3} test.py}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/{_static,api,*.html,*.js}
%endif

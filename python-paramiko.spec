
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	tests	# do not perform "make test"
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module


%define 	module	paramiko
Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Name:		python-%{module}
Version:	1.15.1
Release:	3
License:	LGPL
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/p/paramiko/paramiko-%{version}.tar.gz
# Source0-md5:	48c274c3f9b1282932567b21f6acf3b5
URL:		https://github.com/paramiko/paramiko/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-Crypto >= 1.9
BuildRequires:	python-devel >= 2.3
BuildRequires:	python-ecdsa >=0.11
%endif
%if %{with python3}
BuildRequires:	python3-Crypto >= 1.9
BuildRequires:	python3-devel
BuildRequires:	python3-ecdsa >=0.11
%endif


Requires:	python-Crypto
Requires:	python-modules
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

%package -n python3-%{module}
Summary:	SSH2 protocol for Python
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
A module for Python 3 (or higher) that implements the SSH2 protocol
for secure (encrypted and authenticated) connections to remote
machines.

%description -n python3-%{module} -l pl.UTF-8
Moduł dla języka Python 3 (lub wyższego) implementujący protokół SSH2
dla uzyskania bezpiecznych (szyfrowanych i autoryzowanych) połączeń ze
zdalnymi maszynami.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API and internal documentation for paramiko library.

%prep
%setup  -q -n %{module}-%{version}

find demos -name '*.py' -type f | xargs sed -i -e '1s|#!.*python.*|#!%{_bindir}/python|'

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
%doc README
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif


%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*
%endif

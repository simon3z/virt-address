%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           virt-address
Version:        0.1.1
Release:        1%{?dist}
Summary:        Virtual machines ip address discovery tool

License:        GPLv2
URL:            https://github.com/simon3z/%{name}
Source0:        https://github.com/simon3z/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

Requires:       libvirt-python

%description
Virtual machines ip address discovery tool.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%files
%doc COPYING
%{_bindir}/virt-address
%{python_sitelib}/*


%changelog
* Sat Jan  3 2015 Federico Simoncelli <fsimonce@redhat.com> - 0.1.1
- initial build

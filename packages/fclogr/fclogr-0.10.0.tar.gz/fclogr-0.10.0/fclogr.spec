# This specfile is licensed under:
#
# Copyright (C) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT.html

Name:           fclogr
Version:        0.10.0
Release:        1%{?dist}
Summary:        A tool for managing RPM changelogs and updates

License:        GPL-2.0-or-later
URL:            https://sr.ht/~gotmax23/fclogr
%global furl    https://git.sr.ht/~gotmax23/fclogr
Source0:        %{furl}/refs/download/v%{version}/fclogr-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  gnupg2
BuildRequires:  python3-devel


%description
fclogr is a tool for managing RPM changelogs and updates.


%prep
%autosetup -p1 -n fclogr-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files fclogr


%check
%pytest


%files -f %{pyproject_files}
%license LICENSES/*.txt
%doc README.md
%doc NEWS.md
%{_bindir}/fclogr*


%changelog
* Wed Jul 16 2025 Maxwell G <maxwell@gtmx.me> - 0.10.0-1
- Release 0.10.0.

* Thu Sep 19 2024 Maxwell G <maxwell@gtmx.me> - 0.9.0-1
- Release 0.9.0.

* Sun Mar 3 2024 Maxwell G <maxwell@gtmx.me> - 0.8.0-1
- Release 0.8.0.

* Sat Mar 2 2024 Maxwell G <maxwell@gtmx.me> - 0.7.0-1
- Release 0.7.0.

* Thu Feb 29 2024 Maxwell G <maxwell@gtmx.me> - 0.6.0-1
- Release 0.6.0.

* Wed Jun 21 2023 Maxwell G <maxwell@gtmx.me> - 0.5.0-1
- Release 0.5.0.

* Tue Jun 20 2023 Maxwell G <maxwell@gtmx.me> - 0.4.0-1
- Release 0.4.0.

* Sat Apr 15 2023 Maxwell G <maxwell@gtmx.me> - 0.3.1-1
- Release 0.3.1.

* Sat Apr 15 2023 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Release 0.3.0.

* Sat Mar 18 2023 Maxwell G <maxwell@gtmx.me> - 0.2.0-1
- Initial package

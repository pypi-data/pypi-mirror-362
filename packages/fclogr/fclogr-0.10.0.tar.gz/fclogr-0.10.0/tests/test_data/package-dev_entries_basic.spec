# Copyright (c) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

Name:           package
Version:        1^2.20231016.COMMIT2
Release:        1%{?dist}
Summary:        Test package

License:        ...
URL:            ...


%description
%{summary}.

%prep
%autosetup -c -T


%files

%changelog
* Mon Oct 16 2023 Perry The Packager <example@example.com> - 1^2.20231016.COMMIT2-1
- another change

* Sun Oct 15 2023 Perry The Packager <example@example.com> - 1^1.20231015.COMMIT1-1
- a change

* Fri Mar 03 2023 Packager <example@example.com> - 1-1
- Initial package

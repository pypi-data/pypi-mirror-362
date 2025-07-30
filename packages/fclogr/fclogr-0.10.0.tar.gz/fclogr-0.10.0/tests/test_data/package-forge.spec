# Copyright (c) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

%global forgeurl https://github.com/ansible-community/antsibull
%define tag %{version}

Name:           package-forge
Version:        0.59.0
%forgemeta
Release:        1%{?dist}
Summary:        Test package with forge macros

License:        ...
URL:            ...
Source:         %{forgesource}


%description
%{summary}.

%prep
%forgesetup


%files

%changelog
* Thu Feb 01 2024 Perry the Packager <perry@example.com> - 0.59.0-1
- Initial package

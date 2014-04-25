# The MIT License (MIT)
# 
# Copyright (c) 2013 Tomasz Olszak <olszak.tomasz@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This file is based on qtxmlpatterns.spec from Mer project
# http://merproject.org

Name:       qt5-qtxmlpatterns
Summary:    Qt XML Patterns library
Version:    5.2.90+alpha
Release:    0
Group:      Base/Libraries
License:    LGPL-2.1 or GPL-3.0
URL:        http://qt.digia.com
Source0:    %{name}-%{version}.tar.bz2
Source1001: %{name}.manifest
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtxml-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtnetwork-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-qmake
BuildRequires:  fdupes

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the XMLPatterns library


%package devel
Summary:    Qt XML Patterns - development files
Group:      Base/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the XMLPatterns library development files


#### Build section

%prep
%setup -q -n %{name}-%{version}/qtxmlpatterns
cp %{SOURCE1001} .

# The original source assumes build happens within a monolithic tree.
# The tool used is syncqt, which complains a lot but really only wants
# to know where the mkspecs may be found. Hence the environment variable
# name is a little misleading.
#
# XXX: FOR THE LOVE OF ALL THAT MAY BE HOLY - DO NOT USE RPMBUILD AND
# ITS INTERNAL qmake MACRO. IT BREAKS THE BUILD!
%build
export QTDIR=/usr/share/qt5
touch .git
qmake -qt=5
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;

# We don't need qt5/Qt/
rm -rf %{buildroot}%{_includedir}/qt5/Qt

#
%fdupes %{buildroot}%{_includedir}




#### Pre/Post section

%post -p /sbin/ldconfig
%postun
/sbin/ldconfig




#### File section


%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libQt5XmlPatterns.so.*
%{_qt5_bindir}/*

%files devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/libQt5XmlPatterns.so
%{_libdir}/libQt5XmlPatterns.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5
%{_datadir}/qt5/mkspecs
%{_libdir}/cmake


#### No changelog section, separate $pkg.changes contains the history

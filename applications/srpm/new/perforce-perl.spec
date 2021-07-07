%define _p4perlversion 2056101

Summary: Perforce Perl bindings
Name: perforce-perl
Version: 2020.1
Release: 5%{?dist}
License: Proprietary
URL: https://ftp.perforce.com/perforce/r20.1/bin.tools/

Source: p4perl.tgz
Buildrequires: perforce-api
Buildrequires: perl-ExtUtils-MakeMaker
Buildrequires: perl-Data-Dumper
Buildrequires: gcc-c++
Requires: perl
Requires: openssl-static

%description
Perl bindings for perforce

%prep
%setup -c %{name}-%{version}

%build
cd p4perl-%{version}.%{_p4perlversion}
perl Makefile.PL --apidir /usr/local/p4api --ssl=/usr/local/ssl/lib
sed -i 's#/usr/local/lib#/usr/lib#g;s#/usr/local/share#/usr/share#g' Makefile
%{__make}

%install
cd p4perl-%{version}.%{_p4perlversion}
%{__make} install DESTDIR="%{buildroot}"
find %{buildroot} -name ".packlist" -delete -o -name "perllocal.pod" -delete

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%{_libdir}/perl5/*
%{_mandir}/man3/*

%changelog
* Thu Jul 01 2021 olivier.crozier@nagra.com - 2020.1-1
- Bump to 2020.1/2056101 built over 2020.1/2138914 API

* Fri Apr 08 2016 matthieu.castellazzi@nagra.com - 2014.1-5
- rebuild over 2015.2 P4API

* Fri Nov 06 2015 matthieu.castellazzi@nagra.com - 2014.1-4
- rebuild over 2014.1 API

* Thu Oct 08 2015 olivier.mauras@nagra.com - 2014.1-2
- Update %files path

* Wed Sep 30 2015 olivier.mauras@nagra.com - 2014.1
- Bump to 2014.1 built over 2015.1 API

* Tue Feb 05 2013 olivier.mauras@nagra.com - 2012.2
- Version bump

* Mon Aug 12 2012 olivier.mauras@nagra.com
- Version bump

* Mon Aug 08 2011 olivier.mauras@nagra.com
- First release
- Perforce Perl bindings

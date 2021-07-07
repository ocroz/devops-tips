%define _apiversion 2138914

Summary: Perforce API
Name: perforce-api
Version: 2020.1
Release: 2%{?dist}
License: Proprietary
URL: https://ftp.perforce.com/perforce/r20.1/bin.linux26x86_64/

Source: p4api.tgz
#Source: p4api-glibc2.12-openssl1.0.2.tgz

%description
Perforce API

%prep
%setup -c %{name}-%{version}

%install
# Create directories
install -p -d -m 0755 %{buildroot}/usr/local

# Copy P4API
cp -r p4api-%{version}.%{_apiversion} %{buildroot}/usr/local/p4api

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
/usr/local/p4api

%changelog
* Wed Jun 30 2021 olivier.crozier@nagra.com - 2020.1-1
- p4api downdgrade to 2020.1/2138914

* Wed Jun 30 2021 matthieu.castellazzi@nagra.com - 2021.1-2
- p4api with glibc 2.12 and openssl 1.0.2

* Wed Jun 30 2021 matthieu.castellazzi@nagra.com - 2021.1-1
- Upgrade to 2021.1/2126753 (2021/05/12)

* Fri Nov 11 2016 Olivier Mauras <olivier.mauras@nagra.com> - 2015.2-6
- Modify perforce-server.systemd to gracefully shutdown server

* Fri Apr 08 2016 matthieu.castellazzi@nagra.com - 2015.2-5
- Upgrade to 2015.2/1340214 - new p4api

* Fri Mar 04 2016 matthieu.castellazzi@nagra.com - 2015.2-4
- Improve unit file with NICE and OOMScoreAdjust values

* Wed Jan 06 2016 quanghai.nguyen@nagra.com - 2015.2-2
- Upgrade to 2015.2/1319959 (2015/12/28)

* Fri Nov 13 2015 quanghai.nguyen@nagra.com - 2015.2-2
- Fix perforce-proxy/broker with option "-d"

* Thu Nov 05 2015 matthieu.castellazzi@nagra.com - 2015.2-1
- Upgrade to 2015.2

* Thu Oct 08 2015 olivier.mauras@nagra.com - 2015.1-3
- Systemd unit files again...

* Tue Oct 06 2015 olivier.mauras@nagra.com - 2015.1-2
- Fix user in systemd unit files

* Wed Sep 30 2015 olivier.mauras@nagra.com - 2015.1-1
- Upgrade to 2015.1
- Add systemd support
- Re-merge proxy
- Add new p4broker

* Fri Aug 23 2013 olivier.mauras@nagra.com - 2012.2-2
- Make perforce proxy as a separate package

* Tue Feb 05 2013 olivier.mauras@nagra.com - 2012.2
- Version bump

* Sun Aug 12 2012 olivier.mauras@nagra.com
- Version bump

* Mon Aug 08 2011 olivier.mauras@nagra.com
- First release
- Perforce binaries and API

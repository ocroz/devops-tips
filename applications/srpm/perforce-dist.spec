%define _apiversion 2126753

Summary: Perforce SCM
Name: perforce
Version: 2021.1
Release: 2%{?dist}
License: Proprietary
Group: System Environment/Daemons
URL: http://cdist2.perforce.com/perforce/r21.1/bin.linux26x86_64/

Source: p4api-glibc2.12-openssl1.0.2.tgz
Source1: helix-core-server.tgz
Source2: perforce-server.systemd
Source3: perforce-proxy.systemd
Source4: perforce-broker.systemd

%description
Fast and scalable SCM server

%package server
Summary: Perforce server daemon
%description server
Perforce server daemon

%package proxy
Summary: Perforce proxy daemon
%description proxy
Perforce proxy daemon

%package broker
Summary: Perforce broker daemon
%description broker
Perforce broker daemon

%package client
Summary: Perforce client binary
%description client
Perforce client binary

%package api
Summary: Perforce API required by %{name} bindings
%description api
Perforce API required by %{name} bindings

%prep
%setup -c

%install
# Create directories
install -p -d -m 0755 %{buildroot}/usr/local/bin
install -p -d -m 0755 %{buildroot}/usr/lib/systemd/system/
install -p -D -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/perforce-server.service
install -p -D -m 0644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/perforce-proxy.service
install -p -D -m 0644 %{SOURCE4} %{buildroot}/usr/lib/systemd/system/perforce-broker.service

# Copy P4API
cp -r p4api-%{version}.%{_apiversion} %{buildroot}/usr/local/p4api

# Extract binaries
tar xf %{SOURCE1}

for i in p4 p4broker p4d p4p; do
    install -p -m 0755 $i %{buildroot}/usr/local/bin/
done

%post server
/bin/systemctl enable perforce-server

%preun server
if [ $1 -eq 0 ]; then
    /bin/systemctl stop perforce-server &>/dev/null || :
    /bin/systemctl disable perforce-server
fi

%post proxy
/bin/systemctl enable perforce-proxy

%preun proxy
if [ $1 -eq 0 ]; then
    /bin/systemctl stop perforce-proxy &>/dev/null || :
    /bin/systemctl disable perforce-proxy
fi

%post broker
/bin/systemctl enable perforce-broker

%preun broker
if [ $1 -eq 0 ]; then
    /bin/systemctl stop perforce-broker &>/dev/null || :
    /bin/systemctl disable perforce-broker
fi

%clean
%{__rm} -rf %{buildroot}

%files

%files server
%defattr(-, root, root, 0755)
/usr/local/bin/p4d
/usr/lib/systemd/system/perforce-server.service

%files client
%defattr(-, root, root, 0755)
/usr/local/bin/p4

%files proxy
%defattr(-, root, root, 0755)
/usr/local/bin/p4p
/usr/lib/systemd/system/perforce-proxy.service

%files broker
%defattr(-, root, root, 0755)
/usr/local/bin/p4broker
/usr/lib/systemd/system/perforce-broker.service

%files api
%defattr(-, root, root, 0755)
/usr/local/p4api

%changelog
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

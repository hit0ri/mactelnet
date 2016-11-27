Name:             mactelnet
Version:          0.4.4
Release:          1%{?dist}
Summary:          RouterOS Mac-Telnet applications

License:          GPLv2
URL:              http://lunatic.no/2010/10/routeros-mac-telnet-application-for-linux-users/
# https://github.com/haakonnessjoen/MAC-Telnet
Source0:          https://github.com/haakonnessjoen/MAC-Telnet/archive/v%{version}.tar.gz
Source1:          mactelnetd.service
Patch0:           %{name}-chown.patch

BuildRequires:    systemd
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    gettext-devel

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Console tools for connecting to, and serving, devices using MikroTik RouterOS
MAC-Telnet protocol.

%prep
%setup -q -n MAC-Telnet-%{version}
%patch0 -p1

%build
./autogen.sh
%configure
%make_build

%install
%make_install
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/mactelnetd.service
%find_lang %{name}

%pre
getent group mactelnetd >/dev/null || groupadd -r mactelnetd
getent passwd mactelnetd >/dev/null || useradd -r -g mactelnetd \
    -d %{_localstatedir}/lib/mactelnetd -s /sbin/nologin \
    -c "MAC-Telnet server" mactelnetd
exit 0

%post
%systemd_post mactelnetd.service

%preun
%systemd_preun mactelnetd.service

%postun
%systemd_postun_with_restart mactelnetd.service

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.markdown
%{_bindir}/mndp
%{_bindir}/macping
%{_bindir}/mactelnet
%{_sbindir}/mactelnetd
%{_mandir}/man1/*.1.gz
%{_unitdir}/mactelnetd.service
%config(noreplace) %attr(640, root, mactelnetd) %{_sysconfdir}/mactelnetd.users

%changelog
* Sun Nov 27 2016 Taras Dyshkant <hitori.gm@gmail.com> - 0.4.4-1
- Initial release

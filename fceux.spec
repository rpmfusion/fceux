Name:           fceux
Version:        2.2.2
Release:        2%{?dist}
Summary:        A cross platform, NTSC and PAL Famicom/NES emulator

Group:          Applications/Emulators
License:        GPLv2+
URL:            http://fceux.com/
Source:         http://downloads.sourceforge.net/fceultra/%{name}-%{version}.src.tar.gz

BuildRequires:  scons
BuildRequires:  SDL-devel >= 1.2.14
BuildRequires:  gtk2-devel >= 2.18
BuildRequires:  gd-devel
%if 0%{?fedora} >= 20
BuildRequires:  compat-lua-devel
%else
BuildRequires:  lua-devel
%endif
BuildRequires:  minizip-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Provides:       fceultra = %{version}-%{release}
Obsoletes:      fceultra < 2.0.0
Provides:       gfceu = %{version}-%{release}
Obsoletes:      gfceu <= 0.6.2


%description
FCEUX is a cross platform, NTSC and PAL Famicom/NES emulator that is an
evolution of the original FCE Ultra emulator. Over time FCE Ultra had
separated into many separate branches.

The concept behind FCEUX is to merge elements from FCE Ultra, FCEU
rerecording, FCEUXD, FCEUXDSP, and FCEU-mm into a single branch of FCEU. As
the X implies, it is an all-encompassing FCEU emulator that gives the best
of all worlds for the casual player, the ROM-hacking community, Lua
Scripters, and the Tool-Assisted Speedrun Community.


%package net-server
Summary: Server for the FCEUX emulator

%description net-server
FCEUX clients can connect to this server and play multiplayer NES games over 
the network. 


%prep
%setup -q

# Remove windows binary
rm fceux-server/fceux-net-server.exe

# Remove ~attic directories
find . -name '~attic' -type d -prune -exec rm -rf {} \;

# Remove Visual Studio directory
rm -rf vc

# Remove bundled LUA library
rm -rf src/lua

# Fix for LUA 5.1
sed -i 's/lua5.1/lua-5.1/' SConstruct

# Remove bundled minizip library
rm -rf src/utils/unzip.*

# Fix end-of-line-encoding
sed -i 's/\r//' changelog.txt NewPPUtests.txt \
  documentation/Videolog.txt \
  fceux-server/{AUTHORS,ChangeLog,README}

# Fix desktop file
sed -i 's/\/usr\/share\/pixmaps\/fceux.png/fceux/' fceux.desktop
sed -i '/MimeType=*/s/$/;/' fceux.desktop
sed -i '/OnlyShowIn=*/s/$/;/' fceux.desktop


%build
export CFLAGS="%{optflags}"
# Enable system LUA
# Enable system minizip
# Enable AVI creation
scons %{?_smp_mflags} \
  SYSTEM_LUA=1 \
  SYSTEM_MINIZIP=1 \
  CREATE_AVI=1


%install
# Install binary files
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/fceux %{buildroot}%{_bindir}
install -p -m 755 bin/fceux-net-server %{buildroot}%{_bindir}

# Install data
install -d %{buildroot}%{_datadir}/%{name}
cp -pR output/{palettes,luaScripts} %{buildroot}%{_datadir}/%{name}
install -p -m 644 bin/auxlib.lua %{buildroot}%{_datadir}/%{name}/luaScripts/

# Install icon
install -d %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# Install desktop file
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

# Install man pages
install -d %{buildroot}%{_mandir}/man6
install -p -m 644 documentation/fceux.6 \
  %{buildroot}%{_mandir}/man6/
install -p -m 644 documentation/fceux-net-server.6 \
  %{buildroot}%{_mandir}/man6/

# Install config file
install -d %{buildroot}%{_sysconfdir}
install -p -m 644 fceux-server/fceux-server.conf \
  %{buildroot}%{_sysconfdir}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man6/%{name}.6*
%doc Authors changelog.txt COPYING NewPPUtests.txt README-SDL TODO-SDL
%doc documentation/{cheat.html,faq,todo,TODO-PROJECT,Videolog.txt}

%files net-server
%{_bindir}/fceux-net-server
%config(noreplace) %{_sysconfdir}/fceux-server.conf
%{_mandir}/man6/fceux-net-server.6*
%doc fceux-server/{AUTHORS,ChangeLog,COPYING,README}


%changelog
* Wed Oct 23 2013 Andrea Musuruane <musuruan@gmail.com> - 2.2.2-2
- Added missing update of desktop database

* Sat Oct 19 2013 Andrea Musuruane <musuruan@gmail.com> - 2.2.2-1
- Updated to new upstream realease
- Removed non longer needed patches
- Built with compat-lua for F20+

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-2
- Rebuilt for GD 2.1.0

* Tue Apr 02 2013 Andrea Musuruane <musuruan@gmail.com> - 2.2.1-1
- Updated to new upstream realease
- Packaged fceux-net-server too
- Imported Debian patches
- Enabled LUA scripting

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.5-3
- Mass rebuilt for Fedora 19 Features

* Sat Apr 28 2012 Andrea Musuruane <musuruan@gmail.com> 2.1.5-2
- Obsoleted gfceu too
- Notified upstream about underlinking

* Sun Apr 22 2012 Andrea Musuruane <musuruan@gmail.com> 2.1.5-1
- First release for RPM Fusion
- LUA support is disabled because fceux uses a private header file
- Reused Gentoo and upstream patches
- Made a patch not to use the bundled minizip library


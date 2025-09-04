%global giturl https://github.com/TASVideos/fceux.git
%global commit 34eb7601c415b81901fd02afbd5cfdc84b5047ac

Name:           fceux
Version:        2.6.6
Release:        11%{?dist}
Summary:        A cross platform, NTSC and PAL Famicom/NES emulator

License:        GPLv2+
URL:            http://fceux.com/
Source:         https://github.com/TASEmulators/fceux/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         gcc13.patch
# Added feature macro __FCEU_X86_TSC_ENABLE to enable usage of the X86 TSC
# https://github.com/TASEmulators/fceux/issues/663
Patch1:         fceux-2.6.6-timestamp-nonx86.patch
# Add cmath include
Patch2:         fceux-2.6.6-gcc15.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  SDL2-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  compat-lua-devel
%if 0%{?rhel}
BuildRequires:  minizip-devel
%else
BuildRequires:  minizip-compat-devel
%endif
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

Provides:       fceultra = %{version}-%{release}
Obsoletes:      fceultra < 2.0.0
Provides:       gfceu = %{version}-%{release}
Obsoletes:      gfceu <= 0.6.2
Obsoletes:      fceux-net-server <= 2.2.3


%description
FCEUX is a cross platform, NTSC and PAL Famicom/NES emulator that is an
evolution of the original FCE Ultra emulator. Over time FCE Ultra had
separated into many separate branches.

The concept behind FCEUX is to merge elements from FCE Ultra, FCEU
rerecording, FCEUXD, FCEUXDSP, and FCEU-mm into a single branch of FCEU. As
the X implies, it is an all-encompassing FCEU emulator that gives the best
of all worlds for the casual player, the ROM-hacking community, Lua
Scripters, and the Tool-Assisted Speedrun Community.


%prep
%autosetup -p1

# Remove attic directories
find . -name 'attic' -type d -prune -exec rm -rf {} \;

# Remove Visual Studio directory
rm -rf vc

# Remove bundled LUA library
rm -rf src/lua

# Remove bundled minizip library
rm -rf src/utils/unzip.*

# Fix end-of-line-encoding
sed -i 's/\r//' changelog.txt NewPPUtests.txt \
  documentation/Videolog.txt

# Fix desktop file
sed -i '/Encoding=/d' fceux.desktop
sed -i 's/\/usr\/share\/pixmaps\/fceux1.png/fceux/' fceux.desktop
sed -i '/MimeType=*/s/$/;/' fceux.desktop
sed -i '/OnlyShowIn=*/s/$/;/' fceux.desktop

# Public release
sed -i 's!//#define PUBLIC_RELEASE!#define PUBLIC_RELEASE!' src/version.h

# Set git data
sed -i -r 's!(GIT_URL=).+!\1"%{giturl}"!' scripts/genGitHdr.sh
sed -i -r 's!(GIT_REV=).+!\1"%{commit}"!' scripts/genGitHdr.sh


%build
%cmake
%cmake_build


%install
%cmake_install

# Install icons
install -d %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -d %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -p -m 644 %{name}1.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_datadir}/pixmaps/%{name}1.png
%{_mandir}/man6/%{name}.6*
%exclude %{_mandir}/man6/%{name}-net-server.6*
%doc changelog.txt NewPPUtests.txt README TODO-SDL
%doc documentation/{cheat.html,faq,todo,TODO-PROJECT,Videolog.txt}
%license COPYING


%changelog
* Thu Sep 04 2025 Sérgio Basto <sergio@serjux.com> - 2.6.6-11
- Rebuild for x264

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Andrea Musuruane <musuruan@gmail.com> - 2.6.6-9
- Fix FTBFS with GCC 15

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 23 2024 Leigh Scott <leigh123linux@gmail.com> - 2.6.6-7
- Rebuild for new x265

* Sat Oct 26 2024 Andrea Musuruane <musuruan@gmail.com> - 2.6.6-6
- Rebuild for ffmpeg 7

* Thu Aug 01 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Apr 06 2024 Leigh Scott <leigh123linux@gmail.com> - 2.6.6-4
- Rebuild for new x265 version

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 07 2023 Andrea Musuruane <musuruan@gmail.com> - 2.6.6-2
- Added a patch to fix building on non-x86 CPUs

* Wed Aug 30 2023 Andrea Musuruane <musuruan@gmail.com> - 2.6.6-1
- Updated to new upstream release

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 02 2023 Andrea Musuruane <musuruan@gmail.com> - 2.6.5-1
- Updated to new upstream release

* Fri Mar 03 2023 Leigh Scott <leigh123linux@gmail.com> - 2.6.4-4
- Rebuild for new ffmpeg

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sun Jun 12 2022 Sérgio Basto <sergio@serjux.com> - 2.6.4-2
- Mass rebuild for x264-0.164

* Sun Mar 27 2022 Andrea Musuruane <musuruan@gmail.com> - 2.6.4-1
- Updated to new upstream release

* Sat Mar 12 2022 Andrea Musuruane <musuruan@gmail.com> - 2.6.3-1
- Updated to new upstream release

* Sat Feb 05 2022 Andrea Musuruane <musuruan@gmail.com> - 2.6.2-1
- Updated to new upstream release

* Tue Jan 18 2022 Andrea Musuruane <musuruan@gmail.com> - 2.6.1-1
- Updated to new upstream release

* Fri Nov 12 2021 Andrea Musuruane <musuruan@gmail.com> - 2.5.0-1
- Updated to new upstream release

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Sérgio Basto <sergio@serjux.com> - 2.4.0-2
- Mass rebuild for x264-0.163

* Thu Jul 01 2021 Andrea Musuruane <musuruan@gmail.com> - 2.4.0-1
- Updated to new upstream release

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 11:08:08 CET 2021 Andrea Musuruane <musuruan@gmail.com> - 2.3.0-1
- Updated to new upstream release
- Obsoleted fceux-net-server because it is no longer supported upsteam

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 Andrea Musuruane <musuruan@gmail.com> - 2.2.3-8
- Fixed building with python3 scons

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Andrea Musuruane <musuruan@gmail.com> - 2.2.3-6
- Added gcc-c++ dependency
- Updated BR to minizip-compat-devel for F30+
- Used %%set_build_flags macro
- Removed desktop scriptlets
- Removed update-desktop-database
- Added license tag

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 11 2017 Andrea Musuruane <musuruan@gmail.com> - 2.2.3-1
- Updated to new upstream release
- Dropped obsolete Group tag

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

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


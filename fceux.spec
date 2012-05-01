Name:           fceux
Version:        2.1.5
Release:        2%{?dist}
Summary:        A cross platform, NTSC and PAL Famicom/NES emulator

Group:          Applications/Emulators
License:        GPLv2+
URL:            http://fceux.com/
Source:         http://downloads.sourceforge.net/fceultra/%{name}-%{version}.src.tar.bz2
# Fix compiling
# https://bugs.gentoo.org/show_bug.cgi?id=406471
# Upstream SVN rev 2395
Patch0:         %{name}-2.1.5-datatype-gz.patch
# Fix underlinking
# https://bugs.gentoo.org/show_bug.cgi?id=367675
# http://sourceforge.net/tracker/?func=detail&aid=3522221&group_id=13536&atid=113536
Patch1:         %{name}-2.1.5-underlink.patch
# Use system minizip
# https://sourceforge.net/tracker/?func=detail&aid=3520369&group_id=13536&atid=113536
Patch2:         %{name}-2.1.5-minizip.patch
# Fix compiling with GCC 4.7
# Upstream SVN rev 2484
Patch3:         %{name}-2.1.5-gcc47.patch

BuildRequires:  scons
BuildRequires:  SDL-devel >= 1.2.14
BuildRequires:  gtk2-devel >= 2.18
BuildRequires:  gd-devel
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


%prep
%setup -q -n fceu%{version}
%patch0 -p2
%patch1 -p0
%patch2 -p1
%patch3 -p1

# Remove binary files
rm -rf bin/fceux
rm -rf src/fceux

# Remove bundled LUA library
rm -rf src/lua
sed -i 's/^lua//' src/SConscript

# Remove bundled minizip library
rm -rf src/utils/unzip.*
sed -i 's/^unzip.cpp//' src/utils/SConscript

# Remove default CFLAGS
sed -i 's/^env.Append(CCFLAGS/#env.Append(CCFLAGS/' SConstruct

# Fix end-of-line-encoding
sed -i 's/\r//' Authors.txt changelog.txt TODO-PROJECT \
  documentation/Videolog.txt

# Fix icon path in desktop file
sed -i 's/\/usr\/share\/pixmaps\/fceux.png/fceux/' fceux.desktop


%build
export CFLAGS="%{optflags}"
# Disable LUA support
# Enable AVI creation
scons %{?_smp_mflags} \
  LUA=0 \
  CREATE_AVI=1


%install
# Install binary file
install -d %{buildroot}%{_bindir}
install -p -m 755 src/fceux %{buildroot}%{_bindir}

# Install icon
install -d %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# Install desktop file
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

# Install man page
install -d %{buildroot}%{_mandir}/man6
install -p -m 644 documentation/%{name}.6 \
  %{buildroot}%{_mandir}/man6/%{name}.6


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/fceux
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man6/%{name}.6*
%doc Authors.txt changelog.txt COPYING README-SDL TODO-PROJECT TODO-SDL
%doc documentation/{cheat.html,faq,todo,Videolog.txt}


%changelog
* Sat Apr 28 2012 Andrea Musuruane <musuruan@gmail.com> 2.1.5-2
- Obsoleted gfceu too
- Notified upstream about underlinking

* Sun Apr 22 2012 Andrea Musuruane <musuruan@gmail.com> 2.1.5-1
- First release for RPM Fusion
- LUA support is disabled because fceux uses a private header file
- Reused Gentoo and upstream patches
- Made a patch not to use the bundled minizip library


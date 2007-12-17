%define name    cultivation
%define Name    Cultivation
%define version 9
%define snapshot 20071217
%define release %mkrel 0.%{snapshot}.1

Name:	    %{name}
Version:    %{version}
Release:    %{release}
Summary:    A game about the interactions within a gardening community
License:    Public Domain
Group:	    Games/Strategy
URL:	    http://cultivation.sourceforge.net/
Source0:    %Name-%{version}cvs%{snapshot}.tar.bz2
BuildRequires:	mesaglut-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Cultivation is a game about a community of gardeners growing food
for themselves in a shared space.

Cultivation is quite different from most other games. It is a
social simulation, and the primary form of conflict is over land
and plant resources --- there is no shooting, but there are plenty
of angry looks. It is also an evolution simulation. Within the
world of Cultivation, you can explore a virtually infinite
spectrum of different plant and gardener varieties.

All of the graphics, sounds, melodies,and other content in
Cultivation are 100% procedurally generated at playtime. In other
words, there are no hand-painted texture maps --- instead, each
object has a uniquely 'grown' appearance. Every time you play,
Cultivation generates fresh visuals, music, and behaviors.


%prep
%setup -q -n %{Name}-%{version}cvs%{snapshot}

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC"
pushd minorGems/sound/portaudio
	chmod u+x ./configure
	%configure2_5x
	%__make
popd

pushd game2
%__rm -f gameSource/Makefile
%__cat \
	Makefile.GnuLinux \
	Makefile.common \
	../minorGems/build/Makefile.minorGems \
	gameSource/Makefile.all \
	../minorGems/build/Makefile.minorGems_targets > gameSource/Makefile

pushd gameSource
	%__make %{?_smp_mflags}
popd

popd

%install
install -d -m 755 %{buildroot}%{_gamesbindir}
install -m 755 game2/gameSource/%{Name} \
	%{buildroot}%{_gamesbindir}

install -d -m 755 %{buildroot}%{_gamesdatadir}/%{Name}
install -m 644 game2/gameSource/font.tga \
	%{buildroot}%{_gamesdatadir}/%{Name}
install -m 644 game2/gameSource/features.txt \
	%{buildroot}%{_gamesdatadir}/%{Name}
install -m 644 game2/gameSource/language.txt \
	%{buildroot}%{_gamesdatadir}/%{Name}
install -d -m 755 %{buildroot}%{_gamesdatadir}/%{Name}/languages
install -m 644 game2/gameSource/languages/*.txt \
	%{buildroot}%{_gamesdatadir}/%{Name}/languages

# startscript
%__cat > %{Name}.sh <<'EOF'
#!/bin/bash
if [ ! -d $HOME/%{Name} ]; then
	mkdir -p $HOME/%{Name}
	cd $HOME/%{Name}
	cp %{_gamesdatadir}/%{Name}/*.txt .
	ln -s %{_gamesdatadir}/%{Name}/*.tga .
	ln -s %{_gamesdatadir}/%{Name}/languages .
	ln -s %{_gamesbindir}/%{Name} .
fi

cd $HOME/%{name}

# Basic switch of language according to locale defined in Unix systems
case "$LC_MESSAGES" in
    fr* )
        language="French"
	;;
    pt* )
        language="Portuguese"
	;;
    * )
        language="English"
	;;
esac
echo $language > ./language.txt

./%{name}
EOF
install -m 755 %{Name}.sh \
	%{buildroot}%{_gamesbindir}

# icon
install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 game2/build/win32/iconSource.png \
	%{buildroot}%{_datadir}/pixmaps/%{Name}.png

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{Name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{Name}
Comment=%summary
Exec=%{Name}.sh
Icon=%{Name}.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;SimulationGame;
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, games)
%doc game2/documentation/*
%{_gamesbindir}/%{Name}
%{_gamesbindir}/%{Name}.sh
%{_gamesdatadir}/%{Name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png


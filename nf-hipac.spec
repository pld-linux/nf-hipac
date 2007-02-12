Summary:	nf-HiPAC - high performance packet classification
Summary(pl.UTF-8):   nf-HiPAC - wysoko wydajna klasyfikacja pakietów
Name:		nf-hipac
Version:	0.9.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/nf-hipac/%{name}-%{version}.tar.bz2
# Source0-md5:	725efec87aa93e8e83e8799c9058f143
Patch0:		%{name}-Makefile.patch
URL:		http://www.hipac.org/
BuildRequires:	linux-libc-headers
#Requires:	iptables
Requires:	kernel(nf-hipac) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nf-HiPAC is a full featured packet filter for Linux which demonstrates
the power and flexibility of HiPAC. HiPAC is a novel framework for
packet classification which uses an advanced algorithm to reduce the
number of memory lookups per packet. It is ideal for environments
involving large rule sets and/or high bandwidth networks.

nf-HiPAC provides the same rich feature set as iptables, the popular
Linux packet filter. The complexity of the sophisticated HiPAC packet
classification algorithm is hidden behind an iptables compatible user
interface which renders nf-HiPAC a drop-in replacement for iptables.
Thereby, the iptables' semantics of the rules is preserved, i.e. you
can construct your rules like you are used to. From a user's point of
view there is no need to understand anything about the HiPAC
algorithm.

%description -l pl.UTF-8
nf-HiPAC to w pełni funkcjonalny filtr pakietów dla Linuksa
demonstrujący siłę i elastyczność HiPAC-a. HiPAC to nowy szkielet
klasyfikacji pakietów używający zaawansowanego algorytmu do
ograniczenia liczby wyszukiwań w pamięci dla pakietu. Jest idealny dla
środowisk z dużymi zbiorami reguł i/lub sieci o dużej przepustowości.

nf-HiPAC udostępnia ten sam bogaty zbiór możliwości co iptables -
popularny linuksowy filtr pakietów. Złożoność wyszukanego algorytmu
klasyfikacji pakietów HiPAC-a jest ukryta za zgodnym z iptables
interfejsem użytkownika czyniący nf-HiPAC-a zamiennikiem iptables.
Przy tym zachowana jest semantyka reguł iptables, czyli można tworzyć
reguły tak samo jak wcześniej. Z punktu widzenia użytkownika nie ma
potrzeby rozumienia niczego o algorytmie HiPAC.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -C user clean all \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	IPT_LIB_DIR=%{_libdir}/iptables

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C user install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG FEATURES README TODO
%attr(755,root,root) %{_sbindir}/nf-hipac
%attr(755,root,root) %{_libdir}/libnfhipac.so

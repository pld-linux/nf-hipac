Summary:	nf-HiPAC - high performance packet classification
Name:		nf-hipac
Version:	0.9.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	%{name}-%{version}.tar.bz2
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

The nf-hipac user space tool is designed to be as compatible as
possible to 'iptables -t filter'. It even supports the full power of
iptables targets, matches and stateful packet filtering (connection
tracking) besides the native nf-HiPAC matches. This makes a switch
from iptables to nf-HiPAC very easy. Usually it is sufficient to
replace the calls to iptables with calls to nf-hipac for your filter
rules.

Why another packet filter?

Performance:

iptables, like most packet filters, uses a simple packet
classification algorithm which traverses the rules in a chain linearly
per packet until a matching rule is found (or not). Clearly, this
approach lacks efficiency. As networks grow more and more complex and
offer a wider bandwidth linear packet filtering is no longer an option
if many rules have to be matched per packet. Higher bandwidth means
more packets per second which leads to shorter process times per
packet. nf-HiPAC outperforms iptables regardless of the number of
rules, i.e. the HiPAC classification engine does not impose any
overhead even for very small rule sets.

Scalability to large rule sets:

The performance of nf-HiPAC is nearly independent of the number of
rules. nf-HiPAC with thousands of rules still outperforms iptables
with 20 rules.

Dynamic rule sets:

nf-HiPAC offers fast dynamic rules et updates without stalling packet
classification in contrast to iptables which yields bad update
performance along with stalled packet processing during updates.

%prep
%setup -q
%patch0 -p1

%build
cd user
%{__make} clean all \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}" \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	IPT_LIB_DIR=%{_libdir}/iptables

%install
rm -rf $RPM_BUILD_ROOT

cd user
%{__make} install \
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

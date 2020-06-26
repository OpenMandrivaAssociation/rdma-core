
%define ibmadmajor 5
%define ibnetdiscmajor 5
%define ibverbsmajor 1
%define ibumadmajor 3
%define rdmacmmajor 1

%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d

%define libibverbs %mklibname ibverbs %{ibverbsmajor}
%define libibumad %mklibname ibumad %{ibumadmajor}
%define libibmad %mklibname ibumad %{ibmadmajor}
%define librdmacm %mklibname rdmacm %{rdmacmmajor}
%define libibnetdisc %mklibname ibnetdisc %{ibnetdiscmajor}

%define devname %mklibname %{name} -d

%bcond_with docs

Name: rdma-core
Version: 30.0
Release: 1
Summary: RDMA core userspace libraries and daemons
Group: System/Servers

# Almost everything is licensed under the OFA dual GPLv2, 2 Clause BSD license
#  providers/ipathverbs/ Dual licensed using a BSD license with an extra patent clause
#  providers/rxe/ Incorporates code from ipathverbs and contains the patent clause
#  providers/hfi1verbs Uses the 3 Clause BSD license
License: GPLv2 or BSD
Url: https://github.com/linux-rdma/rdma-core
Source0: https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/rdma-core-%{version}.tar.gz
Patch0:	cmake.patch
# 32-bit arm is missing required arch-specific memory barriers
ExcludeArch: %{arm}

BuildRequires: cmake >= 2.8.11
BuildRequires: ninja
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
BuildRequires: perl-generators
%if %{with docs}
BuildRequires: pandoc
%endif

Provides: rdma = %{EVRD}
Provides: rdma-ndd = %{EVRD}
# the ndd utility moved from infiniband-diags to rdma-core
Conflicts: infiniband-diags <= 1.6.7


%description
RDMA core userspace infrastructure and documentation, including initialization
scripts, kernel driver-specific modprobe override configs, IPoIB network
scripts, dracut rules, and the rdma-ndd utility.

%files
%dir %{_sysconfdir}/rdma
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README.md
%doc %{_docdir}/%{name}-%{version}/rxe.md
%doc %{_docdir}/%{name}-%{version}/udev.md
%doc %{_docdir}/%{name}-%{version}/tag_matching.md
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%{sysmodprobedir}/libmlx4.conf
%{_libexecdir}/mlx4-setup.sh
%config(noreplace) %{_sysconfdir}/rdma/modules/infiniband.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/iwarp.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/opa.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/rdma.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/roce.conf
%config(noreplace) %{_sysconfdir}/rdma/rdma.conf
%config(noreplace) %{_sysconfdir}/rdma/sriov-vfs
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/modprobe.d/truescale.conf
%{_unitdir}/rdma-hw.target
%{_unitdir}/rdma-load-modules@.service
%{_unitdir}/rdma.service
%dir %{dracutlibdir}/modules.d/05rdma
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%{_udevrulesdir}/60-rdma-persistent-naming.rules
%{_udevrulesdir}/../rdma_rename
%{_udevrulesdir}/60-rdma-ndd.rules
%{_udevrulesdir}/75-rdma-description.rules
%{_udevrulesdir}/90-rdma-hw-modules.rules
%{_udevrulesdir}/90-rdma-ulp-modules.rules
%{_udevrulesdir}/90-rdma-umad.rules
%{_udevrulesdir}/98-rdma.rules
%{sysmodprobedir}/libmlx4.conf
%{_libexecdir}/rdma-init-kernel
%{_libexecdir}/rdma-set-sriov-vf
%{_libexecdir}/truescale-serdes.cmds
%{_sbindir}/rdma-ndd
%{_unitdir}/rdma-ndd.service
%{_mandir}/man7/rxe*
%{_mandir}/man8/rdma-ndd.*
%license COPYING.*

#===================================================================
%package -n 	%{devname}
Summary:	RDMA core development libraries and headers
Requires:	%{name} = %{EVRD}
Requires:	%{libibverbs} = %{EVRD}
Requires:	%{libibumad} = %{EVRD}
Requires:	%{librdmacm} = %{EVRD}
Requires:	%{libibnetdisc} = %{EVRD}
Requires:	ibacm = %{EVRD}
Provides:	ibacm-devel = %{EVRD}
Requires:	infiniband-diags = %{EVRD}
Provides:	infiniband-diags-devel = %{EVRD}
Provides:	%{_lib}ibmad-devel = %{EVRD}

%description -n	%{devname}
RDMA core development libraries and headers.

%files -n %{devname}
%doc %{_docdir}/%{name}-%{version}/MAINTAINERS
%dir %{_includedir}/infiniband
%dir %{_includedir}/rdma
%{_includedir}/infiniband/*
%{_includedir}/rdma/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/efadv*
%{_mandir}/man7/efadv*
%{_mandir}/man3/ibv_*
%{_mandir}/man3/rdma*
%{_mandir}/man3/umad*
%{_mandir}/man3/*_to_ibv_rate.*
%{_mandir}/man7/rdma_cm.*
%{_mandir}/man3/ibnd_*
%{_mandir}/man3/mlx4dv*
%{_mandir}/man7/mlx4dv*
%{_mandir}/man3/mlx5dv*
%{_mandir}/man7/mlx5dv*
%{_mandir}/man3/mlx4dv*
%{_mandir}/man7/mlx4dv*

#===================================================================
%package -n infiniband-diags
Summary: InfiniBand Diagnostic Tools
Provides: perl(IBswcountlimits)
Requires: %{libibmad} = %{EVRD}
Requires: %{libibnetdisc} = %{EVRD}

%description -n infiniband-diags
This package provides IB diagnostic programs and scripts needed to diagnose an
IB subnet.  infiniband-diags now also provides libibmad.  libibmad provides
low layer IB functions for use by the IB diagnostic and management
programs. These include MAD, SA, SMP, and other basic IB functions.

%files -n infiniband-diags
%{_sbindir}/ibaddr
%{_mandir}/man8/ibaddr*
%{_sbindir}/ibnetdiscover
%{_mandir}/man8/ibnetdiscover*
%{_sbindir}/ibping
%{_mandir}/man8/ibping*
%{_sbindir}/ibportstate
%{_mandir}/man8/ibportstate*
%{_sbindir}/ibroute
%{_mandir}/man8/ibroute.*
%{_sbindir}/ibstat
%{_mandir}/man8/ibstat.*
%{_sbindir}/ibsysstat
%{_mandir}/man8/ibsysstat*
%{_sbindir}/ibtracert
%{_mandir}/man8/ibtracert*
%{_sbindir}/perfquery
%{_mandir}/man8/perfquery*
%{_sbindir}/sminfo
%{_mandir}/man8/sminfo*
%{_sbindir}/smpdump
%{_mandir}/man8/smpdump*
%{_sbindir}/smpquery
%{_mandir}/man8/smpquery*
%{_sbindir}/saquery
%{_mandir}/man8/saquery*
%{_sbindir}/vendstat
%{_mandir}/man8/vendstat*
%{_sbindir}/iblinkinfo
%{_mandir}/man8/iblinkinfo*
%{_sbindir}/ibqueryerrors
%{_mandir}/man8/ibqueryerrors*
%{_sbindir}/ibcacheedit
%{_mandir}/man8/ibcacheedit*
%{_sbindir}/ibccquery
%{_mandir}/man8/ibccquery*
%{_sbindir}/ibccconfig
%{_mandir}/man8/ibccconfig*
%{_sbindir}/dump_fts
%{_mandir}/man8/dump_fts*
%{_sbindir}/ibhosts
%{_mandir}/man8/ibhosts*
%{_sbindir}/ibswitches
%{_mandir}/man8/ibswitches*
%{_sbindir}/ibnodes
%{_mandir}/man8/ibnodes*
%{_sbindir}/ibrouters
%{_mandir}/man8/ibrouters*
%{_sbindir}/ibfindnodesusing.pl
%{_mandir}/man8/ibfindnodesusing*
%{_sbindir}/ibidsverify.pl
%{_mandir}/man8/ibidsverify*
%{_sbindir}/check_lft_balance.pl
%{_mandir}/man8/check_lft_balance*
%{_sbindir}/dump_lfts.sh
%{_mandir}/man8/dump_lfts*
%{_sbindir}/dump_mfts.sh
%{_mandir}/man8/dump_mfts*
%{_sbindir}/ibclearerrors
%{_mandir}/man8/ibclearerrors*
%{_sbindir}/ibclearcounters
%{_mandir}/man8/ibclearcounters*
%{_sbindir}/ibstatus
%{_mandir}/man8/ibstatus*
%{_mandir}/man8/infiniband-diags*
%{perl_vendorlib}/IBswcountlimits.pm
%config(noreplace) %{_sysconfdir}/infiniband-diags/error_thresholds
%config(noreplace) %{_sysconfdir}/infiniband-diags/ibdiag.conf

#====================================================================
%package -n %{libibmad}
Summary: OpenFabrics Alliance InfiniBand mad (userspace management datagram) library
Requires: %{name} = %{EVRD}

%description -n %{libibmad}
libibmad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%files -n %{libibmad}
%{_libdir}/libibmad*.so.%{ibmadmajor}*

#===================================================================

%package -n infiniband-diags-compat
Summary: OpenFabrics Alliance InfiniBand Diagnostic Tools

%description -n infiniband-diags-compat
Deprecated scripts and utilities which provide duplicated functionality, most
often at a reduced performance. These are maintained for the time being for
compatibility reasons.

%files -n infiniband-diags-compat
%{_sbindir}/ibcheckerrs
%{_mandir}/man8/ibcheckerrs*
%{_sbindir}/ibchecknet
%{_mandir}/man8/ibchecknet*
%{_sbindir}/ibchecknode
%{_mandir}/man8/ibchecknode*
%{_sbindir}/ibcheckport
%{_mandir}/man8/ibcheckport.*
%{_sbindir}/ibcheckportwidth
%{_mandir}/man8/ibcheckportwidth*
%{_sbindir}/ibcheckportstate
%{_mandir}/man8/ibcheckportstate*
%{_sbindir}/ibcheckwidth
%{_mandir}/man8/ibcheckwidth*
%{_sbindir}/ibcheckstate
%{_mandir}/man8/ibcheckstate*
%{_sbindir}/ibcheckerrors
%{_mandir}/man8/ibcheckerrors*
%{_sbindir}/ibdatacounts
%{_mandir}/man8/ibdatacounts*
%{_sbindir}/ibdatacounters
%{_mandir}/man8/ibdatacounters*
%{_sbindir}/ibdiscover.pl
%{_mandir}/man8/ibdiscover*
%{_sbindir}/ibswportwatch.pl
%{_mandir}/man8/ibswportwatch*
%{_sbindir}/ibqueryerrors.pl
%{_sbindir}/iblinkinfo.pl
%{_sbindir}/ibprintca.pl
%{_mandir}/man8/ibprintca*
%{_sbindir}/ibprintswitch.pl
%{_mandir}/man8/ibprintswitch*
%{_sbindir}/ibprintrt.pl
%{_mandir}/man8/ibprintrt*
%{_sbindir}/set_nodedesc.sh

#======================================================================
%package -n	%{libibverbs}
Summary:	A library and drivers for direct userspace use of RDMA (InfiniBand/iWARP/RoCE) hardware
Provides:	%{_lib}cxgb3 = %{EVRD}
Provides:	%{_lib}cxgb4 = %{EVRD}
Provides:	%{_lib}hfi1 = %{EVRD}
Provides:	%{_lib}i40iw = %{EVRD}
Provides:	%{_lib}ipathverbs = %{EVRD}
Provides:	%{_lib}mlx4 = %{EVRD}
Provides:	%{_lib}mthca = %{EVRD}
Provides:	%{_lib}nes = %{EVRD}
Provides:	%{_lib}ocrdma = %{EVRD}
Provides:	%{_lib}rxe = %{EVRD}
Provides:	%{_lib}usnic_verbs = %{EVRD}

%description -n %{libibverbs}
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

Device-specific plug-in ibverbs userspace drivers are included:

- libcxgb3: Chelsio T3 iWARP HCA
- libcxgb4: Chelsio T4 iWARP HCA
- libhfi1: Intel Omni-Path HFI
- libhns: HiSilicon Hip06 SoC
- libi40iw: Intel Ethernet Connection X722 RDMA
- libipathverbs: QLogic InfiniPath HCA
- libmlx4: Mellanox ConnectX-3 InfiniBand HCA (except arm, s390)
- libmlx5: Mellanox Connect-IB/X-4+ InfiniBand HCA (except arm, s390, s390x)
- libmthca: Mellanox InfiniBand HCA
- libnes: NetEffect RNIC
- libocrdma: Emulex OneConnect RDMA/RoCE Device
- libqedr: QLogic QL4xxx RoCE HCA
- librxe: A software implementation of the RoCE protocol
- libvmw_pvrdma: VMware paravirtual RDMA device

%files -n %{libibverbs}
%dir %{_sysconfdir}/libibverbs.d
%dir %{_libdir}/libibverbs
%{_libdir}/libefa.so.*
%{_libdir}/libibverbs*.so.%{ibverbsmajor}*
%{_libdir}/libibverbs/*.so
%{_libdir}/libmlx5.so.*
%{_libdir}/libmlx4.so.*
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%doc %{_docdir}/%{name}-%{version}/libibverbs.md

#===================================================================

%package -n libibverbs-utils
Summary: Examples for the libibverbs library
#Requires: %{libibverbs} = %{EVRD}

%description -n libibverbs-utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%files -n libibverbs-utils
%{_bindir}/ibv_*
%{_mandir}/man1/ibv_*

#===================================================================

%package -n ibacm
Summary: InfiniBand Communication Manager Assistant
Requires: %{name} = %{EVRD}

%description -n ibacm
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ibacm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ibacm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ibacm daemon to retrieve data.

%files -n ibacm
%config(noreplace) %{_sysconfdir}/rdma/ibacm_opts.cfg
%{_bindir}/ib_acme
%{_sbindir}/ibacm
%{_mandir}/man1/ib_acme.*
%{_mandir}/man7/ibacm_prov.*
%{_mandir}/man7/ibacm*
%{_mandir}/man8/ibacm*
%{_unitdir}/ibacm.service
%{_unitdir}/ibacm.socket
%dir %{_libdir}/ibacm
%{_libdir}/ibacm/*
%doc %{_docdir}/%{name}-%{version}/ibacm.md

#===================================================================

%package -n iwpmd
Summary: iWarp Port Mapper userspace daemon
Requires: %{name} = %{EVRD}

%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim
tcp ports through the standard socket interface.

%files -n iwpmd
%{_sbindir}/iwpmd
%{_unitdir}/iwpmd.service
%config(noreplace) %{_sysconfdir}/rdma/modules/iwpmd.conf
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%{_udevrulesdir}/90-iwpmd.rules
%{_mandir}/man8/iwpmd.*
%{_mandir}/man5/iwpmd.*

#===================================================================
%package -n %{libibumad}
Summary: OpenFabrics Alliance InfiniBand umad (userspace management datagram) library
Requires: %{name} = %{EVRD}

%description -n %{libibumad}
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%files -n %{libibumad}
%{_libdir}/libibumad*.so.%{ibumadmajor}*

#===================================================================
%package -n %{libibnetdisc}
Summary: Userspace RDMA Connection Manager
Requires: %{name} = %{EVRD}

%description -n %{libibnetdisc}
librdmacm provides a userspace RDMA Communication Management API.

%files -n %{libibnetdisc}
%{_libdir}/libibnetdisc*.so.%{ibnetdiscmajor}*

#===================================================================
%package -n %{librdmacm}
Summary: Userspace RDMA Connection Manager
Requires: %{name} = %{EVRD}

%description -n %{librdmacm}
librdmacm provides a userspace RDMA Communication Management API.

%files -n %{librdmacm}
%{_libdir}/librdmacm*.so.%{rdmacmmajor}*
%dir %{_libdir}/rsocket
%{_libdir}/rsocket/*.so*
%doc %{_docdir}/%{name}-%{version}/librdmacm.md
%{_mandir}/man7/rsocket.*

#===================================================================

%package -n librdmacm-utils
Summary: Examples for the librdmacm library
Requires:	%{librdmacm}

%description -n librdmacm-utils
Example test programs for the librdmacm library.

%files -n librdmacm-utils
%{_bindir}/cmtime
%{_bindir}/mckey
%{_bindir}/rcopy
%{_bindir}/rdma_client
%{_bindir}/rdma_server
%{_bindir}/rdma_xclient
%{_bindir}/rdma_xserver
%{_bindir}/riostream
%{_bindir}/rping
%{_bindir}/rstream
%{_bindir}/ucmatose
%{_bindir}/udaddy
%{_bindir}/udpong
%{_mandir}/man1/cmtime.*
%{_mandir}/man1/mckey.*
%{_mandir}/man1/rcopy.*
%{_mandir}/man1/rdma_client.*
%{_mandir}/man1/rdma_server.*
%{_mandir}/man1/rdma_xclient.*
%{_mandir}/man1/rdma_xserver.*
%{_mandir}/man1/riostream.*
%{_mandir}/man1/rping.*
%{_mandir}/man1/rstream.*
%{_mandir}/man1/ucmatose.*
%{_mandir}/man1/udaddy.*
%{_mandir}/man1/udpong.*

#===================================================================

%package -n srp_daemon
Summary: Tools for using the InfiniBand SRP protocol devices
Obsoletes: srptools <= 1.0.3
Provides: srptools = %{EVRD}
Obsoletes: openib-srptools <= 0.0.6
Requires: %{name} = %{EVRD}

%description -n srp_daemon
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%files -n srp_daemon
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/srp_daemon.conf
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_unitdir}/srp_daemon.service
%{_unitdir}/srp_daemon_port@.service
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/run_srp_daemon
%{_udevrulesdir}/60-srp_daemon.rules
%{_mandir}/man8/srp_daemon.8*
%{_mandir}/man8/ibsrpdm.8*
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%doc %{_docdir}/%{name}-%{version}/ibsrpdm.md

#===================================================================
%package -n python-pyverbs
Summary: Python3 API over IB verbs
Provides: python3-verbs = %{EVRD}

BuildRequires: pkgconfig(python)
BuildRequires: python-cython
BuildRequires: python-docutils

%description -n python-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.

%files -n python-pyverbs
%{python_sitearch}/pyverbs
%{_docdir}/%{name}-%{version}/tests/*.py
#===================================================================
%prep
%autosetup -p1

%build
%define CMAKE_FLAGS -GNinja

%{!?EXTRA_CMAKE_FLAGS: %define EXTRA_CMAKE_FLAGS %{nil}}

# Pass all of the rpm paths directly to GNUInstallDirs and our other defines.
%cmake %{CMAKE_FLAGS} \
	-DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
        -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
        -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
        -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
        -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
        -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
        -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
        -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
        -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
        -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR:PATH=%{_unitdir} \
        -DCMAKE_INSTALL_INITDDIR:PATH=%{_initrddir} \
        -DCMAKE_INSTALL_RUNDIR:PATH=%{_rundir} \
        -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name}-%{version} \
        -DCMAKE_INSTALL_UDEV_RULESDIR:PATH=%{_udevrulesdir} \
	-DCMAKE_INSTALL_PERLDIR:PATH=%{perl_vendorlib} \
        -DENABLE_IBDIAGS_COMPAT:BOOL=True \
        -DPYTHON_EXECUTABLE:PATH=%{__python} \
        -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python_sitearch} \
        -DNO_PYVERBS=0 \
	%{EXTRA_CMAKE_FLAGS}

%ninja_build

%install
%ninja_install -C build

mkdir -p %{buildroot}/%{_sysconfdir}/rdma

# Red Hat specific glue
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/05rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m0644 redhat/rdma.conf %{buildroot}/%{_sysconfdir}/rdma/rdma.conf
install -D -m0644 redhat/rdma.sriov-vfs %{buildroot}/%{_sysconfdir}/rdma/sriov-vfs
install -D -m0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
install -D -m0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -D -m0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh
install -D -m0644 redhat/rdma.service %{buildroot}%{_unitdir}/rdma.service
install -D -m0755 redhat/rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -D -m0644 redhat/rdma.udev-rules %{buildroot}%{_udevrulesdir}/98-rdma.rules
install -D -m0755 redhat/rdma.kernel-init %{buildroot}%{_libexecdir}/rdma-init-kernel
install -D -m0755 redhat/rdma.sriov-init %{buildroot}%{_libexecdir}/rdma-set-sriov-vf

# ibacm
pushd build
LD_LIBRARY_PATH="$LD_LIBRARY_PATH:./lib" bin/ib_acme -D . -O
install -D -m0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/
popd

# Delete the package's init.d scripts
rm -rf %{buildroot}/%{_initrddir}/
rm -f %{buildroot}/%{_sbindir}/srp_daemon.sh

%post -n rdma-core
# we ship udev rules, so trigger an update.
/sbin/udevadm trigger --subsystem-match=infiniband --action=change || true
/sbin/udevadm trigger --subsystem-match=net --action=change || true
/sbin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true

%post -n ibacm
%systemd_post ibacm.service
%preun -n ibacm
%systemd_preun ibacm.service
%postun -n ibacm
%systemd_postun_with_restart ibacm.service

%post -n srp_daemon
%systemd_post srp_daemon.service
%preun -n srp_daemon
%systemd_preun srp_daemon.service
%postun -n srp_daemon
%systemd_postun_with_restart srp_daemon.service

%post -n iwpmd
%systemd_post iwpmd.service
%preun -n iwpmd
%systemd_preun iwpmd.service
%postun -n iwpmd
%systemd_postun_with_restart iwpmd.service


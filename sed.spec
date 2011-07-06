# -*- coding: utf-8 -*-
%ifos linux
%define _bindir /bin
%endif

Summary: A GNU stream text editor
Name: sed
Version: 4.2.1
Release: 5%{?dist}
License: GPLv2+
Group: Applications/Text
URL: http://sed.sourceforge.net/
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.bz2
Source1: http://sed.sourceforge.net/sedfaq.txt
Patch0: sed-4.2.1-copy.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-devel, libselinux-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch0 -p1

%build
%configure --without-included-regex
make %{_smp_mflags}
install -m 644 -p %{SOURCE1} sedfaq.txt
gzip -9 sedfaq.txt

%check
echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/sed.info.gz %{_infodir}/dir || &> /dev/null
:

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/sed.info.gz %{_infodir}/dir || &> /dev/null
fi
:

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS NEWS THANKS README AUTHORS sedfaq.txt.gz COPYING COPYING.DOC
%{_bindir}/sed
%{_infodir}/*.info*
%{_mandir}/man*/*

%changelog
* Mon Feb 22 2010 Jiri Moskovcak <jmoskovc@redhat.com> 4.2.1-5
- added back -c/--copy
- resolves: #566457

* Fri Oct 16 2009 Jiri Moskovcak <jmoskovc@redhat.com> 4.2.1-4
- added libselinux-devel to buildrequires rhbz#514182
- fixed problem with --excludedocs rhbz#515913

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.2.1-3
- Use bzipped upstream tarball.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009  Jiri Moskovcak <jmoskovc@redhat.com> - 4.2.1-1
- new version
- obsoletes previous patches
- added patch to maintain backwards compatibility for scripts using -c/--copy
- Resolves: #502934

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Jiri Moskovcak <jmoskovc@redhat.com> 4.1.5-11
- improved follow.patch (thanks to Arkadiusz Miskiewicz for initial patch)
- Resolves: #470912

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.5-10
- Autorebuild for GCC 4.3

* Thu Oct  4 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-9
- Fix licensing tag.
- Clean up per merge review comments.
- Resolves: #226404

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-8
- tidy up the specfile per rpmlint comments
- use utf-8 and fix national characters in contributor's names

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 4.1.5-7
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223716

* Fri Dec  8 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-6
- Split confused patches "copy+symlink" and "relsymlink" into discrete
  "copy" and "symlink".

* Mon Sep  4 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-5
- Fix handling of relative symlinks (#205122)

* Wed Aug  3 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-4
- remove superfluous multibyte processing in str_append for UTF-8
  encoding (thanks Paolo Bonzini, #177246)

* Mon Jul 17 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-3
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-2.2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.2
- typo in patch name

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2.1
- rebuild

* Thu Jun 29 2006 Petr Machata <pmachata@redhat.com> - 4.1.5-2
- #185374:
  - Follow symlinks before rename (avoid symlink overwrite)
  - Add -c flag for copy instead of rename (avoid ownership change)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Florian La Roche <laroche@redhat.com>
- 4.1.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 4.1.4-1
- update to 4.1.4

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 4.1.2-5
- rebuilt with GCC 4

* Fri Oct  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-4
- fix up make check to run sed --version with LC_ALL=C
  in the environment (#129014)

* Sat Oct  2 2004 Jakub Jelinek <jakub@redhat.com> 4.1.2-3
- add sedfaq.txt to %%{_docdir} (#16202)

* Mon Aug 23 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.2

* Thu Jul  8 2004 Jakub Jelinek <jakub@redhat.com> 4.1.1-1
- update to 4.1.1

* Mon Jun 21 2004 Jakub Jelinek <jakub@redhat.com> 4.1-1
- update to 4.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Jakub Jelinek <jakub@redhat.com> 4.0.9-1
- update to 4.0.9
- BuildRequire recent glibc and glibc-devel (#123043)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 4.0.8-3
- if not -n, print current buffer after N command on the last line
  unless POSIXLY_CORRECT (#112952)
- adjust XFAIL_TESTS for the improved glibc regex implementation
  (#112642)

* Fri Nov 14 2003 Jakub Jelinek <jakub@redhat.com> 4.0.8-2
- enable --without-included-regex again
- use fastmap for regex searching

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.8
- simplify specfile
- disable --without-included-regex to pass the testsuite

* Thu Jun 26 2003 Jakub Jelinek <jakub@redhat.com> 4.0.7-3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.7
- use "--without-included-regex"
- do not gzip info pages in spec file, "TODO" is not present anymore

* Thu Jan 23 2003 Jakub Jelinek <jakub@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Oct 22 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt to fix x86-64 miscompilation
- run make check in %%build

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com>
- Remove stale URLs from documentation (#62519)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Update to 2000.11.28 patch
- Rebuild for 7.1 tree

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

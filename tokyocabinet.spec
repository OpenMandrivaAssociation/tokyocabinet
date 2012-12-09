%define	major 9
%define libname	%mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Tokyo Cabinet: a modern implementation of DBM
Name:		tokyocabinet
Version:	1.4.47
Release:	%mkrel 4
Group:		System/Libraries
License:	LGPL
URL:		http://1978th.net/tokyocabinet/
Source0:	http://1978th.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		tokyocabinet-mdv_conf.diff
Patch1:		tokyocabinet-1.4.9-lzmalib_linkage_fix.diff
BuildRequires:	autoconf
BuildRequires:	bzip2-devel
BuildRequires:	liblzo-devel
BuildRequires:	lzmalib-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Tokyo Cabinet is a library of routines for managing a database. The database is
a simple data file containing records, each is a pair of a key and a value.
Every key and value is serial bytes with variable length. Both binary data and
character string can be used as a key and a value. There is neither concept of
data tables nor data types. Records are organized in hash table or B+ tree.

As for database of hash table, each key must be unique within a database, so it
is impossible to store two or more records with a key overlaps. The following
access methods are provided to the database: storing a record with a key and a
value, deleting a record by a key, retrieving a record by a key. Moreover,
traversal access to every key are provided, although the order is arbitrary.
These access methods are similar to ones of DBM (or its followers: NDBM and
GDBM) library defined in the UNIX standard. Tokyo Cabinet is an alternative for
DBM because of its higher performance.

As for database of B+ tree, records whose keys are duplicated can be stored.
Access methods of storing, deleting, and retrieving are provided as with the
database of hash table. Records are stored in order by a comparison function
assigned by a user. It is possible to access each record with the cursor in
ascending or descending order. According to this mechanism, forward matching
search for strings and range search for integers are realized. Moreover,
transaction is available in database of B+ tree.

Tokyo Cabinet is written in the C language, and provided as API of C, Perl,
Ruby, and Java. Tokyo Cabinet is available on platforms which have API
conforming to C99 and POSIX. Tokyo Cabinet is a free software licensed under
the GNU Lesser General Public License.

%package -n	%{libname}
Summary:	Tokyo Cabinet: a modern implementation of DBM
Group:          System/Libraries

%description -n	%{libname}
Tokyo Cabinet is a library of routines for managing a database. The database is
a simple data file containing records, each is a pair of a key and a value.
Every key and value is serial bytes with variable length. Both binary data and
character string can be used as a key and a value. There is neither concept of
data tables nor data types. Records are organized in hash table or B+ tree.

As for database of hash table, each key must be unique within a database, so it
is impossible to store two or more records with a key overlaps. The following
access methods are provided to the database: storing a record with a key and a
value, deleting a record by a key, retrieving a record by a key. Moreover,
traversal access to every key are provided, although the order is arbitrary.
These access methods are similar to ones of DBM (or its followers: NDBM and
GDBM) library defined in the UNIX standard. Tokyo Cabinet is an alternative for
DBM because of its higher performance.

As for database of B+ tree, records whose keys are duplicated can be stored.
Access methods of storing, deleting, and retrieving are provided as with the
database of hash table. Records are stored in order by a comparison function
assigned by a user. It is possible to access each record with the cursor in
ascending or descending order. According to this mechanism, forward matching
search for strings and range search for integers are realized. Moreover,
transaction is available in database of B+ tree.

Tokyo Cabinet is written in the C language, and provided as API of C, Perl,
Ruby, and Java. Tokyo Cabinet is available on platforms which have API
conforming to C99 and POSIX. Tokyo Cabinet is a free software licensed under
the GNU Lesser General Public License.

%package -n	%{develname}
Summary:	Static library and header files for the tokyocabinet library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname -d %{name} 1}

%description -n	%{develname}
Tokyo Cabinet is a library of routines for managing a database. The database is
a simple data file containing records, each is a pair of a key and a value.
Every key and value is serial bytes with variable length. Both binary data and
character string can be used as a key and a value. There is neither concept of
data tables nor data types. Records are organized in hash table or B+ tree.

As for database of hash table, each key must be unique within a database, so it
is impossible to store two or more records with a key overlaps. The following
access methods are provided to the database: storing a record with a key and a
value, deleting a record by a key, retrieving a record by a key. Moreover,
traversal access to every key are provided, although the order is arbitrary.
These access methods are similar to ones of DBM (or its followers: NDBM and
GDBM) library defined in the UNIX standard. Tokyo Cabinet is an alternative for
DBM because of its higher performance.

As for database of B+ tree, records whose keys are duplicated can be stored.
Access methods of storing, deleting, and retrieving are provided as with the
database of hash table. Records are stored in order by a comparison function
assigned by a user. It is possible to access each record with the cursor in
ascending or descending order. According to this mechanism, forward matching
search for strings and range search for integers are realized. Moreover,
transaction is available in database of B+ tree.

Tokyo Cabinet is written in the C language, and provided as API of C, Perl,
Ruby, and Java. Tokyo Cabinet is available on platforms which have API
conforming to C99 and POSIX. Tokyo Cabinet is a free software licensed under
the GNU Lesser General Public License.

This package contains the static library and its header files.


%package	tcawmgr
Summary:	The CGI utility of the abstract database API (tokyocabinet)
Group:		System/Servers
Requires:	%{libname} = %{version}
Requires:	apache

%description	tcawmgr
The CGI utility of the abstract database API (tokyocabinet).

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p0

%build
rm -f configure
autoconf

%configure2_5x \
    --enable-zlib \
    --enable-bzip \
    --enable-pthread \
    --enable-exlzma \
    --enable-exlzo

%make LDFLAGS="%{ldflags} -L. -L%{_libdir}"

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}/var/www/cgi-bin
mv %{buildroot}%{_libdir}/tcawmgr.cgi %{buildroot}/var/www/cgi-bin/

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf << EOF
<Location /cgi-bin/tcawmgr.cgi>
    Order Deny,Allow
    Deny from All
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf"
</Location>
EOF

# cleanup
rm -rf %{buildroot}%{_datadir}/%{name}
rm -f doc/*~

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post tcawmgr
%if %mdkversion < 201010
%_post_webapp
%endif

%postun tcawmgr
%if %mdkversion < 201010
%_postun_webapp
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING ChangeLog README doc/* lab/magic
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/tokyocabinet.pc
%{_mandir}/man3/*

%files tcawmgr
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf
%attr(0755,root,root) /var/www/cgi-bin/tcawmgr.cgi


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.47-2mdv2011.0
+ Revision: 670713
- mass rebuild

* Tue Feb 15 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.47-1
+ Revision: 637867
- 1.4.47

* Mon Aug 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.46-1mdv2011.0
+ Revision: 568101
- 1.4.46

* Tue Feb 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.42-2mdv2010.1
+ Revision: 510237
- rebuild
- not really unmaintained...

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - unmaintained webapp cleaning

* Sun Feb 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.42-1mdv2010.1
+ Revision: 505810
- 1.4.42

* Tue Jan 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.41-2mdv2010.1
+ Revision: 493875
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.41-1mdv2010.1
+ Revision: 480144
- 1.4.41

* Sun Nov 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.37-1mdv2010.1
+ Revision: 463123
- Update to new version 1.4.37
- Fix URL

* Wed Aug 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.31-1mdv2010.0
+ Revision: 418133
- 1.4.31

* Mon Jun 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.27-1mdv2010.0
+ Revision: 387955
- 1.4.27
- rediffed patches

* Sat May 30 2009 Frederik Himpe <fhimpe@mandriva.org> 1.4.23-1mdv2010.0
+ Revision: 381527
- update to new version 1.4.23

* Thu May 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.21-1mdv2010.0
+ Revision: 378437
- bump major
- 1.4.21
- rediff patches

* Sat Mar 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-1mdv2009.1
+ Revision: 351896
- 1.4.9
- rediffed P0
- added P1 to make it link against -llzmalib

* Tue Jan 20 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-1mdv2009.1
+ Revision: 331726
- 1.4.0
- rediffed P0

* Mon Nov 24 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.20-1mdv2009.1
+ Revision: 306339
- 1.3.20

* Thu Nov 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.18-1mdv2009.1
+ Revision: 302651
- 1.3.18
- rediffed P0

* Mon Oct 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.15-1mdv2009.1
+ Revision: 297549
- 1.3.15
- rediffed P0

* Thu Sep 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.7-1mdv2009.0
+ Revision: 280751
- 1.3.7

* Thu Aug 28 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.5-1mdv2009.0
+ Revision: 276863
- 1.3.5

* Thu Jul 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-1mdv2009.0
+ Revision: 258789
- 1.3.1

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-1mdv2009.0
+ Revision: 211345
- 1.2.6
- added the tcawmgr cgi and apache config

* Sun Apr 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-1mdv2009.0
+ Revision: 195935
- 1.2.4
- 1.2.3
- new major (3)

* Wed Jan 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.12-1mdv2008.1
+ Revision: 160312
- 1.1.12

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.11-1mdv2008.1
+ Revision: 156116
- 1.1.11

* Fri Jan 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.8-1mdv2008.1
+ Revision: 147927
- 1.1.8

* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-1mdv2008.1
+ Revision: 141830
- fix deps
- import tokyocabinet


* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-1mdv2008.1
- initial Mandriva package

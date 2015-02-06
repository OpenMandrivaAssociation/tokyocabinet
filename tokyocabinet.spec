%define debug_package %{nil}

%define	major	9
%define libname	%mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Tokyo Cabinet: a modern implementation of DBM
Name:		tokyocabinet
Version:	1.4.48
Release:	3
Group:		System/Libraries
License:	LGPL
Url:		http://fallabs.com/tokyocabinet/
Source0:	http://fallabs.com/tokyocabinet/%{name}-%{version}.tar.gz
Patch0:		tokyocabinet-mdv_conf.diff
Patch1:		tokyocabinet-1.4.9-lzmalib_linkage_fix.diff

BuildRequires:	bzip2-devel
BuildRequires:	lzo-devel
BuildRequires:	lzmalib-devel
BuildRequires:	pkgconfig(zlib)

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
This package contains the shared library for %{name}.

%package -n	%{devname}
Summary:	Development library and header files for the tokyocabinet library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n	%{devname}
This package contains the development library and its header files.

%package	tcawmgr
Summary:	The CGI utility of the abstract database API (tokyocabinet)
Group:		System/Servers
Requires:	apache

%description	tcawmgr
The CGI utility of the abstract database API (tokyocabinet).

%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
rm -f configure
autoconf

%configure2_5x \
	--disable-static \
	--enable-zlib \
	--enable-bzip \
	--enable-pthread \
	--enable-exlzma \
	--enable-exlzo

%make LDFLAGS="%{ldflags} -L. -L%{_libdir}"

%check
#make check

%install
%makeinstall_std

install -d %{buildroot}/var/www/cgi-bin
mv %{buildroot}%{_libexecdir}/tcawmgr.cgi %{buildroot}/var/www/cgi-bin/

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf << EOF
<Location /cgi-bin/tcawmgr.cgi>
    Require local granted
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf"
</Location>
EOF

# cleanup
rm -rf %{buildroot}%{_datadir}/%{name}
rm -f doc/*~
rm -f %{buildroot}%{_libdir}/*.a

%files
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc COPYING ChangeLog README doc/* lab/magic
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/tokyocabinet.pc
%{_mandir}/man3/*

%files tcawmgr
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/tcawmgr.conf
/var/www/cgi-bin/tcawmgr.cgi


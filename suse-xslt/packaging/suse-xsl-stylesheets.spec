#
# spec file for package suse-xsl-stylesheets
#
# Copyright (c) 2011, 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
#

Name:           suse-xsl-stylesheets
Version:        1.9

%define dtdversion     1.0
%define dtdname        novdoc
%define regcat         %{_bindir}/sgml-register-catalog
%define dbstyles       %{_datadir}/xml/docbook/stylesheet/nwalsh/current
%define novdoc_catalog for-catalog-%{dtdname}-%{dtdversion}.xml

Release:        1
Summary:        SUSE-branded Docbook stylesheets for XSLT 1.0
License:        GPL-2.0 or GPL-3.0
Group:          Productivity/Publishing/XML
URL:            http://sourceforge.net/p/daps/suse-xslt
Source0:        %{name}-%{version}.tar.bz2
Source1:        susexsl-fetch-source
Source2:        %{name}.rpmlintrc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

BuildRequires:  docbook-xsl-stylesheets >= 1.75
BuildRequires:  libxslt
BuildRequires:  make
BuildRequires:  trang 

Requires:       docbook
Requires:       docbook-xsl-stylesheets >= 1.75
Requires:       libxslt

Recommends:     daps
Recommends:     docbook5
Recommends:     docbook5-xsl-stylesheets

%description
SUSE-branded DocBook stylesheets for XSLT 1.0

Extensions for the DocBook XSLT 1.0 stylesheets that provide SUSE branding 
for PDF, HTML, and ePUB. This package also provides the NovDoc DTD, a subset of
the DocBook 4 DTD.

#--------------------------------------------------------------------------
%prep
%setup -q -n %{name}

#--------------------------------------------------------------------------
%build
%__make  %{?_smp_mflags}

#--------------------------------------------------------------------------
%install
make install DESTDIR=$RPM_BUILD_ROOT

#----------------------
%post
# register catalogs
#
# SGML CATALOG
#
if [ -x %{regcat} ]; then
  for CATALOG in catalog/CATALOG.%{dtdname}-%{dtdversion}; do
    %{regcat} -a %{_datadir}/sgml/$CATALOG >/dev/null 2>&1 || true
  done
fi
# XML Catalog
#
# remove existing entries first - needed for
# zypper in, since it does not call postun
# delete ...
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{dtdname}-%{dtdversion}
# ... and add it again
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{novdoc_catalog}

exit 0

#----------------------
%postun
#
# Remove catalog entries
#
# SGML
if [ ! -f %{_sysconfdir}/xml/%{novdoc_catalog} -a -x /usr/bin/edit-xml-catalog ] ; then
  for c in catalog/CATALOG.%{dtdname}-%{dtdversion}; do
    %{regcat} -r %{_datadir}/sgml/$c >/dev/null 2>&1
  done
# XML
  edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{dtdname}-%{dtdversion}
fi

exit 0


#----------------------
%files
%defattr(-,root,root)

# Directories
%dir %{_datadir}/xml/docbook/stylesheet/suse

%dir %{_datadir}/xml/%{dtdname}
%dir %{_datadir}/xml/%{dtdname}/schema
%dir %{_datadir}/xml/%{dtdname}/schema/*
%dir %{_datadir}/xml/%{dtdname}/schema/*/1.0

%dir %{_defaultdocdir}/%{name}

# stylesheets
%{_datadir}/xml/docbook/stylesheet/suse/*

# NovDoc Schemas
%{_datadir}/xml/%{dtdname}/schema/dtd/%{dtdversion}/*
%{_datadir}/xml/%{dtdname}/schema/rng/%{dtdversion}/*

# Catalogs
%config /var/lib/sgml/CATALOG.*
%{_datadir}/sgml/CATALOG.*
%config %{_sysconfdir}/xml/*.xml

# Documentation
%doc %{_defaultdocdir}/%{name}/*

#----------------------
%changelog

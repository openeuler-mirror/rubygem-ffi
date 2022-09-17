%global gem_name ffi
Name:                rubygem-%{gem_name}
Version:             1.10.0
Release:             4
Summary:             FFI Extensions for Ruby
License:             BSD
URL:                 https://www.github.com/ffi/ffi
Source0:             https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:             https://www.github.com/ffi/%{gem_name}/archive/%{version}.tar.gz
Patch0:              Remove-taint-support.patch
Patch1:              Add-riscv-typesconf.patch
BuildRequires:       ruby(release) rubygems-devel ruby-devel gcc libffi-devel rubygem(rspec)
%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%package doc
Summary:             Documentation for %{name}
Requires:            %{name} = %{version}-%{release}
BuildArch:           noarch
%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version} -b 1
ln -s %{gem_name}-%{version}/test test
ln -s %{gem_name}-%{version}/spec spec
%patch0 -p1
%patch1 -p1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install
cp -r ./lib/ffi/platform/riscv64-linux/ ./%{gem_instdir}/lib/ffi/platform/

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/%{gem_name}-%{version}/spec spec
pushd spec/ffi/fixtures
make JFLAGS="%{optflags}"
popd
rspec -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/LICENSE.SPECS
%exclude %{gem_instdir}/appveyor.yml
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%{gem_instdir}/ffi.gemspec

%changelog
* Wed Sep 14 2022 laokz <laokz@foxmail.com> - 1.10.0-4
- Pack lost riscv files of last commit

* Tues Mar 8 2022 zzzum <ovezjin@outlook.com> - 1.10.0-3
- Add riscv types conf

* Wed Jan 26 2022 liyanan <liyanan32@huawei.com> - 1.10.0-2
- Remove taint support

* Thu Aug 20 2020 xiezheng <xiezheng4@huawei.com> - 1.10.0-1
- package init

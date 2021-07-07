# Manage rpm files

```bash
rpm -qf /path/2/bin       # Query rpm from which this binary has been installed
rpm -qa | grep -i ${name} # Query all packages installed via rpm
rpm -qi ${package-name}   # Query information about this package
rpm -ql ${package-name}   # Query files included into this package
rpm -qip ${rpm}           # Query information about this local rpm file
rpm -qlp ${rpm}           # Query files included into this local rpm file
rpm -ivh ${rpm}           # Install a rpm
rpm -e ${package-name}    # Uninstall this package
```

# Build rpm from srpm (source rpm)

See:
- https://wiki.centos.org/HowTos/RebuildSRPM
- https://rpm-packaging-guide.github.io/
- https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/Packagers_Guide/ > §2.2. Creating a Basic Spec File && §A.5. Spec File Preamble
- https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ > §9. Working with Spec Files
- https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/

See examples at: [../applications/srpm/](../applications/srpm/).

```bash
# Environment
sudo yum install -y rpm-build # redhat-rpm-config (optional)
sudo yum install -y make gcc  # compiler

# Directories for rpm building
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
# Or: sudo yum install rpmdevtools -y && rpmdev-setuptree

# Extract previous rpm
rpm -i ${rpm}          # as the unpriviledge user (not as root)
ls ~/rpmbuild/SPECS/   # The spec file from which the rpm has been built
ls ~/rpmbuild/SOURCES/ # The files included into this rpm

# Rebuild the rpm
cd ~/rpmbuild/SPECS/
vi ${spec}             # Change the spec file
rpmbuild -ba ${spec}   # Rebuild the rpm from this new spec file
ls ~/rpmbuild/BUILD/   # Used to build

# Result
ls ~/rpmbuild/SRPMS/   # Result source rpm files
ls ~/rpmbuild/RPMS/    # Result rpm files
rpm -qlp ${rpm}        # List rpm content
sudo rpm -ivh ${rpm}   # Install rpm
```

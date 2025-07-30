<div align="center">
  <img src="assets/media/choppr_the_crocodile.svg?ref_type=heads" width="500"/>
</div>

# Choppr

A Hoppr plugin to filter unused components out of the delivered SBOM using strace results.

Choppr refines the components in a
[Software Bill of Materials (SBOM)](https://en.wikipedia.org/wiki/Software_supply_chain). It does not replace SBOM
generation tools. Mainly, Choppr analyses a build or runtime to verify which components are used, and remove the SBOM
components not used. Starting with file accesses, it works backwards from how an SBOM generation tool typically would.
For example SBOM generators use the yum database to determine which packages yum installed. Choppr looks at all the
files accessed and queries sources like yum to determine the originating package.

Other intended results include:
- Reducing installed components. Size is optimized. The number of vulnerabilities is reduced. The less tools available
  to an attacker the better.
- Creating a runtime container from the build container
- Detecting files without corresponding SBOM components

# Configuration

## manifest.yml
You must list the RPM repositories used on your system in the
[`manifest.yml`](https://hoppr.dev/docs/using-hoppr/input-files/manifest) file, for example:

```yml
repositories:
  rpm:
    - url: http://mirrorlist.rockylinux.org/?arch=x86_64&repo=BaseOS-8
    - url: http://mirrorlist.rockylinux.org/?arch=x86_64&repo=AppStream-8
    - url: https://mirrors.rockylinux.org/powertools/rocky/8/
    - url: https://mirrors.rockylinux.org/extra/rocky/8/
    - url: https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
```

To obtain this list, use the following command:

```bash
# For RHEL 8 and later
dnf repolist --verbose

# For RHEL 7 and earlier
yum repolist --verbose
```

With the output from one of these commands, you should be able to find the URLs to the repositories used on your system.

## transfer.yml
You must add choppr as a plugin and configure it in the
[`transfer.yml`](https://hoppr.dev/docs/using-hoppr/input-files/transfer) file, for example:

```yml
Filter:
  plugins:
    - name: choppr.plugin
    config:
      strace_results: strace_output.txt
      certificates:
        - url: my.privaterepo.com
          certificate: /certs/combined.pem
      strace_regex_excludes:
        - ^.*<project-name>.*$
        - ^.*\.(c|cpp|cxx|h|hpp|o|py|s)$
        - ^/usr/share/pkgconfig$
        - ^/tmp$
        - ^bin$
        - ^.*\.git.*$
        - ^.*(\.\.)+.*$
        - ^.*(CMakeFiles.*|\.cmake)$
```

## Required Configuration Variables

### strace_results

The path to the output file created when running strace on your build or runtime executable.

This file can be creating using the following command to wrap your build script or runtime executable. The `strace` tool
must be installed on your system separately from choppr.

```sh
strace -f -e trace=file -o "strace_output.txt" <build script/runtime executable>
```

**Type:** str

**Example Usage:**
```yml
strace_results: strace_output.txt
```

## Optional Configuration Variables

### allow_version_mismatch

Allow version numbers to be mismatched when comparing SBOM packages to remote repository packages.

**Default:** false

**Type:** bool

**Example Usage:**
```yml
allow_version_mismatch: true
```

### allowlist

A dictionary with packages to always keep in the SBOM.

The keys are purl types, and the values are a list of packages. A package has two members, name and version, both are
regex patterns.

**Default:** {}

**Type:**
```yml
allowlist: # dict[PurlType, list[PackagePattern]]
  _purl_type_: # str (deb, npm, rpm, ...)
    - name: regex
      version: regex
    ...
  ...
```

**Example Usage:**
```yml
allowlist:
  deb:
    - name: ".*"
      version: ".*"
  generic:
    - name: "^python$"
      version: "^3.10"
```

### cache_dir

The path for the cache directory where Choppr will output temporary and downloaded files.

**Default:** ./.cache/choppr

**Type:** str

**Example Usage:**
```yml
cache_dir: /tmp/choppr
```

### cache_timeout

The timeout for local cache files, like DEB packages, that aren't traced to a checksum, like RPM packages.

Expects a number followed by a unit (d = days, h = hours, m = minutes, s = seconds).

**Default:** 7d

**Type:** str

**Example Usage:**
```yml
cache_timeout: 24h
```

### certificates

A list of objects with a url and certificate key that is used to access the provided url when a self signed certificate
needs to be used.

**Default:** []

**Type:** list[dict[str, str]]

**Example Usage:**
```yml
certificates:
  - url: my.privaterepo.com
    certificate: /certs/combined.pem
  - ...
```

### clear_cache

Enable `clear_cache` to delete the cache directory when Choppr finishes running.

**Default:** false

**Type:** bool

**Example Usage:**
```yml
clear_cache: true
```

### deb_repositories

A list of DEB repositories with the URL, distributions, and components to include.

**Default:** []

**Type:** list[DebianRepository]

**Example Usage:**
```yml
deb_repositories:
  - url: http://archive.ubuntu.com/ubuntu/
    distributions:
      - name: jammy
        components:
          - main
          - restricted
          - universe
          - multiverse
  - ...
```

### delete_excluded

Disable `delete_excluded` to keep RPMs that are discovered to be unnecessary and marked as excluded.

**Default:** true

**Type:** bool

**Example Usage:**
```yml
delete_excluded: false
```

### denylist

A dictionary with packages to always remove from the SBOM.

The keys are purl types, and the values are a list of packages. A package has two members, name and version, both are
regex patterns.

**Default:** {}

**Type:**
```yml
denylist: # dict[PurlType, list[PackagePattern]]
  _purl_type_: # str (deb, npm, rpm, ...)
    - name: regex
      version: regex
    ...
  ...
```

**Example Usage:**
```yml
denylist:
  deb:
    - name: "cmake"
      version: "3.22"
  npm:
    - name: ".*"
      version: ".*"
```

### http_limits

Limits to enforce when performing HTTP requests within Choppr.

- `retries` - The number of times to retry the request if it fails
- `retry_interval` - The number of seconds to wait before retrying the request
- `timeout` - The number of seconds to wait for a request to complete before timing out

**Default:**
```yml
retries: 3
retry_interval: 5
timeout: 60
```

**Type:**
```yml
retries: PositiveInt
retry_interval: PositiveFloat
timeout: PositiveFloat
```

**Example Usage:**
```yml
http_limits:
  retries: 10
  retry_interval: 30
  timeout: 300
```

### keep_essential_os_components

Keep components that are essential to the operating system, to include the operating system component.

**Default:** false

**Type:** bool

**Example Usage:**
```yml
keep_essential_os_components: true
```

### output_files

Specify the paths for output files.

**Defaults:**
```json
excluded_components = {
  "<purl_type>": {
    "file": "choppr_excluded_components_<purl_type>.txt",
    "component_format": "<excluded_component_format>"
  },
  ...
}
```

For `excluded_component_format` the default value is `{name}={version}` except for NPM, and RPM. Those are as follows:
```yml
NPM: "{name}@{version}"
RPM: "{name}-{version}"
```

**Type:**
```yml
output_files:
  excluded_components: # dict[PurlType, ExcludedPackageFile]
    _purl_type_: # str (deb, npm, rpm, ...)
      file: Path
      component_format: str # optional
    ...
```

**Example Usage:**
```yml
output_files:
  excluded_components:
    generic:
      file: output/excluded_generic.csv
      component_format: "{name},{version}"
    npm:
      file: output/excluded_npm.txt
    rpm:
      file: output/excluded_rpm.txt
```

### recursion_limit

A positive integer that will limit the number of recursive calls to use when checking for nested package dependencies.

**Default:** 10

**Type:** PositiveInt

**Example Usage:**
```yml
recursion_limit: 20
```

### strace_regex_excludes

An array of regex strings, used to filter the strace input. The example below shows some of the recommended regular
expressions.

**Default:** []

**Type:** list[str]

**Example Usage:**
```yml
strace_regex_excludes:
  - "^.*project-name.*$"              # Ignore all files containing the project name to exclude source files
  - "^.*\.(c|cpp|cxx|h|hpp|o|py|s)$"  # Ignore source, header, object, and script files
  - "^/usr/share/pkgconfig$"          # Ignore pkgconfig, which is included/modified by several RPMs
  - "^/tmp$"                          # Ignore the tmp directory
  - "^bin$"                           # Ignore overly simple files, that will be matched by most RPMs
  - "^.*\.git.*$"                     # Ignore all hidden git directories and files
  - "^.*(\.\.)+.*$"                   # Ignore all relative paths containing '..'
  - "^.*(CMakeFiles.*|\.cmake)$"      # Ignore all CMake files
```

# Generating strace

# Approaches

How to use Choppr depends on your project and needs. Consider the following use cases and their recommended approaches.
Note, this references
[CISA defined SBOM types](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).


## Build SBOM of software product

The user provides the required content. Choppr determines which comoponents were used during the build. The exclude
list tells Choppr to remove components like CMake, because the user is certain no CMake software was built into their
product. An uninstall script is generated. Building again after removing these components verifies no required
components were lost.

## Create runtime image and Runtime SBOM from build image

Choppr uses a multistage build to `ADD` the files used. Optionally metadata such as the yum database can be kept. The
additional include list can be used to specify dynamically linked libraries, necessary services, or any other necessary
components that were not exercised during build. This will also be reflected in the SBOM components.

## Create Runtime SBOM from runtime image

Similar to analyzing a build, Choppr can analyze a runtime. Note, to if this is used to describe a delivery, it should
be merged with the Build SBOM.

# Specificaitons

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [Conventional Branch](https://conventional-branch.github.io/)
- [PEP 440 - Version Identification and Dependency Specification](https://peps.python.org/pep-0440/)
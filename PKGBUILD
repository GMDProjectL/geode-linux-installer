pkgname=geode-linux-installer
pkgver=1.0
pkgrel=1
pkgdesc="Geode Linux Installer"
arch=('any')
url="https://github.com/GMDProjectL/geode-linux-installer"
license=('MIT')
depends=('python-requests' 'pyside6')
makedepends=()
checkdepends=()
optdepends=()
backup=()
options=()
install=
source=(${pkgname}::"git+file://${PWD}")

package() {
    cd "$srcdir"
    export UPDATER_DIST="${pkgdir}/opt/geode-linux-installer"

    # Create directory structure
    mkdir -p "${UPDATER_DIST}/src"
    mkdir -p "${UPDATER_DIST}/locale"
    mkdir -p "${UPDATER_DIST}/assets/swelve"
    mkdir -p "${pkgdir}/usr/bin"
    mkdir -p "${pkgdir}/usr/share/applications"

    # Install Python source files
    install -Dm644 "$srcdir/${pkgname}/src"/*.py -t "${UPDATER_DIST}/src/"
    
    # Install localization files
    install -Dm644 "$srcdir/${pkgname}/locale"/*.json -t "${UPDATER_DIST}/locale/"
    
    # Install assets
    install -Dm644 "$srcdir/${pkgname}/assets"/*.png -t "${UPDATER_DIST}/assets/"
    install -Dm644 "$srcdir/${pkgname}/assets/swelve"/*.png -t "${UPDATER_DIST}/assets/swelve/"
    
    # Install desktop file
    install -Dm644 "$srcdir/${pkgname}/geode-linux-installer.desktop" -t "${pkgdir}/usr/share/applications/"
    
    # Create executable wrapper script
    cat > "${pkgdir}/usr/bin/${pkgname}" << 'EOF'
#!/bin/bash
cd /opt/geode-linux-installer
python src/main.py "$@"
EOF
    chmod +x "${pkgdir}/usr/bin/${pkgname}"
}
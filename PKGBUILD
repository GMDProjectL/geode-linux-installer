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

    mkdir -p "${UPDATER_DIST}"

    install -Dm0644 $srcdir/${pkgname}/src/*.py -t ${UPDATER_DIST}/src/
    install -Dm0644 $srcdir/${pkgname}/locale/*.json -t ${UPDATER_DIST}/locale/
    install -Dm0644 $srcdir/${pkgname}/assets/ -t ${UPDATER_DIST}
    
    install -Dm0644 $srcdir/${pkgname}/assets/geode-linux-installer.desktop -t "${pkgdir}/usr/share/applications"
}
#!/usr/bin/env bash
set -euo pipefail
npm ci
npm test -- --coverage
npm run build
PKG_FILE=$(npm pack --silent)
mkdir -p ../dist
mv "${PKG_FILE}" "../dist/typescript-app-${npm_package_version}.tgz"
echo "Created ../dist/typescript-app-${npm_package_version}.tgz"

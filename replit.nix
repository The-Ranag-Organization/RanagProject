{pkgs}: {
  deps = [
    pkgs.wineWow64Packages.full
    pkgs.python312Packages.django
  ];
}

{pkgs}: {
  deps = [
    pkgs.python312Packages.huggingface-hub
    pkgs.wineWow64Packages.full
    pkgs.python312Packages.django
  ];
}

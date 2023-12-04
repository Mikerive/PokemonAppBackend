{ pkgs }: {
  deps = [
    pkgs.unixtools.ifconfig
    pkgs.mkinitcpio-nfs-utils
  ];
}
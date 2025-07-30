{ pkgs ? import <nixpkgs> {} }:
with import <nixpkgs> {};

let
  baseconfig = { allowUnfree = true; };
  unstable = import <nixos-unstable> { config =  baseconfig; };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    unstable.uv
    unstable.python312
    stdenv.cc.cc.lib
    zlib
    # Additional libraries for building C extensions
    openssl
    glib
    libffi
    ncurses
    # Development tools
    gcc
    gnumake
    pkg-config
  ];
  shellHook = ''
    export LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib:${zlib}/lib:${openssl.out}/lib:${pkgs.libffi}/lib:${ncurses}/lib:$LD_LIBRARY_PATH
    export UV_PYTHON=${pkgs.python312}
    uv venv
  '';
}

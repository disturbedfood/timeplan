  let
    pkgs = import <nixpkgs> {};
  in
  { stdenv ? pkgs.stdenv, python27Full ? pkgs.python27Full, python27Packages ? pkgs.python27Packages }:
  
  stdenv.mkDerivation {
    name = "python-nix";
    version = "0.1.0.0";
    shellHook = ''
	export PS1="\u timeplan-dev > "	
'';
    src = ./.;
    buildInputs=[ python27Full
		  python27Packages.requests
		  python27Packages.beautifulsoup4
		  python27Packages.dateutil
		  python27Packages.lxml
	 ];
  }


{ lib, python3Packages, pkgs }:
python3Packages.buildPythonApplication {
  pname = "modemtx";
  version = "0.1";

  propagatedBuildInputs = [ python3Packages.requests pkgs.minimodem ];

  src = ./.;
}

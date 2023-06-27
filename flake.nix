{
  description = "PythonEDA's nix-flakes domain";

  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
    pythoneda-base = {
      url = "github:pythoneda/base/0.0.1a15";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
    };
    pythoneda-event-nix-flakes = {
      url = "github:pythoneda-event/nix-flakes/0.0.1a1";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pythoneda-base.follows = "pythoneda-base";
    };
    pythoneda-shared-git = {
      url = "github:pythoneda-shared/git/0.0.1a2";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pythoneda-base.follows = "pythoneda-base";
    };
    pythoneda-shared-nix = {
      url = "github:pythoneda-shared/nix/0.0.1a4";
      inputs.nixos.follows = "nixos";
      inputs.flake-utils.follows = "flake-utils";
      inputs.pythoneda-base.follows = "pythoneda-base";
    };
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        description = "PythonEDA's nix-flakes domain";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda/nix-flakes";
        maintainers = with pkgs.lib.maintainers; [ ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/devShells.nix;
        pythoneda-nix-flakes-for = { version, pythoneda-base
          , pythoneda-shared-git, pythoneda-event-nix-flakes
          , pythoneda-shared-nix, python }:
          let
            pname = "pythoneda-nix-flakes";
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            src = ./.;
            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip pkgs.jq poetry-core ];
            propagatedBuildInputs = with python.pkgs; [
              pythoneda-base
              pythoneda-event-nix-flakes
              pythoneda-shared-git
              pythoneda-shared-nix
            ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ "pythonedagitpython" ];

            preBuild = ''
              python -m venv .env
              source .env/bin/activate
              pip install ${pythoneda-base}/dist/pythoneda_base-${pythoneda-base.version}-py3-none-any.whl
              pip install ${pythoneda-event-nix-flakes}/dist/pythoneda_event_nix_flakes-${pythoneda-event-nix-flakes.version}-py3-none-any.whl
              pip install ${pythoneda-shared-git}/dist/pythoneda_shared_git-${pythoneda-shared-git.version}-py3-none-any.whl
              pip install ${pythoneda-shared-nix}/dist/pythoneda_shared_nix-${pythoneda-shared-nix.version}-py3-none-any.whl
              rm -rf .env
            '';

            postInstall = ''
              mkdir $out/dist
              cp dist/${wheelName} $out/dist
              jq ".url = \"$out/dist/${wheelName}\"" $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json > temp.json && mv temp.json $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json
            '';

            meta = with pkgs.lib; {
              inherit description license homepage maintainers;
            };
          };
        pythoneda-nix-flakes-0_0_1a3-for = { pythoneda-base
          , pythoneda-shared-git, pythoneda-event-nix-flakes
          , pythoneda-shared-nix, python }:
          pythoneda-nix-flakes-for {
            version = "0.0.1a3";
            inherit pythoneda-base pythoneda-shared-git
              pythoneda-event-nix-flakes pythoneda-shared-nix python;
          };
      in rec {
        packages = rec {
          pythoneda-nix-flakes-0_0_1a3-python38 =
            pythoneda-nix-flakes-0_0_1a3-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python38;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python38;
              pythoneda-event-nix-flakes =
                pythoneda-event-nix-flakes.packages.${system}.pythoneda-event-nix-flakes-latest-python38;
              pythoneda-shared-nix =
                pythoneda-shared-nix.packages.${system}.pythoneda-shared-nix-latest-python38;
              python = pkgs.python38;
            };
          pythoneda-nix-flakes-0_0_1a3-python39 =
            pythoneda-nix-flakes-0_0_1a3-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python39;
              pythoneda-event-nix-flakes =
                pythoneda-event-nix-flakes.packages.${system}.pythoneda-event-nix-flakes-latest-python39;
              pythoneda-shared-nix =
                pythoneda-shared-nix.packages.${system}.pythoneda-shared-nix-latest-python39;
              python = pkgs.python39;
            };
          pythoneda-nix-flakes-0_0_1a3-python310 =
            pythoneda-nix-flakes-0_0_1a3-for {
              pythoneda-base =
                pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
              pythoneda-shared-git =
                pythoneda-shared-git.packages.${system}.pythoneda-shared-git-latest-python310;
              pythoneda-event-nix-flakes =
                pythoneda-event-nix-flakes.packages.${system}.pythoneda-event-nix-flakes-latest-python310;
              pythoneda-shared-nix =
                pythoneda-shared-nix.packages.${system}.pythoneda-shared-nix-latest-python310;
              python = pkgs.python310;
            };
          pythoneda-nix-flakes-latest-python38 =
            pythoneda-nix-flakes-0_0_1a3-python38;
          pythoneda-nix-flakes-latest-python39 =
            pythoneda-nix-flakes-0_0_1a3-python39;
          pythoneda-nix-flakes-latest-python310 =
            pythoneda-nix-flakes-0_0_1a3-python310;
          pythoneda-nix-flakes-latest = pythoneda-nix-flakes-latest-python310;
          default = packages.pythoneda-nix-flakes-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-nix-flakes-0_0_1a3-python38 = shared.devShell-for {
            package = packages.pythoneda-nix-flakes-0_0_1a3-python38;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python38;
            python = pkgs.python38;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-nix-flakes-0_0_1a3-python39 = shared.devShell-for {
            package = packages.pythoneda-nix-flakes-0_0_1a3-python39;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python39;
            python = pkgs.python39;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-nix-flakes-0_0_1a3-python310 = shared.devShell-for {
            package = packages.pythoneda-nix-flakes-0_0_1a3-python310;
            pythoneda-base =
              pythoneda-base.packages.${system}.pythoneda-base-latest-python310;
            python = pkgs.python310;
            inherit pkgs nixpkgsRelease;
          };
          pythoneda-nix-flakes-latest-python38 =
            pythoneda-nix-flakes-0_0_1a3-python38;
          pythoneda-nix-flakes-latest-python39 =
            pythoneda-nix-flakes-0_0_1a3-python39;
          pythoneda-nix-flakes-latest-python310 =
            pythoneda-nix-flakes-0_0_1a3-python310;
          pythoneda-nix-flakes-latest = pythoneda-nix-flakes-latest-python310;
          default = pythoneda-nix-flakes-latest;
        };
      });
}

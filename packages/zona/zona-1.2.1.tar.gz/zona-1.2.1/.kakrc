# commands to edit important files in the root
declare-option str project_root %sh{ git rev-parse --show-toplevel }

define-command -params 1 root-edit %{
    edit %exp{%opt{project_root}/%arg{1}}
}

define-command just %{
    root-edit justfile
}
define-command pyproject %{
    root-edit pyproject.toml
}
define-command readme %{
    root-edit README.md
}

define-command kakrc %{
    root-edit .kakrc
}

# change working directory to the package
hook global -once BufCreate .* %{
    change-directory %exp{%opt{project_root}/src/zona}
}

#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

function gen_stub()
{
    local dir=$1
    # Vérifie si le dossier est 'config' ou contient 'config/'
    if [[ "${dir}" == *"/config"* ]]; then
        return
    fi
    
    local stub_path=$1/__init__.py
    if [[ "${1##*/}" != "__pycache__" && ! -e $stub_path ]]
    then
        echo "Creating $stub_path..."
        cat > "$stub_path" <<'STUB'
#!/usr/bin/env python3
"""Package stub."""
STUB
    fi
}

export -f gen_stub
cd -- "$DIR"

# Exclut explicitement le dossier config
find src/tanat-cli-preset -type d -not -path "*/config*" -exec bash -c 'gen_stub "$0"' {} \;
#!/usr/bin/env python3
"""
Configura equipos y Push Rulesets para Robotica_2026_II usando GitHub CLI.

Requisitos:
  1. Tener GitHub CLI (`gh`) instalado.
  2. Ejecutar `gh auth login`.
  3. Tener permisos de administrador sobre el repositorio y permisos para gestionar equipos.
  4. Completar los usuarios GitHub de los profesores en access_control.json.
  5. Completar los usuarios GitHub faltantes de estudiantes si se desea darles acceso inmediato.

Uso:
  python3 github_admin/setup_access_control.py
      -> solo muestra y valida el plan.

  python3 github_admin/setup_access_control.py --apply
      -> crea/actualiza Teams y Rulesets.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "github_admin" / "access_control.json"

def run(cmd, input_json=None, allow_fail=False):
    inp = None if input_json is None else json.dumps(input_json)
    p = subprocess.run(
        cmd,
        input=inp,
        text=True,
        capture_output=True
    )
    if p.returncode != 0 and not allow_fail:
        print("\nERROR ejecutando:", " ".join(cmd))
        print(p.stderr.strip())
        sys.exit(p.returncode)
    return p

def gh_api(method, endpoint, payload=None, allow_fail=False):
    cmd = ["gh", "api", "--method", method, endpoint]
    if payload is not None:
        cmd += ["--input", "-"]
    p = run(cmd, payload, allow_fail=allow_fail)
    if p.returncode != 0:
        return None
    text = p.stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}

def require_gh():
    if not shutil.which("gh"):
        print("ERROR: GitHub CLI no está instalado.")
        print("Instálalo y luego ejecuta: gh auth login")
        sys.exit(1)

    p = run(["gh", "auth", "status"], allow_fail=True)
    if p.returncode != 0:
        print("ERROR: GitHub CLI no está autenticado.")
        print("Ejecuta: gh auth login")
        sys.exit(1)

def team_get(org, slug):
    return gh_api("GET", f"/orgs/{org}/teams/{slug}", allow_fail=True)

def team_create(org, slug, description):
    body = {
        "name": slug,
        "description": description,
        "privacy": "closed"
    }
    return gh_api("POST", f"/orgs/{org}/teams", body)

def ensure_team(org, slug, description):
    team = team_get(org, slug)
    if team and team.get("id"):
        print(f"  ✓ Team existente: {slug}")
        return team
    print(f"  + Creando team: {slug}")
    return team_create(org, slug, description)

def grant_repo(org, repo, slug, permission="push"):
    gh_api(
        "PUT",
        f"/orgs/{org}/teams/{slug}/repos/{org}/{repo}",
        {"permission": permission}
    )
    print(f"    ✓ Permiso {permission}: {slug}")

def add_member(org, slug, username):
    gh_api(
        "PUT",
        f"/orgs/{org}/teams/{slug}/memberships/{username}",
        {"role": "member"}
    )
    print(f"    ✓ Miembro: @{username}")

def existing_rulesets(org, repo):
    data = gh_api("GET", f"/repos/{org}/{repo}/rulesets?includes_parents=false")
    return data if isinstance(data, list) else []

def upsert_ruleset(org, repo, payload):
    existing = {r.get("name"): r for r in existing_rulesets(org, repo)}
    old = existing.get(payload["name"])
    if old:
        rid = old["id"]
        print(f"  ↻ Actualizando ruleset: {payload['name']}")
        return gh_api("PUT", f"/repos/{org}/{repo}/rulesets/{rid}", payload)
    print(f"  + Creando ruleset: {payload['name']}")
    return gh_api("POST", f"/repos/{org}/{repo}/rulesets", payload)

def make_push_ruleset(name, protected_paths, bypass_team_ids):
    return {
        "name": name,
        "target": "push",
        "enforcement": "active",
        "bypass_actors": [
            {
                "actor_id": int(team_id),
                "actor_type": "Team",
                "bypass_mode": "always"
            }
            for team_id in bypass_team_ids
        ],
        "rules": [
            {
                "type": "file_path_restriction",
                "parameters": {
                    "restricted_file_paths": protected_paths
                }
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica cambios reales en GitHub. Sin esta opción solo valida y muestra el plan."
    )
    parser.add_argument(
        "--allow-missing-users",
        action="store_true",
        help="Permite aplicar aunque haya estudiantes sin usuario GitHub."
    )
    args = parser.parse_args()

    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    org = cfg["organization"]
    repo = cfg["repository"]

    professors = cfg.get("professors", [])
    professor_users = [
        p.get("github", "").strip()
        for p in professors
        if p.get("github", "").strip()
        and not p.get("github", "").startswith("REEMPLAZAR_")
    ]

    if len(professor_users) != len(professors):
        print("FALTA CONFIGURAR LOS USUARIOS GITHUB DE LOS PROFESORES.")
        print("Edita github_admin/access_control.json antes de ejecutar --apply.")
        if args.apply:
            sys.exit(2)

    missing = []
    for section_name in ("lab_groups", "project_teams"):
        for key, team in cfg[section_name].items():
            for member in team.get("members", []):
                if not member.get("github"):
                    missing.append((section_name, key, member["name"], member["email"]))

    print("\n=== PLAN DE CONTROL DE ACCESO ===")
    print(f"Organización: {org}")
    print(f"Repositorio:   {repo}")
    print(f"Profesores:   {len(professor_users)} configurados")
    print(f"Grupos lab:   {len(cfg['lab_groups'])}")
    print(f"Equipos final:{len(cfg['project_teams'])}")
    print(f"Usuarios GitHub pendientes: {len(missing)}")

    if missing:
        print("\nUsuarios pendientes:")
        for section, key, name, email in missing:
            print(f"  - {section} {key}: {name} <{email}>")
        if args.apply and not args.allow_missing_users:
            print("\nNo se aplicaron cambios.")
            print("Completa los usuarios o usa --allow-missing-users.")
            sys.exit(3)

    if not args.apply:
        print("\nModo validación: no se hizo ningún cambio en GitHub.")
        print("Cuando esté listo:")
        print("  python3 github_admin/setup_access_control.py --apply")
        return

    require_gh()

    # 1) Professors team
    print("\n[1/4] Equipo de profesores")
    prof_team = ensure_team(
        org,
        "profesores",
        "Profesores del curso Robótica 2026-II"
    )
    prof_id = prof_team["id"]
    grant_repo(org, repo, "profesores", "admin")
    for username in professor_users:
        add_member(org, "profesores", username)

    # 2) Student teams
    team_ids = {}

    print("\n[2/4] Teams de laboratorio")
    for group, data in cfg["lab_groups"].items():
        slug = data["team_slug"]
        team = ensure_team(org, slug, f"Grupo de laboratorio {group} - Robótica 2026-II")
        team_ids[slug] = team["id"]
        grant_repo(org, repo, slug, "push")
        for m in data["members"]:
            if m.get("github"):
                add_member(org, slug, m["github"])

    print("\n[3/4] Teams de proyecto final")
    for number, data in cfg["project_teams"].items():
        slug = data["team_slug"]
        team = ensure_team(org, slug, f"Proyecto Final Equipo {number} - Robótica 2026-II")
        team_ids[slug] = team["id"]
        grant_repo(org, repo, slug, "push")
        for m in data["members"]:
            if m.get("github"):
                add_member(org, slug, m["github"])

    # 3) Push rulesets
    print("\n[4/4] Push Rulesets")

    # Professor-controlled files
    professor_paths = [
        "Profesor/**/*",
        "docs/**/*",
        ".github/**/*",
        "github_admin/**/*",
        "README.md",
        "Estudiantes/README.md",
        "Proyecto_Final/README.md",
        "CONTRIBUTING.md",
        "MANIFEST.md",
        "manifest.json",
        "LICENSE",
        "ESTRUCTURA.txt"
    ]
    upsert_ruleset(
        org,
        repo,
        make_push_ruleset(
            "ACL 2026-II - Archivos de profesores",
            professor_paths,
            [prof_id]
        )
    )

    for group, data in cfg["lab_groups"].items():
        slug = data["team_slug"]
        upsert_ruleset(
            org,
            repo,
            make_push_ruleset(
                f"ACL 2026-II - Lab {group}",
                data["protected_paths"],
                [prof_id, team_ids[slug]]
            )
        )

    for number, data in cfg["project_teams"].items():
        slug = data["team_slug"]
        upsert_ruleset(
            org,
            repo,
            make_push_ruleset(
                f"ACL 2026-II - Proyecto {int(number):02d}",
                data["protected_paths"],
                [prof_id, team_ids[slug]]
            )
        )

    print("\n✅ Configuración terminada.")
    print("Verifica en GitHub:")
    print(f"  https://github.com/{org}/{repo}/settings/rules")
    print(f"  https://github.com/orgs/{org}/teams")

if __name__ == "__main__":
    main()

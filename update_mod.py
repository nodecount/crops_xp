#%%
# py update_mod.py

import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import sys
import requests
import json

target_version = input("Version Minecraft cible (ex: 1.21.10) : ").strip()
build_path = "./build/libs"

#######################################
##  Création de la nouvelle branche  ##
#######################################

print("\n")

new_branch_created = False
actual_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
if actual_branch != target_version:
    print(f"Création de la branche {target_version} basée sur l'actuelle {actual_branch}...")

    subprocess.run(["git", "checkout", "-b", target_version], check=True)

    print(f"# Nouvelle branche {target_version} créée")
    new_branch_created = True

#######################################################################
##  Mise à jour des versions des dépendances dans gradle.properties  ##
#######################################################################

print("\n")

print(f"Récupération des versions des dépendances pour la version {target_version}...")

# Récupération de la yarn_version

yarn_data = requests.get("https://meta.fabricmc.net/v2/versions/yarn").json()
yarn_version = next(x["version"] for x in yarn_data if x["gameVersion"] == target_version)

# Récupération de la loader_version

loader_data = requests.get("https://meta.fabricmc.net/v2/versions/loader").json()
loader_version = loader_data[0]["version"]

# Récupération de la loom_version

loom_version = "1.12-SNAPSHOT"

# Récupération de la fabric_version

xml_data = requests.get("https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml").text
root = ET.fromstring(xml_data)
versions = [v.text for v in root.find("versioning").find("versions").findall("version")]
fabric_versions = [v for v in versions if v.endswith(target_version)]
fabric_version = fabric_versions[-1]  # dernière = la plus récente

# Aggrégation et affichage des versions récupérées

new_versions = {
    "minecraft_version": target_version,
    "yarn_mappings": yarn_version,
    "loader_version": loader_version,
    "loom_version": loom_version,
    "fabric_version": fabric_version,
}

print(f"Nouvelles versions des dépendances récupérées :\n")
for k, v in new_versions.items():
    print(f"  {k}={v}")

# Lecture de gradle.properties et modification des versions des dépendances

file = "./gradle.properties"

print(f"\nEcriture des nouvelles versions des dépendances dans {file}...")

with open(file, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    for key, value in new_versions.items():
        if line.startswith(key + "="):
            line = f"{key}={value}\n"
            break
    new_lines.append(line)

with open(file, "w") as f:
    f.writelines(new_lines)

print(f"\nVersions des dépendances mises à jour dans le fichier")

################################
##  Chercher/remplacer final  ##
################################

print("\n")

print(f"Recherche des références restantes à un ancienne version et remplacement par {target_version}...")

old_version = None
if new_branch_created:
    old_version = actual_branch
else:
    old_version = input(f"Quelle est la version ayant servi de base à la duplication du code ? (laisser vide pour ignorer cette étape)")

if old_version:
    result = subprocess.run(
        ["git", "grep", "-l", old_version],
        capture_output=True,
        text=True,
        check=False
    )

    files = result.stdout.splitlines()

    for file_path in files:
        path = Path(file_path)
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            new_content = content.replace(old_version, target_version)
            path.write_text(new_content, encoding="utf-8")

    print(f"\nChercher/remplacer de {old_version} vers {target_version} terminé")

###################################
##  Commit & push de la branche  ##
###################################

print("\n")

menu_push_branch = input(f"Commit & push du code modifié ? (y/n)")
if menu_push_branch == 'y':
    new_branch = target_version
    print(f"Commit & push de la nouvelle branche {new_branch}...")

    commit_msg = f"Update to {target_version}"

    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    if new_branch_created == 'y':
        subprocess.run(["git", "push", "-u", f"origin {new_branch}"], check=True)
    else:
        subprocess.run(["git", "push"], check=True)

    print(f"# Commit \"{commit_msg}\" et push réalisés sur {new_branch}")

#############################################
##  Build du mod dans la nouvelle version  ##
#############################################

print("\n")

jars_built = list(Path(build_path).glob("*.jar"))

menu_rebuild = None
if len(jars_built) == 2:
    menu_rebuild = input(f"(Rebuild le mod dans la nouvelle version {target_version} ? (y/n)")

if not menu_rebuild or menu_rebuild == 'y':
    print(f"Build du mod dans la nouvelle version {target_version}...")

    gradlew = Path("gradlew.bat" if sys.platform.startswith("win") else "./gradlew")

    subprocess.run([str(gradlew), "--stop"], check=True)
    subprocess.run([str(gradlew), "clean"], check=True)
    subprocess.run([str(gradlew), "build --refresh-dependencies"], check=True)

    print(f"\nJAR du mod généré dans sous \"{build_path}\" (ne pas prendre \"xxx-sources.jar\")")

##########################################
##  Publication du mod dans CurseForge  ##
##########################################

print("\n")

menu_curseforge = input(f"Publication du mod dans CurseForge ? (y/n)")
if menu_curseforge == 'y':
    jars_built = list(Path(build_path).glob("*.jar"))
    if len(jars_built) == 2:

        API_KEY = "VOTRE_API_KEY"
        PROJECT_ID = "VOTRE_PROJECT_ID"
        FILE_PATH = f"{build_path}/cropse_xp-1.21.10.jar"

        payload = {
            "gameVersions": [target_version, "Java 21"],
            "releaseType": "release",  # alpha | beta  | release
            "changelog": "Mise à jour pour Minecraft 1.21.10",
            "relations": {
                "projects": [
                    {
                        "slug": "fabric-api",
                        "type": "requiredDependency"
                    }
                ]
            }
        }

        headers = {
            "x-api-token": API_KEY
        }

        with open(FILE_PATH, "rb") as f:
            files = {
                "metadata": (None, requests.utils.json.dumps(payload), "application/json"),
                "file": (FILE_PATH, f, "application/java-archive")
            }
            r = requests.post(
                f"https://minecraft.curseforge.com/api/projects/{PROJECT_ID}/upload-file",
                headers=headers,
                files=files
            )

        print(r.status_code, r.text)
    else:
        print(f"Echec : Il n'existe aucun .jar dans \"{build_path}\"")



##########################################
##  Publication du mod dans CurseForge  ##
##########################################

print("\n")

menu_modrinth = input(f"Publication du mod dans Modrinth ? (y/n)")
if menu_modrinth == 'y':
    jars_built = list(Path(build_path).glob("*.jar"))
    if len(jars_built) == 2:

        MODRINTH_TOKEN = "VOTRE_TOKEN_MODRINTH"
        PROJECT_ID = "VOTRE_PROJECT_ID"  # ex: "cropse_xp"
        FILE_PATH = "build/libs/cropse_xp-1.21.10.jar"

        # métadonnées de la release
        data = {
            "name": "cropse_xp 1.21.10",
            "version_number": "1.21.10",
            "project_id": PROJECT_ID,
            "changelog": "Mise à jour compatibilité Minecraft 1.21.10, Fabric, client & serveur.",
            "game_versions": ["1.21.10"],
            "loaders": ["fabric"],
            "dependencies": [
                {
                    "dependency_type": "required",
                    "project_id": "fabric-api"
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {MODRINTH_TOKEN}"
        }

        with open(FILE_PATH, "rb") as f:
            files = {
                "data": (None, json.dumps(data), "application/json"),
                "file": (FILE_PATH, f, "application/java-archive")
            }

            r = requests.post("https://api.modrinth.com/v2/version", headers=headers, files=files)

        print(r.status_code, r.text)
    else:
        print(f"Echec : Il n'existe aucun .jar dans \"{build_path}\"")

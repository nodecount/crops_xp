#%%
# py update_mod.py

import requests
import xml.etree.ElementTree as ET
import subprocess
# import os

target_version = input("Version Minecraft cible (ex: 1.21.9) : ").strip()

#######################################
##  Création de la nouvelle branche  ##
#######################################

old_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
old_version = old_branch

new_branch = target_version
subprocess.run(["git", "checkout", "-b", new_branch], check=True)

print(f"# Nouvelle branche créée : {new_branch}")

#######################################################################
##  Mise à jour des versions des dépendances dans gradle.properties  ##
#######################################################################

print(f"\nRécupération des versions des dépendances pour la version {target_version}...")

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

# Compilation et affichage des versions récupérées

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

print(f"\nChercher/remplacer final des {old_version} restants en {target_version}...")

# for root, dirs, files in os.walk("."):
#     for file in files:
#         path = os.path.join(root, file)
#         # on ignore .git
#         if ".git" in path:
#             continue
#         try:
#             with open(path, "r", encoding="utf-8") as f:
#                 content = f.read()
#             if old_version in content:
#                 content = content.replace(old_version, target_version)
#                 with open(path, "w", encoding="utf-8") as f:
#                     f.write(content)
#         except:
#             # on ignore les fichiers non textuels sans erreur
#             pass

subprocess.run(
    f'git grep -l "{old_version}" | xargs sed -i "s/{old_version}/{target_version}/g"',
    shell=True,
    check=False
)

print(f"\nChercher/remplacer de {old_version} vers {target_version} terminé")

#############################################
##  Build du mod dans la nouvelle version  ##
#############################################

print(f"\nBuild du mod dans la nouvelle version {target_version}...")

subprocess.run(["./gradlew", "build --refresh-dependencies"], check=True)

print(f"\nJAR du mod généré dans sous ./build/libs (ne pas prendre xxx-sources.jar)")

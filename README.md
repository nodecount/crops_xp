# Crops XP Minecraft mod

This Minecraft mod runs with the Fabric and Forge modloaders.

## About

This mod allows you to gains XP when you harvest mature crops.

This is a good alternative to killing mobs to gain experience in Minecraft. Ideal for players who play in peaceful mode and still want to enchant their stuff.

Works with other mods which integrate crops (farmer delight, ...).

## How this mod has been created

Doc :    
- https://docs.fabricmc.net/develop/getting-started/creating-a-project

### Get the Fabric template

Go to https://fabricmc.net/develop/template/ and enter :    
- Crops XP
- nodecount.crops_xp
- 1.21.9
- Check "Split client and common sources"
- Click on `Download Template`

Official example :    
- https://github.com/FabricMC/fabric-example-mod/

If you only want to watch the recommended versions of Fabric Loader, Yarn and Fabric API for the `gradle.properties` file corresponding to a Minecraft version :    
- https://fabricmc.net/develop/

### Get the Forge template

Go to https://files.minecraftforge.net/net/minecraftforge/forge/ :    
- Click on version 1.21.9
- Download on version 1.21.9
- Click on `Mdk`

### Modifying the templates

Modify the project's `gradle.properties` file to change the `maven_group` and `archive_base_name` properties to match your mod's details.

Modify the `\src\main\resources\fabric.mod.json` file to change the `id`, `name`, and `description` properties to match your mod's details.

More about the `fabric.mod.json` file :    
- https://docs.fabricmc.net/develop/getting-started/project-structure

Make sure to update the versions of Minecraft, the mappings, the Loader and the Loom - all of which can be queried through https://fabricmc.net/develop/ - to match the versions you wish to target.

## How to run the mod and build it into a JAR file

### Upgrade Gradle wrapper

Do :    
```powershell
./gradlew wrapper --gradle-version 8.14
./gradlew wrapper --version
```

> When you have to upgrade `minecraft_version` and `fabric-loom` version, update first Gradle wrapper version
> or you will get error `Failed to setup Minecraft, java.lang.UnsupportedOperationException: Unsupported unpick version`
> In this case, come back on a functionnal version and upgrade Gradle wrapper

### Clean Gradle cache

Do :    
```powershell
./gradlew --stop
./gradlew clean
Remove-Item ".gradle\loom-cache" -Recurse -Force
```

### Setting up a Development Environment 

Installing JDK 21 :    
- https://www.oracle.com/fr/java/technologies/downloads/#jdk21-windows

### Run the mod

Do :    
```powershell
./gradlew runClient # Start the game in client mode
./gradlew runServer # Start the game in server mode
```

### Build the mod into a JAR file

Do :    
```powershell
./gradlew build --refresh-dependencies
```

The generated JAR is here (no need to take the `xxx-sources.jar`) :
```powershell
cd build/libs
```

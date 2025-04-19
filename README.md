# Crops XP Minecraft mod

This Minecraft mod is running with the Fabric modloader.

## About

Allow you to gains XP while harvaseting mature crops.

It's a good alternative to kill monsters to win experience in Minecraft. Ideal for players that play in peaceful and also want to enchant their stuff.

Works with other mod which integrate crops (farmer delight, ...)

## How this mod has been created

Doc :    
- https://docs.fabricmc.net/develop/getting-started/creating-a-project

### Get the Fabric template

Go to https://fabricmc.net/develop/template/ and enter :    
- crops xp
- nodecount.crops_xp
- 1.21.1

Official example :    
- https://github.com/FabricMC/fabric-example-mod/

### Modifying the template

Modify the project's `gradle.properties` file to change the `maven_group` and `archive_base_name` properties to match your mod's details.

Modify the `\src\main\resources\fabric.mod.json` file to change the `id`, `name`, and `description` properties to match your mod's details.

More about the `fabric.mod.json` file :    
- https://docs.fabricmc.net/develop/getting-started/project-structure

Make sure to update the versions of Minecraft, the mappings, the Loader and the Loom - all of which can be queried through https://fabricmc.net/develop/ - to match the versions you wish to target.

## How to run the mod and build it into a JAR file

### Setting up a Development Environment 

Installing JDK 21 :    
- https://www.oracle.com/fr/java/technologies/downloads/#jdk21-windows

### Run the mod

Do :    
```bash
./gradlew runClient # Start the game in client mode
./gradlew runServer # Start the game in server mode
```

### Build the mod into a JAR file

Do :    
```bash
./gradlew build
```

The generated JAR is here (no need to take the `xxx-sources.jar`) :
```bash
cd build/libs
```

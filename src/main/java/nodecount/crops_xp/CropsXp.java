package nodecount.crops_xp;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.minecraft.block.CropBlock;
import net.minecraft.entity.ExperienceOrbEntity;
import net.minecraft.server.world.ServerWorld;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CropsXp implements ModInitializer {
	public static final String MOD_ID = "crops_xp";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		// This code runs as soon as Minecraft is in a mod-load-ready state.
		// However, some things (like resources) may still be uninitialized.
		// Proceed with mild caution.

		PlayerBlockBreakEvents.AFTER.register((world, player, pos, state, blockEntity) -> {
			if (!world.isClient && state.getBlock() instanceof CropBlock cropBlock) {
				if (cropBlock.isMature(state)) {
					ServerWorld serverWorld = (ServerWorld) world;
					int numberOfOrbs = world.getRandom().nextBetween(3, 4);
					int orbXpPoints = 3;

					for (int i = 0; i < numberOfOrbs; i++) {
						// Position légèrement décalée pour éviter une superposition exacte
						double offsetX = (world.getRandom().nextDouble() - 0.5) * 0.3;
						double offsetZ = (world.getRandom().nextDouble() - 0.5) * 0.3;

						ExperienceOrbEntity xpOrb = new ExperienceOrbEntity(
							serverWorld,
							pos.getX() + 0.5 + offsetX, pos.getY() + 0.5, pos.getZ() + 0.5 + offsetZ,
							orbXpPoints
						);

						serverWorld.spawnEntity(xpOrb);
					}

					LOGGER.info("Mature crop of type {} has been broke by {}", state.getBlock().getTranslationKey(), player.getName().getString());
					LOGGER.info(" => {} orbres of {} Xp points generated", numberOfOrbs, orbXpPoints);
				}
			}
		});
	}
}
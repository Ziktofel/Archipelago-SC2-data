Debug commands in Archipelago SC2 are in-game chat commands, intended to be used by developers for testing and bug fixing purposes. They are similar to cheat codes, but usually provide benefits more specific to AP or the current mission. Since they are intended to be used by developers for testing, they often have shorthand variants, to prevent activating these commands by accident it is required to enable Debug Mode first with a separate command. Entering Debug Mode enables all other debug commands. Every Debug command starts with a dash/minus '-'

Debug commmands can be divided into 3 categories:

• Generic: These commands work in ANY Archipelago SC2 mission.
• Semi Generic: These commands are not implemented in every single mission, but they are shared across many missions where they make sense. Example: Skip to the next section of a mission.
• Map Specific: These commands test a specific feature of the mission you are currently playing. Example: Complete a bonus objective.

Full list of Debug Commmands:


Generic: These commands can be used in any Archipelago SC2 mission

-debug, -d: Activate Debug Mode, required to use all the other debug commands


-control x: Take one-sided control of player x
-reapply: Reapplies default behaviors to all your units. Fixes certain bugs where units do not get all benefits from their items
-resetbase, -reset: Resets many aspects of your main base, including Spear of Adun energy/cooldown and Merc cooldown
-skip, -s: Skips all transmissions currently playing, and allows other triggers queued after these transmissions to progress the mission state
-clear, -c: Clears the action queue, retaining the one action currently running. WARNING: This can soft-lock your game!

-win: Ends the mission in victory, granting the victory location (intended to work in all missions, does not work for all missions at this time)
-revive, -r: Revives your heroes instantly (currently only works with Kerrigan, intended to work with other heroes like Nova)


Semi-generic: These commands are not implemented in every single mission, but they are shared across multiple missions where they make sense

-sx: Skip to Section X. This command is implemented in most missions that have multiple sections. For example, typing '-s2' in the mission "The Dig" will skip Section 1, the Siege Tank introduction and proceed to Section 2, the defense of the Laser Drill.

This is intended to be a prototype for the future implementation of a Checkpoint system.



Map Specific: These commands only work for one (or a few) specific missions, usually to test a mechanic only used in that mission.

Rendezvous:

-fenix: Spawns Fenix in the enemy base (test for the final reinforcement wave for Protoss raceswap)

With Friends like these:

-FullPower: All Hyperion upgrades.

Templar's Return:

-openX: Open Door X

The Infinite Cycle:

-holdoutX, -hX: Skips to the specified "holdout" sections. The semi-generic -sX command skips to after the holdouts instead.

The Escape:

-s3: This skips to the Vulture freeway escape section, which is normally not accessible in Archipelago.

Breakout:

-freeX: Complete bonus objective X, freeing the prisoners.

Gates of Hell

-drop: Spawn the next drop pod. Currently only works for the very first drop pod.

Piercing the Shroud:

-ammo: Replenish your abilities.

Zero Hour:

-spawn: Make the next rescues appear on the Map.
-flank: Trigger a flank attack.
-drop: Trigger a Zerg drop pod.
-color: Make the different zerg players use different colors.

Harvest of Screams:

-snowdie: Stop the snowfall visuals 
-snowgo: Restart snow
-blizzardgo: Start a flash freeze

The Dig:

-s2: Start Drill phase
-s3, -s4, -s5: Set the door to 70%, 33%, 5% hp
-drill: Get control of the Drill

Into the Void:

-fX: Establish Forward Bases. 1,2,3 for Raynor, Kerrigan or Artanis AI (only available if the respective AI controls one of the bases). Each use will make the AI progress 1 "step".
-bX: Finish the 4 Bonus Objectives.
-tX: Spawn Void Thrasher attacking Player X, 1,2,3 being Raynor, Kerrigan or Artanis.

The Essence of Eternity

-revive, -r: Instantly revives all heroes used by your allies (or yourself if playing with ally control enabled).

Amon's Fall:

-eat: Trigger Amon to destroy the next base in the cycle.

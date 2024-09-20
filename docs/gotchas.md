# Gotchas
Writing down pitfalls encountered over time spent working on the project to hopefully not fall into them again.

## Data
### Magazines
A unit can have multiple Magazine abilities with different ammo. However, a `CEffectUseMagazine` needs to specify which magazine Abil it is using, or it will use all and will ignore current ammo count and maximums for the later ones.

## Triggers
### Cutscenes
Most cutscenes disable all units / factions not part of the cutscene. This means conditions checking the presence of enemies in a trigger like a victory trigger may behave unexpectedly around cutscenes.

For example, there was a bug in The Dig where the "kill the bases" locations would send when triggering the cutscene on reaching the base.


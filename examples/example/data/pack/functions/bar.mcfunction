gamemode creative @a[limit=2]
function pack:foo
say After!
advancement grant @a only minecraft:story/shiny_gear
bossbar add bar1 "My bossbar"
bossbar set bar1 color red
bossbar set bar1 visible true
bossbar set bar1 players Mongoriann
bossbar set bar1 value 100
bossbar set bar1 max 200
bossbar list
say name, color, style: My bossbar, red, progress
scoreboard players add Mongoriann a 4
execute at @e[sort=random, limit=1] run summon minecraft:lightning_bolt
execute at @e[sort=random, limit=1] run tp Mongoriann

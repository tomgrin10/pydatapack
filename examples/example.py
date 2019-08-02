from pydatapack.mc import *


def foo():
    """
    This function
    is very cool
    """
    say("Hello, world!")
    command_unsafe("say Hello, world!")


def bar():
    gamemode(target=target.players(limit=2), mode=gamemode.creative)
    foo()
    say("After!")
    advancement.grant(target.players, advancement.method.only, "minecraft:story/shiny_gear")

    bar1 = Bossbar("bar1")
    bar1.add("My bossbar")
    bar1.color = "red"
    bar1.visible = True
    bar1.players = "Mongoriann"
    bar1.value = 100
    bar1.max = 200
    Bossbar.list()
    say(f"name, color, style: {', '.join((bar1.name, bar1.color, bar1.style))}")

    score = scoreboard.Score("Mongoriann", "a")
    score.__iadd__(4)
    score += 'a'

    with execute.at(target.entities(sort=target.sort.random, limit=1)):
        summon("minecraft:lightning_bolt")
        tp("Mongoriann")


def a():
    with execute.at(target.entities(sort=target.sort.random, limit=1)):
        summon("minecraft:lightning_bolt")
        a()


def sleep():
    with execute.as_(target.players):
        command_unsafe("execute store result score @s SleepTimer run data get entity @s SleepTimer")

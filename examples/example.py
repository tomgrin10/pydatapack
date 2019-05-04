from pydatapack.mc import *


def foo():
    """
    This function
    is very cool
    """
    say("Hello, world!")
    command_unsafe("say Hello, world!")


def bar():
    gamemode(target=target.players(limit=1), mode=gamemode.creative)
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
    say(f"name: {bar1.name}, color: {bar1.color}, style: {bar1.style}")

    del bar1
    with execute.at(target.entities(sort=target.sort.random, limit=1)):
        summon("minecraft:lightning_bolt")
        tp("Mongoriann")


def a():
    summon("minecraft:lightning_bolt")


def b():
    with execute.at(target.entities(sort=target.sort.random, limit=1)):
        a()

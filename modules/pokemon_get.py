import pokepy
import random

search = pokepy.V2Client()


def get_all_info(name):
    try:
        pokemon = search.get_pokemon(name)
    except Exception:
        return

    species = search.get_pokemon_species(pokemon.id)

    stats = {
        (pokemon.stats[i].stat.name).upper(): pokemon.stats[i].base_stat
        for i in range(len(pokemon.stats))
    }

    total = 0
    for stat in stats.values():
        total += stat

    stats["**TOTAL**"] = total

    lore = [
        text.flavor_text
        for text in species.flavor_text_entries
        if text.language.name == "en"
    ]

    info = {
        "name": (pokemon.name).capitalize(),
        "id": pokemon.id,
        "color": species.color.name,
        "height": f"{pokemon.height/10} m",
        "weight": f"{pokemon.weight/10} kg",
        "image": f"https://img.pokemondb.net/artwork/{pokemon.name}.jpg",
        "types": [typ.type.name for typ in pokemon.types],
        "abilities": [
            (ability.ability.name).capitalize() for ability in pokemon.abilities
        ],
        "stats": stats,
        "lore": lore[random.randint(0, len(lore) - 1)]
        .replace("\x0c", " ")
        .replace("\n", " "),
    }

    return info


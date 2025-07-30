# Copyright (C) 2025 <UTN FRA>
#
# Author: Facundo Falcone <f.falcone@sistemas-utnfra.com.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

lista_dict_pokemones = [
        {
            "id": 244,
            "nombre": "entei",
            "tipo": ["fuego"],
            "poder": 30,
            "condicion": "legendario"
        },
        {
            "id": 28,
            "nombre": "sandslash",
            "tipo": ["suelo"],
            "poder": 15,
            "condicion": "normal"
        },
        {
            "id": 584,
            "nombre": "vanilluxe",
            "tipo": ["hielo"],
            "poder": 15,
            "condicion": "normal"
        },
        {
            "id": 26,
            "nombre": "raichu",
            "tipo": ["eléctrico"],
            "poder": 20,
            "condicion": "normal"
        },
        {
            "id": 9,
            "nombre": "blastoise",
            "tipo": ["agua"],
            "poder": 18,
            "condicion": "normal"
        },
        {
            "id": 384,
            "nombre": "rayquaza",
            "tipo": ["dragón"],
            "poder": 39,
            "condicion": "legendario"
        },
        {
            "id": 150,
            "nombre": "mewtwo",
            "tipo": ["psiquico"],
            "poder": 25,
            "condicion": "normal"
        },
        {
            "id": 483,
            "nombre": "dialga",
            "tipo": ["acero"],
            "poder": 38,
            "condicion": "legendario"
        },
        {
            "id": 5,
            "nombre": "charmeleon",
            "tipo": ["fuego"],
            "poder": 8,
            "condicion": "normal"
        },
        {
            "id": 76,
            "nombre": "golem",
            "tipo": ["suelo"],
            "poder": 16,
            "condicion": "normal"
        },
        {
            "id": 144,
            "nombre": "articuno",
            "tipo": ["hielo"],
            "poder": 33,
            "condicion": "legendario"
        },
        {
            "id": 25,
            "nombre": "pikachu",
            "tipo": ["eléctrico"],
            "poder": 5,
            "condicion": "normal"
        },
        {
            "id": 134,
            "nombre": "vaporeon",
            "tipo": ["agua"],
            "poder": 18,
            "condicion": "normal"
        },
        {
            "id": 373,
            "nombre": "salamence",
            "tipo": ["dragón"],
            "poder": 20,
            "condicion": "normal"
        },
        {
            "id": 151,
            "nombre": "mew",
            "tipo": ["psiquico"],
            "poder": 24,
            "condicion": "normal"
        },
        {
            "id": 82,
            "nombre": "magneton",
            "tipo": ["acero"],
            "poder": 21,
            "condicion": "normal"
        },
        {
            "id": 6,
            "nombre": "charizard",
            "tipo": ["fuego"],
            "poder": 18,
            "condicion": "normal"
        },
        {
            "id": 383,
            "nombre": "groudon",
            "tipo": ["suelo"],
            "poder": 32,
            "condicion": "legendario"
        },
        {
            "id": 614,
            "nombre": "beartic",
            "tipo": ["hielo"],
            "poder": 16,
            "condicion": "normal"
        },
        {
            "id": 145,
            "nombre": "zapdos",
            "tipo": ["eléctrico"],
            "poder": 35,
            "condicion": "legendario"
        },
        {
            "id": 245,
            "nombre": "suicune",
            "tipo": ["agua"],
            "poder": 31,
            "condicion": "legendario"
        },
        {
            "id": 334,
            "nombre": "altaria",
            "tipo": ["dragón"],
            "poder": 20,
            "condicion": "normal"
        },
        {
            "id": 249,
            "nombre": "lugia",
            "tipo": ["psiquico"],
            "poder": 34,
            "condicion": "legendario"
        },
        {
            "id": 208,
            "nombre": "steelix",
            "tipo": ["acero"],
            "poder": 23,
            "condicion": "normal"
        }
    ]

lista_poke_ids = [
    244, 28, 584,
    26, 9, 384,
    150, 483, 5,
    76, 144, 25,
    134, 373, 151,
    82, 6, 383,
    614, 145, 245,
    334, 249, 208
]

lista_poke_nombres = [
    "entei", "sandslash", "vanilluxe", 
    "raichu", "blastoise", "rayquaza", 
    "mewtwo", "dialga", "charmeleon",
    "golem", "articuno", "pikachu",
    "vaporeon", "salamence", "mew",
    "magneton", "charizard", "groudon",
    "beartic", "zapdos", "suicune",
    "altaria", "lugia", "steelix"
]

lista_poke_poderes = [
    30, 15, 15,
    20, 18, 39,
    25, 38, 8,
    16, 33, 5,
    18, 20, 24,
    21, 18, 32,
    16, 35, 31,
    20, 34, 23
]

lista_poke_condiciones = [
    "legendario", "normal", "normal",
    "normal", "normal", "legendario",
    "normal", "legendario", "normal",
    "normal", "legendario", "normal",
    "normal", "normal", "normal",
    "normal", "normal", "legendario",
    "normal", "legendario", "legendario",
    "normal", "legendario", "normal"
]

lista_poke_tipos = [
    "fuego", "suelo", "hielo",
    "eléctrico", "agua", "dragón",
    "psiquico", "acero", "fuego",
    "suelo", "hielo", "eléctrico",
    "agua", "dragón", "psiquico",
    "acero", "fuego", "suelo",
    "hielo", "eléctrico", "agua",
    "dragón", "psiquico", "acero"
]

matriz_pokemones = [
    lista_poke_ids,
    lista_poke_nombres,
    lista_poke_tipos,
    lista_poke_poderes,
    lista_poke_condiciones
]
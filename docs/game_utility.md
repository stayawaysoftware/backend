# Utilidades para Game: funciones y usos

Dentro de lo que es la implementación de la lógica del juego, se brindan las funciones desarrolladas en game_utility para que sean las que se usen por parte del módulo de la partida, como un nivel muy superior a la aplicación de los efectos de las cartas, manejo de las relaciones entre carta/mazo/jugadores, etc.

Son funciones que sirven como gran abstracción para facilitar el desarrollo de los distintos módulos planteados e implementados en nuestro sistema.

## Explicación de uso de las utilidades brindadas

En particular, estas funciones nosotros la vamos a usar para lo siguiente:

- _Inicializar los mazos_ ==> Apenas se crea el juego, se debe llamar a esta función para crear los mazos y llenar el de disponibles de todas las cartas correspondientes en función de la cantidad de jugadores que se considere.
- _Eliminar los mazos_ ==> Cuando la partida finalice, se llama esta función para eliminar los mazos creados y sus relaciones con las cartas
- _Robar una carta del mazo de disponibles_ ==> Cuando se esté en la fase de robar una carta (o un efecto lo requiera), se debe llamar a esta función
- _Descartar una carta_ ==> Análogo a lo anterior pero con la fase de descarte (o que un efecto lo requiera)
- _Jugar una carta_
  - Debe ser llamada para los siguientes casos:
    - Una carta fue jugada por un jugador de la partida (sea acción, defensa, obstáculo o pánico)
    - El jugador elige no defenderse (tanto de una carta de acción, como de un intercambio)
    - Se pide realizar un intercambio
  - En particular, se tiene como "**contrato**" que:
    - Si se juega una carta --> Se pasa el IDTYPE real de esa carta
    - Si NO se defiende --> El IDTYPE es 0
    - Si se pide intercambio --> El IDTYPE es 32

## Explicación de las funciones implementadas

### Inicializar mazos

`initialize_decks(id_game: int, quantity_players: int) -> Deck`

- Dados el ID de la partida y la cantidad de jugadores, se encarga de crear los mazos y llenar el mazo de disponibles con las cartas correspondientes (en función de la cantidad de jugadores).
- Se devuelve la entidad del Mazo General creado y con la cual están relacionados el de disponible y el de descarte

### Eliminar mazos

`delete_decks(id_game: int) -> None`

- Dado el ID de la partida, se encarga de eliminar los mazos relacionados a esta

### Robar carta del mazo de disponibles

`draw(id_game: int, id_player: int) -> int`

- Esta función es la que se encarga de sacar una carta _random_ del mazo de disponibles de nuestra partida
  - En caso que no tenga ninguna carta, es la encargada de llamar a la función de "mezclar" los mazos (i.e., mover todas las descartadas al de disponibles nuevamente)
- Además, se encarga de manejar las relaciones sacándola del mazo de disponibles y agregándosela directamente a la mano del jugador
- Devuelve el ID de la carta para facilitar los tests de unicidad de relaciones dentro de una misma partida

### Descartar una carta

`discard(id_game: int, idtype_card: int, id_player: int) -> int`

- Se encarga de elegir una carta random de la mano del jugador que coincida con el IDTYPE pasado por parámetro, sacarla de su mano y agregarla al mazo de descarte de esa misma partida

### Jugar una carta (incluye defensa) + relizar intercambio

`play( id_game: int, id_player: int, idtype_card: int, target: Optional[int] = None) -> GameAction`

**Aclaración:** se van a usar conceptos de efectos de carta y GameAction, para lo cual primero se deberá leer el apartado correspondiente en [effects.md](effects.md).

- Dada la carta que juega el jugador y los parámetros correspondientes (como target en el caso que sea lanzallamas para saber contra quién va aplicado), se devuelve el efecto de esta carta bajo el formato de **GameAction**.
- Respecto al uso que se le tiene que dar a esta función, consideramos lo siguiente bajo un esquema general:
  - Si el GameAction especifica que se solicita una defensa, entonces se debe comunicar al front que el jugador colocado en el _target_ debe defenderse contra la carta jugada. Además, el GameAction especificará la lista de IDTYPEs de cartas que pueden defenderlo de esta acción
    - Caso contrario especificará o bien no hacer nada, o bien modificar la partida o el estado de esta
  - Si se quiere realizar un intercambio, se debe colocar que el IDTYPE de la carta es 32 y en target el jugador que se elige para cambiar
  - Si el jugador NO se defiende, se debe colocar que el IDTYPE de la carta es 0

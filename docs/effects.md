# Efectos de las cartas

Dado el IDTYPE de una carta y los parámetros de quién la juega y cuál es el "target" (contra quién se quiere aplicar), el módulo de generación de efectos de las cartas se encarga de devolver las instrucciones de lo que debe realizar la partida en caso que los datos sean correctos (i.e., no se juegue "La Cosa" por ejemplo).

## GameAction: ¿Cómo se muestra el efecto de una carta?

Las _instrucciones_ que se devuelven para que la partida sepa qué es lo que debe realizar son "empaquetadas" bajo un GameAction (objeto donde se especifican estas instrucciones).

El GameAction tiene los siguientes atributos:

- action (de tipo ActionType) ==> Por ejemplo NOTHING, KILL, ASK_DEFENSE
- target ==> Jugador al que se le debe aplicar esa acción
- possible_cards ==> En caso de ASK_DEFENSE, esta lista contiene los IDTYPES de las cartas que se pueden defender de la que se jugó (por ejemplo, si se jugó lanzallamas, en la lista está el IDTYPE de "No Barcaboas")

Es un contrato entre Game (Benja) y Lógica del Juego (Ema) para hacer independientes nuestras partes y comunicarnos únicamente en el tema de efectos mediante el GameAction, sin realizar ninguna modificación de la partida desde la lógica del juego sino diciendo qué es lo que se debe hacer. Esto permite que la implementación del modelo sea independiente de la implementación de los efectos.

## Esquema de los efectos de una carta (¿cómo funciona internamente?)

La función desde la cual se llaman en general a todos los efectos es `do_effect`. Esta es la que, en función del IDTYPE de la carta, "deriva" la responsabilidad a la función que corresponda en base a la carta que se jugó.

Por ejemplo, si se jugó "Lanzallamas", se llama a `do_effect` con el IDTYPE de "Lanzallamas" y se deriva la responsabilidad a la función `do_lanzallamas_effect`.

En el caso de que se juegue una carta que no tenga efecto, se devuelve un GameAction con action = NOTHING.

## ¿Cómo se implementa un efecto?

Para implementar un efecto, se debe crear una función que se llame `do_<nombre_carta>_effect` (por ejemplo, `do_lanzallamas_effect`). Esta función debe recibir los siguientes parámetros:

- id_game: ID de la partida
- id_player: ID del jugador que jugó la carta (en caso que sea necesario)
- target: ID del jugador al que se le quiere aplicar el efecto (en caso que sea necesario)

Además, los efectos, en caso de ser de existir cartas que se puedan defender, deben contener un booleano que implique si se jugó por primera vez o realmente se quiere hacer el efecto de esa carta.

Esto se usa para que, si se juega por primera vez la carta LANZALLAMAS, se devuelva un GameAction con action = ASK_DEFENSE y possible_cards = [IDTYPE de "No Barcaboas"]. Luego, si la siguiente carta que se juega (que sería la de defensa) es None, se vuelve a llamar a `do_lanzallamas_effect` pero con el booleano de "primera vez" en False, para que se haga el efecto de la carta y se pida la KILL.

Para ello es importantísimo que Game guarde en su modelo la última llamada realizada a play() (i.e., la última carta que se jugó) para poder redirigir al efecto a realizar en caso de que no se haga la defensa.

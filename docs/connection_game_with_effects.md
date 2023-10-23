# Esquema de los nuevos efectos y conexión con Game

## **GAME ACTION atributos**

- `action` -> ActionType
- `action2` -> ActionType (en caso que se requiera realizar más de una acción)
- `target` -> Lista de enteros
- `defense_cards` -> Lista de enteros (tipos de carta)
- `card_target` -> Lista de enteros (tipos de carta)

## CAMPOS QUE RECIBE PLAY()

- `id_game`: Id del juego
- `id_player`: Id del jugador que jugó esa carta
- `idtype_card`: Id de tipo de la carta jugada
- `idtype_card_before`: Id de la carta jugada en el paso anterior
- `target`: Persona a la que se le quiere aplicar esa carta
- `card_chosen_by_player`: Carta elegida por el jugador (pej. en intercambio)
- `card_chosen_by_target`: Carta elegida por el target (pej. en intercambio), o que eligió el player para ver (pej. en sospecha)

## **POSIBLES RETORNOS**

- Si se devuelve una excepción ValueError, entonces esa jugada de carta estuvo mal y se le debe avisar al front que el jugador no puede realizarla (por ejemplo, si se quiere intercambiar con alguien que está en cuarentena)
- Teóricamente esto lo tiene que ver el front pero por las dudas lo aviso

## **LANZALLAMAS**

- _Pedir defensa_ (first play)
    - Acción -> ASK_DEFENSE
    - Persona que se tiene que defender --> target[0]
    - Cartas con las que se puede defender -> defense_cards

- _Efecto posta si no se defiende_
    - Acción --> KILL
    - Persona que matar --> Target

- _NADA DE BARBACOAS_
    - Acción -> NOTHING

## **INTERCAMBIO / SEDUCCIÓN**

- _Pedir defensa_ (first play)
    - Acción -> ASK_DEFENSE
    - Persona que se tiene que defender --> target[0]
    - Cartas con las que se puede defender -> defense_cards

- _Efecto posta si no se defiende_
    - Acción -> EXCHANGE
    - Personas que se intercambian -> target[0], target[1]
    - Cartas que se intercambian -> card_target[0], card_target[1]

    - Acción2 -> INFECT (puede ser _None_)
    - Persona infectada -> target[2]

- _ATERRADOR_
    - Acción -> SHOW
    - Persona que muestra su carta -> target[0]
    - Persona que ve la carta -> target[1]
    - Carta que se muestra -> card_target[0]

- _NO, GRACIAS_
    - Acción -> NOTHING

- _FALLASTE_
    - Acción -> ASK_EXCHANGE (pedir intercambio pero al que le sigue en el orden al target[1])
    - Persona que intercambia -> target[0]
    - Carta que se intercambia -> card_target[0]

## **ANÁLISIS**

- _Efecto posta (first play)_
    - Acción -> SHOW_ALL (mostrar toda la mano de la persona)
    - Persona que muestra su mano -> target[0]
    - Persona que ve la carta -> target[1]

## **SOSPECHA**

- _Efecto posta (first play)_
    - Acción -> SHOW
    - Persona que muestra su carta -> target[0]
    - Persona que ve la carta -> target[1]
    - Carta que se muestra -> card_target[0]

## **WHISKY**

- _Efecto posta (first play)_
    - Acción -> SHOW_ALL_TO_ALL (mostrar toda la mano de la persona a todos los jugadores)
    - Persona que muestra su mano -> target[0]

## **VIGILA TUS ESPALDAS**

- _Efecto posta (first play)_
    - Acción -> REVERSE_ORDER

## **CAMBIO DE LUGAR / MÁS VALE QUE CORRAS**

- _Pedir defensa_ (first play)
    - Acción -> ASK_DEFENSE
    - Persona que se tiene que defender --> target[0]
    - Cartas con las que se puede defender -> defense_cards

- _Efecto posta si no se defiende_
    - Acción -> CHANGE_POSITION
    - Personas que se mueven -> target[0], target[1]

- _AQUÍ ESTOY BIEN_ / _MÁS VALE QUE CORRAS_
    - Acción -> NOTHING

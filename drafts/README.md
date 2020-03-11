
Variables globales:
  - Número de turnos
  - Número de monos
  - Probabilidad de cada depredador
  - Probabilidad de cada evento (e.g. serpiente atrapa a mono en arbusto)


Antes de comenzar la serie de turnos:
  1. Se crean monos y se asigna wordmap y actionmap aleatorios a los monos
  2. Se crean los depredadores

Para cada turno:
  1. El águila/serpiente aparece (o no aparece)
  2. Algunos monos ven al águila/serpiente, si es que aparece
  3. Los monos envían mensajes según lo que perciben (hay un mensaje nulo y una percepción nula)
  4. Los monos deciden qué hacer según lo que han escuchado
  5. El águila/serpiente come. (se eliminan monos de la lista)

En la trasición de un turno a otro:
  1. Replicación?
  2. Transmisión del lenguaje?
  3. Reinforcement?
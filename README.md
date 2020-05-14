# Ejercicio BKR

El ejercicio consiste de hacer una api con 2 tablas y armar endpoint REST para consultar,
crear, borrar o actualizar ambas tablas. Los servicios deben responder manejando solo el *Accept: application/json*

- [*] Generar tablas `users` y `states`
- [*] Importar informacion del archivo `stats.csv` en la tabla `states`
- [*] Generar CRUD (REST) de `users`
- [*] Generar endpoint (REST) `states`


## Tablas


### Users

Column | Type
------ | ----
id | int sequence ( PK )
name | string
age | int
state | int (FK states)
updated_at | datetime
created_at | datetime

### States
Column | Type
------ | ----
id | int sequence ( PK )
code | int
name | string
updated_at | datetime
created_at | datetime

## Solución

### Api REST:

Para ejecutar el api REST:

    `docker-compose up api`

Enpoints del api REST:

Modelo | Operacion | Verbo HTTP | Endpoint
------ | --------- | ---------- | --------
State  | Listar    | GET        | /api/v1/states
User   | Listar    | GET        | /api/v1/users
User   | Crear     | POST       | /api/v1/users
User   | Leer uno  | GET        | /api/v1/users/<user_id>
User   | Modificar | PATCH      | /api/v1/users/<user_id>
User   | Eliminar  | DELETE     | /api/v1/users/<user_id>

### Ejecutar comandos

Ejecutar comandos de flask:

```bash
$ docker-compose run --rm manage
```

Crear tablas en la base de datos:

```bash
$ docker-compose run --rm manage db upgrade
```

Importar estados:

```bash
$ docker-compose run --rm manage import-states states.csv
```

Ejecutar tests:

```bash
$ docker-compose run --rm test
```

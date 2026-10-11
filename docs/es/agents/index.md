# Entrada para agentes del sistema Attestra

Alcance: diseño actual de `main`, con evidencia en [compatibilidad](../../compatibility.md). Este repositorio mantiene requisitos y contratos entre componentes, no instrucciones ejecutables de despliegue ni un artefacto instalable.

| Tarea | Guía canónica | Implementación |
| --- | --- | --- |
| Límites y términos | [Arquitectura](../../../architecture.md), [conceptos](concepts.md) | [Catálogo](../../repositories.md) |
| Onboarding y recuperación | [Flujos](journeys.md) | [Agente backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/index.md) |
| Captura/parsing | [Contratos](contracts.md) | [Captura backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/id-capture.md) |
| Descubrimiento/despliegue | [Ciclo de entornos](../../../operations/environments.md) | [Operación backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/operations.md) |
| Interfaz y comportamiento real | [Semántica UI](ui.md) | Archivos `spec.md`, no temporizadores del prototipo |
| Compatibilidad y pendientes | [Limitaciones](limitations.md) | [Responsabilidades](../../../DOCUMENTATION.md) |

Invariantes: confirmar correo no verifica identidad; solo el cliente que confirma recibe sesión; la plataforma conserva passkeys; capture ready es evidencia inmutable, no extracción ni aprobación; parsing no invoca validación silenciosamente; el índice público nunca contiene secretos o datos de identificación. Conserva refs y distingue diseño, implementación, pruebas, reporte del operador y trabajo diferido.

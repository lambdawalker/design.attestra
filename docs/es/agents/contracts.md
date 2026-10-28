# Responsabilidad de contratos e integración

| Contrato | Responsable | Representación exacta |
| --- | --- | --- |
| Pruebas de correo, transiciones y privacidad | [Diseño onboarding](../../../auth/onboarding/architecture.md) | [HTTP backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/api.md) |
| Separación captura/parsing y referencias | [Contratos de evidencia](../../../auth/onboarding/id-evidence-contracts.md) | [Captura backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/id-capture.md); parsing sigue propuesto |
| Descubrimiento público | [Arquitectura de entornos](../../../operations/environments.md) | [Índice](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/environment-index.md), `registry/registry.go` |
| Configuración Android de compilación | Exportador backend y consumidor Gradle | [Integración](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/integration.md) |
| Semántica de estados UI | `ui.md` de la función y `spec.md` cercano | [Directorio de pantallas](../../../auth/onboarding/ui-reference/README.md) |

El diseño formal de evidencia conserva su ruta actual. No lo muevas por el simple hecho de existir captura. Tampoco dupliques aquí límites operativos o tipos JSON como otro esquema mantenido a mano. Una ruta propuesta no demuestra una API desplegada.

Un cambio debe identificar páginas y pruebas afectadas de backend, Android y central. Coordina commits y registra el estado de transición: no son atómicos entre repositorios. Conserva enlaces válidos. Compatibilidad de código en desarrollo es distinta de compatibilidad entre artefactos publicados. No existe todavía una matriz de versiones de todo el sistema.

# Semántica de interfaz y evidencia

Usa el [índice de pantallas](../../../auth/onboarding/ui-reference/README.md) y el `spec.md` junto a cada HTML. Los IDs son los directorios establecidos. Cada especificación describe entrada/salida, campos/acciones, estados, accesibilidad, servicio responsable y limitaciones conocidas.

Los HTML son referencias de diseño, no integraciones ejecutándose contra backend. Temporizadores, botones o avisos de éxito no prueban entrega de correo, sesión, passkey o identidad. El sitio enlaza HTML como fuente y no lo ejecuta en su origen. Los PNG existentes llevan la etiqueta `design-prototype`; faltan hashes y renderer originales. Son referencias históricas, no capturas verificadas de una aplicación actual.

El [manifiesto](../../screenshots/manifest.json) registra esas limitaciones y rutas. No se afirma haber capturado una app de producción. Nuevas capturas aceptadas requieren datos sintéticos, renderer/configuración controlados, identidad de fuente y revisión visual. Una construcción normal no reemplaza imágenes históricas.

El código manual requiere un campo accesible de seis dígitos con pegado/autofill. Loading refleja trabajo real y ofrece timeout/recuperación. Los diálogos passkey pertenecen al sistema operativo. Preview/carga de captura y revisión de parsing necesitan variantes adicionales indicadas en las guías; la pantalla histórica de identidad aprobada pertenece a validación diferida, nunca a captura.

# Estado, limitaciones y decisiones

Lee [compatibilidad y desviaciones](../../compatibility.md) antes de tratar diseño como implementación. El backend incluye captura, índice y setup/teardown reanudables. Parsing y validación independiente siguen diseñados/diferidos. Android incluye captura y mock de depuración; el mock no valida S3 o dispositivo real.

El operador reportó setup y salud completos para dev y QA el 2026-10-10. Es evidencia reportada, no una prueba reproducible de correo, passkeys, parsing o captura real. Captura sigue siendo opt-in. Separa resultados verificables de esos reportes.

Una instancia del índice atiende una cuenta/región. Aislamiento productivo entre cuentas, publicación entre cuentas, proveedores de parsing/validación y clientes web/iOS completos permanecen abiertos. La API no hospeda el dominio de aplicación ni asociaciones. Cognito permite contraseñas a nivel proveedor aunque la UI ofrezca passkeys/correo.

La documentación describe código actual en inglés, con guías de integración en español y fallback explícito al inglés de la misma revisión para detalles sin traducir. No hay versiones de sistema confirmadas ni manuales de versiones históricas. El sitio central no certifica una versión de biblioteca por aprobar un diseño; el repositorio que publica controla los datos de instalación.

La [política de documentación](../../../DOCUMENTATION.md) es autoritativa. Se audita publicación, sin introducir publicación de paquetes. Sitios o entradas de agente faltantes en otros repositorios se registran como pendientes; este trabajo solo cambia backend y diseño central.

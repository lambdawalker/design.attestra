# Componentes y terminología

La [arquitectura](../../../architecture.md) define límites de confianza. Android controla interacción, permisos/cámara, estado protegido y credenciales nativas. La API Go valida pruebas, coordina Cognito y captura evidencia privada. AWS aporta almacenamiento, entrega, identidad de cuentas y trabajo asíncrono.

Una **prueba** autoriza confirmar correo. Una **sesión** autoriza solicitudes autenticadas. Un **manifiesto de evidencia** fija versiones S3 exactas. Un **resultado de parsing** contiene extracción con procedencia. Una **revisión** registra correcciones del usuario. Una **decisión de validación** es un resultado independiente de aseguramiento. No son intercambiables.

El **índice de entornos** publica configuración cliente. Su hash identifica contenido de configuración; no código desplegado, salud ni autenticación móvil. Los recibos de despliegue coordinan escrituras y recuperación, no son sesiones de usuario.

El [catálogo](../../repositories.md) registra responsables y disponibilidad de documentación. Sigue las guías concretas para configuración, API y limitaciones. Las especificaciones centrales no asignan números de versión a bibliotecas.

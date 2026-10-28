# Flujos y recuperación de fallos

Comienza en [onboarding](../../../auth/onboarding/README.md). La [confirmación de correo](../../../auth/onboarding/email-confirmation/flow.md) usa prueba local A y B del correo, o B y código C mostrado por separado. Leer un enlace no confirma una cuenta. Aceptar signup no prueba entrega. Reenviar invalida material anterior según presupuestos del servidor. Si se pierde una confirmación exitosa, recupera mediante login, no reproduciendo la prueba.

[Crear passkey](../../../auth/onboarding/passkey-creation/flow.md) exige sesión autenticada. La plataforma controla selector y clave privada. Cancelar o usar un dispositivo incompatible conserva el acceso por correo. [Login](../../../auth/login/architecture.md) y [reanudar](../../../auth/onboarding/resume.md) son distintos de la confirmación inicial.

[Captura](../../../auth/onboarding/id-capture/flow.md) obtiene fotos, carga a S3 privado y congela versiones exactas. Reintenta operaciones inciertas con la misma identidad y reconcilia estado. La comprobación de archivos puede terminar en ready, recaptura, fallo, cancelación o expiración. [Parsing](../../../auth/onboarding/id-parsing/flow.md) es el siguiente diseño: extracción asíncrona, JSON validado y revisión versionada. La captura actual del backend no lo implementa.

[Validación de ID](../../../verification/id-validation/architecture.md) sigue siendo independiente y diferida. “Detalles guardados” o “captura lista” nunca significa identidad aprobada. [Verificación de domicilio](../../../verification/address/architecture.md) tiene decisiones propias de política/proveedor.

Integración: [API backend](https://raw.githubusercontent.com/lambdawalker/go.attestra.aws.auth/main/docs/agents/api.md), [captura Android](https://raw.githubusercontent.com/lambdawalker/android.attestra.auth/main/docs/identity-capture.md) y [contrato HTTP cliente](https://raw.githubusercontent.com/lambdawalker/android.attestra.auth/main/docs/identity/http-contract.md). Sus revisiones son independientes; consulta el registro de evidencia antes de afirmar compatibilidad.

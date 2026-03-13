# Google OAuth 2.0 - Guía de Configuración y Solución de Problemas

Esta guía centraliza la configuración de Google OAuth 2.0 para el ERP KoreBase, consolidando los pasos de configuración y las soluciones a los problemas comunes que hemos encontrado.

## 1. Configuración del Entorno (.env)

El sistema requiere las credenciales de Google Cloud Console. Asegúrate de tener estas variables en tu archivo `.env`:

```env
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret
# (Opcional - solo si se usa el método de archivo)
# GOOGLE_CLIENT_SECRETS_PATH=/ruta/al/client_secret.json
```

## 2. Configuración en la Consola de Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. En tu proyecto, navega a **API y Servicios > Credenciales**.
3. Asegúrate de que los **Orígenes autorizados de JavaScript** incluyan:
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`
   - *Dominio web en producción (ej. onrender.com)*
4. **MUY IMPORTANTE**: Los **URI de redireccionamiento autorizados** deben coincidir **exactamente** con las URLs mapeadas en Django:
   - `http://localhost:8000/core/auth/google/callback/`
   - `http://127.0.0.1:8000/core/auth/google/callback/`
   *(Nota: el error `redirect_uri_mismatch` ocurre si falta el `/core/` al inicio o la barra `/` al final)*

## 3. Arquitectura en Django

El flujo de OAuth está manejado directamente en `core/views.py`:
- `google_login_view`: Inicia el flujo construyendo el request hacia Google.
- `google_callback_view`: Recibe la respuesta de Google, extrae los tokens, lee el perfil del usuario (email, nombres) y lo registra en la base de datos `CustomUser`.

### Generación de Usuarios Mágica
Si el usuario no existe, se crea automáticamente asegurando que el `employee_id` sea único generando un sufijo incremental si hay colisiones con la parte izquierda del correo electrónico.

## 4. Solución de Problemas Frecuentes

| Error | Causa y Solución |
|-------|------------------|
| `redirect_uri_mismatch` | Las URLs configuradas en GCP no coinciden con las de tu entorno local/producción. Verifica que la URL exacta del error esté registrada en GCP. |
| `invalid_client` | Las variables `GOOGLE_CLIENT_ID` o `GOOGLE_CLIENT_SECRET` faltan o están mal escritas en tu `.env`. |
| `no such column: core_customuser.email_verified` | Faltan migraciones por aplicar. Ejecuta `python manage.py migrate`. |
| Falta el módulo `google-auth` | Ejecuta `pip install -r requirements.txt`. Asegúrate de que el entorno virtual esté activo. |

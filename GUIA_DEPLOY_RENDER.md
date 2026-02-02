# 🚀 Deploy en Render.com - Guía Paso a Paso

## 📌 Resumen

Vamos a subir tu sistema de gestión de videos a Render.com para que esté disponible 24/7 en internet.

**Resultado final:**
- ✅ Gestor accesible desde: `https://tu-gestor.onrender.com`
- ✅ Descargador accesible desde: `https://tu-descargador.onrender.com`
- ✅ Base de datos persistente
- ✅ SSL (HTTPS) automático
- ✅ Plan gratuito disponible

---

## 🎯 PARTE 1: Preparación

### Paso 1.1: Crear cuenta en Render.com

1. Ve a [render.com](https://render.com)
2. Click en **"Get Started for Free"**
3. Regístrate con:
   - GitHub (recomendado - más fácil)
   - O con email
4. Verifica tu email

### Paso 1.2: Crear cuenta en GitHub (si no tienes)

1. Ve a [github.com](https://github.com)
2. Sign up
3. Verifica email

---

## 📦 PARTE 2: Subir el Proyecto a GitHub

### Paso 2.1: Preparar archivos

Tu carpeta debe tener estos archivos:

```
sistema-completo/
├── manager_app.py              ← Backend gestor
├── downloader_app_v3.py        ← Backend descargador
├── start_manager.py            ← NEW: Inicio gestor
├── start_downloader.py         ← NEW: Inicio descargador
├── requirements.txt            ← Dependencias
├── .gitignore                  ← NEW: Archivos a ignorar
├── templates/
│   ├── manager.html           ← Frontend gestor
│   └── downloader.html        ← Frontend descargador
└── README.md                   ← Opcional: Documentación
```

**Archivos NUEVOS que debes crear:**

**`.gitignore`** (guarda como archivo sin extensión):
```
__pycache__/
*.pyc
*.db
videos_database.db
.DS_Store
*.log
*.bat
LIMPIAR_CACHE.txt
FIX_DESCARGADOR.txt
```

### Paso 2.2: Crear repositorio en GitHub

**Opción A: Desde GitHub.com (más fácil)**

1. Ve a [github.com](https://github.com)
2. Click en el **"+"** arriba a la derecha
3. Click **"New repository"**
4. Nombre: `gestor-videos-youtube`
5. Descripción: `Sistema de gestión y descarga de videos de YouTube`
6. Privacidad: **Public** (o Private si prefieres)
7. **NO** marques "Add README"
8. Click **"Create repository"**

### Paso 2.3: Subir archivos

**Opción A: Desde la web (más fácil para principiantes)**

1. En tu nuevo repositorio, click **"uploading an existing file"**
2. Arrastra TODOS los archivos de tu carpeta `sistema-completo`
3. **IMPORTANTE:** Incluye la carpeta `templates` completa
4. Escribe mensaje: `Initial commit`
5. Click **"Commit changes"**

**Opción B: Desde GitHub Desktop (recomendado)**

1. Descarga [GitHub Desktop](https://desktop.github.com/)
2. Instala y abre sesión con tu cuenta
3. File → Add Local Repository
4. Selecciona tu carpeta `sistema-completo`
5. Click "Create Repository"
6. Escribe mensaje: `Initial commit`
7. Click **"Commit to main"**
8. Click **"Publish repository"**

✅ **Verifica:** Tu repositorio debe verse así en GitHub:
```
gestor-videos-youtube/
├── manager_app.py
├── downloader_app_v3.py
├── start_manager.py
├── start_downloader.py
├── requirements.txt
├── .gitignore
└── templates/
    ├── manager.html
    └── downloader.html
```

---

## 🌐 PARTE 3: Deploy del GESTOR

### Paso 3.1: Crear servicio web para el Gestor

1. En [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** arriba a la derecha
3. Selecciona **"Web Service"**
4. Click **"Build and deploy from a Git repository"**
5. Click **"Connect account"** (autoriza GitHub)
6. Selecciona tu repositorio: `gestor-videos-youtube`
7. Click **"Connect"**

### Paso 3.2: Configurar el Gestor

En la pantalla de configuración, llena:

| Campo | Valor |
|-------|-------|
| **Name** | `gestor-videos` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python start_manager.py` |
| **Instance Type** | `Free` |

### Paso 3.3: Variables de entorno del Gestor

Click en **"Advanced"**, luego **"Add Environment Variable"**:

**Variable 1:**
- Key: `PYTHON_VERSION`
- Value: `3.11.0`

**Variable 2:**
- Key: `RENDER`
- Value: `true`

### Paso 3.4: Crear el servicio

1. Click **"Create Web Service"** al final
2. **Espera 5-10 minutos** mientras Render:
   - Descarga tu código
   - Instala Flask y yt-dlp
   - Inicia la aplicación

✅ Cuando veas **"Your service is live 🎉"**, copia la URL:
```
https://gestor-videos-XXXX.onrender.com
```

---

## 📥 PARTE 4: Deploy del DESCARGADOR

### Paso 4.1: Crear servicio web para el Descargador

1. En tu dashboard, click **"New +"** de nuevo
2. Selecciona **"Web Service"**
3. **"Build and deploy from a Git repository"**
4. Selecciona el **MISMO repositorio**: `gestor-videos-youtube`
5. Click **"Connect"**

### Paso 4.2: Configurar el Descargador

| Campo | Valor |
|-------|-------|
| **Name** | `descargador-videos` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python start_downloader.py` |
| **Instance Type** | `Free` |

### Paso 4.3: Variables de entorno del Descargador

Click en **"Advanced"**, luego **"Add Environment Variable"**:

**Variable 1:**
- Key: `PYTHON_VERSION`
- Value: `3.11.0`

**Variable 2:**
- Key: `RENDER`
- Value: `true`

### Paso 4.4: Crear el servicio

1. Click **"Create Web Service"**
2. Espera 5-10 minutos

✅ Cuando esté listo, copia la URL:
```
https://descargador-videos-XXXX.onrender.com
```

---

## 🔗 PARTE 5: Conectar Gestor con Descargador

Ahora debes actualizar el código para que el gestor apunte al descargador en Render (no a localhost).

### Paso 5.1: Actualizar manager.html

En tu archivo `templates/manager.html`, busca y reemplaza:

**Línea ~22 (botón en header):**
```html
<!-- ANTES: -->
<a href="http://localhost:5000" target="_blank" class="btn btn-secondary">

<!-- DESPUÉS: -->
<a href="https://descargador-videos-XXXX.onrender.com" target="_blank" class="btn btn-secondary">
```

**Línea ~508 (función abrirDescargador):**
```javascript
// ANTES:
function abrirDescargador(url) {
    window.open(`http://localhost:5000?url=${encodeURIComponent(url)}`, '_blank');
}

// DESPUÉS:
function abrirDescargador(url) {
    window.open(`https://descargador-videos-XXXX.onrender.com?url=${encodeURIComponent(url)}`, '_blank');
}
```

**⚠️ IMPORTANTE:** Reemplaza `XXXX` con tu URL real de Render.

### Paso 5.2: Subir cambios a GitHub

**Opción A: Desde GitHub.com**

1. Ve a tu repositorio en GitHub
2. Click en `templates/manager.html`
3. Click en el ícono de lápiz (Edit)
4. Haz los cambios
5. Scroll abajo, mensaje: `Actualizar URLs para producción`
6. Click **"Commit changes"**

**Opción B: Desde GitHub Desktop**

1. Abre GitHub Desktop
2. Verás los cambios en `manager.html`
3. Escribe mensaje: `Actualizar URLs para producción`
4. Click **"Commit to main"**
5. Click **"Push origin"**

✅ Render detectará el cambio automáticamente y hará **redeploy** (tarda ~3 minutos).

---

## 💾 PARTE 6: Base de Datos Persistente

Por defecto, Render **borra archivos** al hacer redeploy. Necesitamos un disco persistente.

### Paso 6.1: Agregar disco al Gestor

1. Ve a tu servicio **"gestor-videos"** en Render
2. Click en la pestaña **"Disks"**
3. Click **"Add Disk"**
4. Configuración:
   - **Name:** `database-disk`
   - **Mount Path:** `/data`
   - **Size:** `1 GB` (gratis hasta 1GB)
5. Click **"Save"**

### Paso 6.2: Actualizar código para usar disco

En `manager_app.py`, busca la línea que dice:

```python
DATABASE = 'videos_database.db'
```

Reemplázala por:

```python
# Base de datos persistente en disco de Render
DATABASE = '/data/videos_database.db' if os.path.exists('/data') else 'videos_database.db'
```

### Paso 6.3: Subir cambio

1. Sube el cambio a GitHub (como en Paso 5.2)
2. Render hará redeploy
3. Ahora la base de datos NO se borrará al redeploy

---

## ✅ PARTE 7: Verificar que Todo Funciona

### Test 1: Acceder al Gestor

1. Abre tu URL del gestor: `https://gestor-videos-XXXX.onrender.com`
2. ¿Se ve la interfaz? ✅
3. ¿Puedes hacer búsquedas? ✅

### Test 2: Agregar un Video

1. Click en **"Agregar Video"**
2. Pega una URL de YouTube
3. Llena el formulario
4. Click "Guardar"
5. ¿Aparece en la lista? ✅

### Test 3: Acceder al Descargador

1. En el gestor, click en **"Descargador"** (arriba)
2. ¿Se abre el descargador en nueva pestaña? ✅
3. ¿Puedes pegar una URL? ✅
4. ¿Se carga el preview? ✅

### Test 4: Descargar desde una Card

1. En el gestor, busca un video
2. Click en **"Descargar"** en una card
3. ¿Se abre el descargador con la URL pre-cargada? ✅
4. ¿Puedes seleccionar calidad? ✅
5. ¿Puedes descargar? ✅

---

## 🎨 PARTE 8: Dominio Personalizado (Opcional)

### Opción A: Usar subdominio de Render (Gratis)

Ya lo tienes:
- Gestor: `https://gestor-videos-XXXX.onrender.com`
- Descargador: `https://descargador-videos-XXXX.onrender.com`

### Opción B: Tu propio dominio

Si tienes un dominio (ej: `videos.tudominio.com`):

1. En Render: Settings → **"Custom Domain"**
2. Agrega tu dominio: `videos.tudominio.com`
3. Render te dará un **CNAME** como:
   ```
   gestor-videos-XXXX.onrender.com
   ```
4. En Hostinger (tu proveedor de dominio):
   - Panel de control → DNS/Dominios
   - Agrega registro **CNAME**:
     - Host: `videos`
     - Apunta a: `gestor-videos-XXXX.onrender.com`
5. Espera propagación (15 min - 24 horas)

Repite para el descargador con `descargador.tudominio.com`.

---

## 📊 PARTE 9: Monitorear tu Aplicación

### Ver Logs

1. En Render, entra a tu servicio
2. Pestaña **"Logs"**
3. Verás todo lo que imprime tu app en tiempo real

### Ver Métricas

1. Pestaña **"Metrics"**
2. Verás:
   - CPU usage
   - Memory usage
   - Requests/segundo

### Ver Eventos

1. Pestaña **"Events"**
2. Historial de deploys
3. Cambios y errores

---

## 💰 Costos y Límites

### Plan Gratuito (lo que tienes ahora):

**Incluye:**
- ✅ 750 horas/mes (= ~31 días para 1 servicio)
- ✅ SSL automático (HTTPS)
- ✅ 1 GB de disco persistente gratis
- ✅ 512 MB de RAM

**Limitaciones:**
- ⏳ Después de 15 minutos sin uso, entra en "sleep"
  - Primera visita tarda 30-60 segundos en "despertar"
  - Luego funciona normal
- 🔢 Máximo 2 servicios gratuitos simultáneos

### Plan Starter ($7/mes por servicio):

**Mejoras:**
- ✅ Sin sleep (siempre activo)
- ✅ Más RAM (512 MB)
- ✅ Soporte prioritario

### Recomendación:

- **Empezar con plan gratuito** para probar
- Si el equipo lo usa mucho, upgrade a Starter

---

## 🔧 Troubleshooting

### Problema 1: Deploy falla

**Solución:**
1. Ve a la pestaña **"Events"**
2. Click en el deploy fallido
3. Lee el error
4. Errores comunes:
   - `ModuleNotFoundError: No module named 'X'` → Falta en `requirements.txt`
   - `Port already in use` → Render asigna puerto automático, asegúrate de usar `os.environ.get('PORT')`

### Problema 2: App carga muy lento

**Causa:** Primera carga tras 15 min de inactividad (plan gratuito).

**Solución:**
- Es normal en plan gratuito
- Upgrade a Starter para que esté siempre activo

### Problema 3: Base de datos se borra

**Causa:** No configuraste disco persistente.

**Solución:**
- Sigue **PARTE 6** arriba
- Verifica que el mount path sea `/data`
- Verifica que el código use `/data/videos_database.db`

### Problema 4: Descargador no abre

**Causa:** URL no actualizada en `manager.html`.

**Solución:**
- Verifica que hayas reemplazado `localhost:5000` con tu URL real de Render
- Verifica que el descargador esté "live" en Render

### Problema 5: No puedo descargar videos

**Causa:** yt-dlp puede estar bloqueado o necesita cookies.

**Solución:**
1. Ve a los logs del descargador
2. Si ves errores de YouTube:
   - Puede necesitar cookies (más complejo)
   - Verifica que yt-dlp esté actualizado en requirements.txt

---

## 📋 Checklist Final

Antes de compartir con tu equipo:

- [ ] Gestor deployed y funcionando
- [ ] Descargador deployed y funcionando
- [ ] URLs actualizadas en `manager.html`
- [ ] Disco persistente configurado
- [ ] Probado agregar videos
- [ ] Probado buscar videos
- [ ] Probado descargar desde card
- [ ] Probado acceso directo al descargador
- [ ] URLs guardadas en documento seguro

---

## 🎉 ¡Listo para Compartir!

Tu sistema ya está en línea. Comparte estas URLs con tu equipo:

**Gestor (Principal):**
```
https://gestor-videos-XXXX.onrender.com
```

**Descargador (Directo):**
```
https://descargador-videos-XXXX.onrender.com
```

**Instrucciones para el equipo:**

1. Entra al gestor
2. Busca videos por título, etiquetas, sede, etc.
3. Click en "Descargar" abre el descargador automáticamente
4. Selecciona calidad y descarga

---

## 📞 Soporte

**Si algo falla:**

1. Revisa los **Logs** en Render
2. Verifica que todas las **URLs** estén actualizadas
3. Verifica que el **disco persistente** esté montado

**Archivos clave:**
- `manager_app.py` - Backend gestor
- `downloader_app_v3.py` - Backend descargador  
- `templates/manager.html` - Frontend gestor (URLs aquí)
- `templates/downloader.html` - Frontend descargador

---

**¡Tu sistema está en la nube! 🚀**

Cualquier duda en el proceso, pregúntame paso por paso.

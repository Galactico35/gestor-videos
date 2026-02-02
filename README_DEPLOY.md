# 📦 Paquete para Deploy en Render.com

## 📋 Contenido

Este paquete contiene todo lo necesario para subir tu sistema a Render.com.

### Archivos incluidos:

```
deploy-render/
├── manager_app.py              ← Backend del gestor
├── downloader_app_v3.py        ← Backend del descargador
├── start_manager.py            ← Script inicio gestor
├── start_downloader.py         ← Script inicio descargador
├── requirements.txt            ← Dependencias Python
├── gitignore_template.txt      ← Renombrar a .gitignore
├── templates/
│   ├── manager.html           ← Frontend gestor
│   └── downloader.html        ← Frontend descargador
└── GUIA_DEPLOY_RENDER.md       ← GUÍA COMPLETA PASO A PASO
```

---

## 🚀 Inicio Rápido

### 1. Lee la guía completa

**→ Abre:** `GUIA_DEPLOY_RENDER.md`

Esta guía tiene **TODO** el proceso paso a paso con capturas y explicaciones detalladas.

### 2. Pasos resumidos:

1. **Crear cuenta en Render.com** (gratis)
2. **Subir archivos a GitHub**
3. **Crear 2 servicios web en Render:**
   - Gestor (manager)
   - Descargador (downloader)
4. **Conectar gestor con descargador**
5. **Configurar base de datos persistente**
6. **¡Listo!**

---

## ⚠️ Importante

### Antes de subir a GitHub:

1. **Renombra** `gitignore_template.txt` → `.gitignore`
2. **Verifica** que tengas todos los archivos listados arriba
3. **Asegúrate** de incluir la carpeta `templates` completa

### Después del deploy:

**DEBES actualizar 2 URLs en `manager.html`:**

Busca y reemplaza `localhost:5000` con tu URL real del descargador en Render.

**Ejemplo:**
```html
<!-- Línea 22 -->
<a href="https://TU-DESCARGADOR.onrender.com" ...>

<!-- Línea 508 -->
window.open(`https://TU-DESCARGADOR.onrender.com?url=...`, ...);
```

---

## 💡 Tips

- **Primera vez:** Tarda 5-10 minutos en hacer deploy
- **Plan gratuito:** Suficiente para empezar
- **Sleep mode:** Primera carga tras 15 min de inactividad tarda 30-60 seg
- **Upgrade:** Si el equipo lo usa mucho, considera Starter ($7/mes)

---

## 📞 Soporte

Si tienes dudas durante el proceso:

1. **Lee la guía completa** - Tiene troubleshooting
2. **Revisa los logs** en Render
3. **Verifica las URLs** estén actualizadas

---

**¡Todo está listo para subir a la nube! 🚀**

Sigue la guía paso a paso y en 30 minutos tendrás tu sistema en línea.

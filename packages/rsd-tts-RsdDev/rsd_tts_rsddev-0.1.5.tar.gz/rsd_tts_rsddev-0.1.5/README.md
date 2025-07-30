# rsd_tts · [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Libreria Python per sintesi vocale in italiana (Windows 10/11)**  
*Pulizia automatica del testo e output vocale chiaro*
---

## ⚠️ Requisiti di sistema
- **Solo Windows 10/11**  
- Voice pack italiano installato (es. "Elsa" o "Cosimo")  
- Python 3.7+  

*(Non supporta macOS/Linux)*  
---

✨ **Funzionalità**:
- ✅ Pulizia automatica di markdown, emoji e caratteri speciali
- ✅ Ottimizzato per la pronuncia italiana
- ✅ Regolazione di velocità/volume
- ✅ Integrazione nativa con SAPI (Windows)
- ✅ Pulizia automatica della domanda per risposte AI
  

Installazione:
pip install rsd-tts-RsdDev

Uso:
```python
from rsd_tts import parla

[Valori default]
parla("Ciao mondo! :)")  # Pronuncia "Ciao mondo sorriso"

[Controllo velocità e volume]
parla("Funziona perfettamente! :)", velocità=-2, volume=90)


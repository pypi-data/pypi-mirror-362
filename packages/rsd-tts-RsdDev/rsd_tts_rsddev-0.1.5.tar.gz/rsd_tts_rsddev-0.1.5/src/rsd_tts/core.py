import win32com.client
import re
import sys

# Controllo sistema operativo
if not sys.platform.startswith("win"):
    raise OSError("Questa libreria richiede Windows 10/11 con voice pack italiano installato.")

def pulisci_testo(testo):
    """Pulisce il testo da caratteri speciali e formattazioni indesiderate"""
    # Rimozione di markdown e formattazioni speciali
    testo = re.sub(r'\*\*([^*]+)\*\*', r'\1', testo)  # **grassetto**
    testo = re.sub(r'\*([^*]+)\*', r'\1', testo)      # *corsivo*
    testo = re.sub(r'`([^`]+)`', r'\1', testo)        # `codice`
    testo = re.sub(r'~~([^~]+)~~', r'\1', testo)      # ~~barrato~~
    
    # Rimozione di caratteri speciali isolati
    testo = re.sub(r'[^\w\s.,!?;:\'\"()\-—+&@#%$€£]', ' ', testo)
    
    # Sostituzione di sequenze speciali
    sostituzioni = {
        r'\.{3,}': ' punto punto punto ',   # ...
        r':-\)|:\)': ' sorriso ',            # :-) :)
        r':\(|:-\(': ' triste ',             # :( : -(
        r';\)|;-\)': ' occhiolino ',         # ;) ;-)
        r':D|:-D': ' risata ',               # :D :-D
        r'<3': ' cuore ',                    # <3
        r'->': ' diventa ',                  # ->
        r'<-': ' da ',                       # <-
        r'&': ' e ',                         # &
        r'@': ' chiocciola ',                # @
        r'#': ' hashtag ',                   # #
        r'\*': ' asterisco ',                # * isolato
        r'\/': ' barra ',                    # / isolato
    }
    
    for pattern, repl in sostituzioni.items():
        testo = re.sub(pattern, repl, testo)
    
    # Gestione di numeri e simboli combinati
    testo = re.sub(r'(\d+)\s*([x×])\s*(\d+)', r'\1 per \3', testo)  # 10x10 → 10 per 10
    testo = re.sub(r'(\d+)\s*%', r'\1 percento', testo)             # 50% → 50 percento
    
    # Normalizzazione spazi
    testo = re.sub(r'\s+', ' ', testo).strip()
    
    return testo

def parla(testo, velocità=0, volume=100, is_ai_response=True):
    """Pronuncia il testo pulito in italiano.
    
    Args:
        testo (str): Testo da pronunciare
        velocità (int): Da -10 (lento) a 10 (veloce)
        volume (int): Da 0 (muto) a 100 (massimo)
        is_ai_response (bool): Se True, applica pulizia aggiuntiva per risposte AI
    """
    testo_pulito = pulisci_testo(testo)
    
    if is_ai_response:
        testo_pulito = re.sub(r'\?.*$', '.', testo_pulito)  # Rimuove domande
    
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = velocità
    speaker.Volume = volume
    speaker.Speak(testo_pulito)

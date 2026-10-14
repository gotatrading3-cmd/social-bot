"""Clonage de VOTRE voix (avec votre accord) avec Chatterbox multilingue (licence MIT) : tourne chez GitHub, pas sur le PC.
Usage : python voix_clone.py SORTIE.wav "texte a dire" [ref1|ref2|ref3]"""
import io, os, sys, tarfile, tempfile
from cryptography.fernet import Fernet

def charger_refs(enc_path, key):
    d = tempfile.mkdtemp(prefix="vref_")
    data = Fernet(key.encode()).decrypt(open(enc_path, "rb").read())
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
        t.extractall(d)
    return d

def batch(fichiers, outdir, ref="ref1"):
    """fichiers : JSON [{"id": ..., "text": ...}] ; ecrit outdir/<id>.wav pour chaque phrase (le texte est deja ecrit comme il se prononce)."""
    import json
    refs = charger_refs(os.environ.get("VOICE_REF_ENC", "voice/voix_ref.enc"), os.environ["VOICE_KEY"])
    import torch, torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    os.makedirs(outdir, exist_ok=True)
    for fp in fichiers:
        for it in json.load(open(fp, encoding="utf-8")):
            dst = os.path.join(outdir, it["id"] + ".wav")
            if os.path.exists(dst):
                continue
            wav = model.generate(it["text"], language_id="fr", audio_prompt_path=os.path.join(refs, ref + ".wav"),
                                 exaggeration=float(os.environ.get("EXAG", "0.85")), cfg_weight=float(os.environ.get("CFG", "0.20")))
            ta.save(dst, wav, model.sr)
            print("fait", it["id"], flush=True)


def variantes(outdir, textes, ref="ref1"):
    """Essai de plusieurs reglages d'energie : exaggeration (intensite de l'expression) et cfg_weight (plus bas = debit plus rapide)."""
    refs = charger_refs(os.environ.get("VOICE_REF_ENC", "voice/voix_ref.enc"), os.environ["VOICE_KEY"])
    import torch, torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    os.makedirs(outdir, exist_ok=True)
    for nom, ex, cfg in (("A", 0.65, 0.30), ("B", 0.85, 0.20), ("C", 1.0, 0.15)):
        for i, t in enumerate(textes.split("||")):
            wav = model.generate(t.strip(), language_id="fr", audio_prompt_path=os.path.join(refs, ref + ".wav"), exaggeration=ex, cfg_weight=cfg)
            ta.save(os.path.join(outdir, "var%s_%d.wav" % (nom, i + 1)), wav, model.sr)
            print("fait", nom, i + 1, flush=True)


def main():
    if sys.argv[1] == "--variantes":
        return variantes(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "ref1")
    if sys.argv[1] == "--json":
        return batch(sys.argv[3:], sys.argv[2])
    out, textes = sys.argv[1], sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) > 3 else "ref1"
    refs = charger_refs(os.environ.get("VOICE_REF_ENC", "voice/voix_ref.enc"), os.environ["VOICE_KEY"])
    import torch, torchaudio as ta
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    for i, t in enumerate(textes.split("||")):
        wav = model.generate(t.strip(), language_id="fr", audio_prompt_path=os.path.join(refs, ref + ".wav"),
                             exaggeration=0.45, cfg_weight=0.4)
        ta.save(out.replace(".wav", "_%d.wav" % (i + 1)), wav, model.sr)
        print("fait", i + 1, flush=True)

if __name__ == "__main__":
    main()

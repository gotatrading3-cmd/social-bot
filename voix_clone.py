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

def main():
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

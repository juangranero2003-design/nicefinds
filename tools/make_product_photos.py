"""Genera fotos de producto (products/<file>.jpg) con Cloudflare Workers AI.

Lo corre la GitHub Action .github/workflows/product-photos.yml.
Para cada producto de pins/log.csv que todavía no tiene foto:
  1. Busca su prompt en products/prompts.csv (si no hay, arma uno con el título).
  2. Le agrega el estilo común y llama al modelo FLUX.2 klein 9B de Cloudflare,
     pasándole una foto de referencia (products/mixer-cart.jpg, hecha con Canva)
     para que copie su luz, colores y ambiente.
  3. Guarda la imagen como JPG cuadrado de 1000x1000 (< 200 KB) en
     products/pending/. La web NO muestra esa carpeta: la tarea diaria revisa
     cada foto y, solo si se parece al producto real, la mueve a products/.

Necesita dos variables de entorno (secretos de GitHub):
  CF_ACCOUNT_ID  y  CF_API_TOKEN
"""
import base64, csv, io, json, os, pathlib, sys, urllib.request, uuid

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = "@cf/black-forest-labs/flux-2-klein-9b"
STYLE_REFERENCE = ROOT / "products" / "mixer-cart.jpg"  # foto de Canva usada como guía de estilo
STYLE = ("Candid photo taken with a smartphone in a real, lived-in American home, natural daylight, "
         "true-to-life colors, realistic textures with small everyday imperfections, slightly casual framing, "
         "a few ordinary items around, no studio look, no CGI, no glossy render, no text, no logos, "
         "no brand names, no people's faces. Square 1:1 photo.")
MAX_PER_RUN = 6  # tope por ejecución (cada foto gasta ~1.400 de las 10.000 neuronas diarias gratis)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def reference_bytes():
    """La foto de referencia achicada a 512x512 (gasta menos cupo)."""
    if not STYLE_REFERENCE.exists():
        return None
    im = Image.open(STYLE_REFERENCE).convert("RGB").resize((512, 512), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return buf.getvalue()


def multipart(fields, files):
    """Arma un cuerpo multipart/form-data a mano (sin librerías extra)."""
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    for name, data in files.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{name}.jpg"\r\n'
                     f'Content-Type: image/jpeg\r\n\r\n'.encode() + data + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def generate(prompt, account, token, ref):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{MODEL}"
    files = {}
    if ref:
        files["input_image_0"] = ref
        prompt = ("Image 0 is ONLY a reference for photographic style: soft window lighting, "
                  "muted cream and sage green color grading, warm wood tones, gentle contrast. "
                  "Do NOT copy any object, furniture, appliance, room or composition from image 0. "
                  "Create a completely new scene showing only this subject: " + prompt)
    body, ctype = multipart({"prompt": prompt, "width": 1024, "height": 1024}, files)
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}", "Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=180) as r:
        payload, kind = r.read(), r.headers.get("Content-Type", "")
    if kind.startswith("image/"):
        return payload
    data = json.loads(payload)
    if not data.get("success", True):
        raise RuntimeError(data.get("errors"))
    result = data.get("result", data)
    return base64.b64decode(result["image"])


def save_jpg(raw, dest):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    side = min(im.size)  # recorte cuadrado centrado
    left, top = (im.width - side) // 2, (im.height - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize((1000, 1000), Image.LANCZOS)
    for q in (85, 78, 70, 62):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() < 200_000:
            break
    dest.write_bytes(buf.getvalue())


def main():
    account, token = os.environ.get("CF_ACCOUNT_ID"), os.environ.get("CF_API_TOKEN")
    if not account or not token:
        sys.exit("Faltan los secretos CF_ACCOUNT_ID / CF_API_TOKEN")
    prompts = {r["file"]: r["prompt"] for r in read_csv(ROOT / "products/prompts.csv")}
    ref = reference_bytes()
    done = 0
    pending_dir = ROOT / "products" / "pending"
    pending_dir.mkdir(exist_ok=True)
    for row in read_csv(ROOT / "pins/log.csv"):
        published = ROOT / "products" / f"{row['file']}.jpg"
        dest = pending_dir / f"{row['file']}.jpg"
        if published.exists() or dest.exists():  # ya publicada o esperando revisión
            continue
        if done >= MAX_PER_RUN:
            print("Tope por ejecución alcanzado; el resto queda para la próxima.")
            break
        base = prompts.get(row["file"]) or f"{row['title']} shown in a real home setting."
        print(f"Generando {dest.name} ...")
        try:
            save_jpg(generate(f"{base} {STYLE}", account, token, ref), dest)
            done += 1
        except Exception as e:  # sigue con los demás si uno falla
            print(f"  error con {row['file']}: {e}")
    print(f"Listo: {done} foto(s) nueva(s).")


if __name__ == "__main__":
    main()

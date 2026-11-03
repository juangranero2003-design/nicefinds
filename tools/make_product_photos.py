"""Genera fotos de producto (products/<file>.jpg) con Cloudflare Workers AI.

Lo corre la GitHub Action .github/workflows/product-photos.yml.
Para cada producto de pins/log.csv que todavía no tiene foto:
  1. Busca su prompt en products/prompts.csv (si no hay, arma uno con el título).
  2. Le agrega el estilo común y llama al modelo FLUX de Cloudflare.
  3. Guarda la imagen como JPG cuadrado de 1000x1000 (< 200 KB).

Necesita dos variables de entorno (secretos de GitHub):
  CF_ACCOUNT_ID  y  CF_API_TOKEN
"""
import base64, csv, io, json, os, pathlib, sys, urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = "@cf/black-forest-labs/flux-1-schnell"
STYLE = ("Photorealistic lifestyle photo, square 1:1 format, warm natural window light, "
         "soft neutral palette (cream, warm wood, sage green), shallow depth of field, "
         "cozy American home, no text, no logos, no brand names, no people's faces.")
MAX_PER_RUN = 10  # tope de seguridad para no gastar de más


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate(prompt, account, token):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{MODEL}"
    body = json.dumps({"prompt": prompt, "steps": 8}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    if not data.get("success", True):
        raise RuntimeError(data.get("errors"))
    return base64.b64decode(data["result"]["image"])


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
    done = 0
    for row in read_csv(ROOT / "pins/log.csv"):
        dest = ROOT / "products" / f"{row['file']}.jpg"
        if dest.exists():
            continue
        if done >= MAX_PER_RUN:
            print("Tope por ejecución alcanzado; el resto queda para la próxima.")
            break
        base = prompts.get(row["file"]) or f"{row['title']} shown in a real home setting."
        print(f"Generando {dest.name} ...")
        try:
            save_jpg(generate(f"{base} {STYLE}", account, token), dest)
            done += 1
        except Exception as e:  # sigue con los demás si uno falla
            print(f"  error con {row['file']}: {e}")
    print(f"Listo: {done} foto(s) nueva(s).")


if __name__ == "__main__":
    main()

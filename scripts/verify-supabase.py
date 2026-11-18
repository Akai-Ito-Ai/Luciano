"""Comprueba la conexión; la prueba opcional libera sus propias reservas al terminar."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
import uuid
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-reservations", action="store_true")
    args = parser.parse_args()
    source = (ROOT / "config.js").read_text()
    block = re.search(r"supabase\s*:\s*\{(.*?)\}", source, re.S).group(1)

    def field(name):
        return re.search(r"\b" + name + r"\s*:\s*['\"]([^'\"]*)['\"]", block).group(1)

    base, key, event = field("url").rstrip("/"), field("publishableKey"), field("eventId")
    assert re.fullmatch(r"https://[a-z0-9]+\.supabase\.co", base), "Revisar la URL de proyecto."
    assert key.startswith("sb_publishable_") or key.startswith("eyJ"), "Se necesita una clave pública."
    headers = {"Content-Type": "application/json", "apikey": key}
    if key.startswith("eyJ"):
        headers["Authorization"] = "Bearer " + key

    def rpc(name, params=None):
        request = urllib.request.Request(base + "/rest/v1/rpc/" + name,
                                         data=json.dumps({"p_event_id": event, **(params or {})}).encode(),
                                         headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            result = json.loads(error.read())
            raise RuntimeError(f"{name}: HTTP {error.code}, {result.get('message', 'error del servidor')}") from None

    expected = json.loads((ROOT / "supabase/regalos-luciano.json").read_text())
    actual = rpc("invitation_available_gifts")
    assert [gift["id"] for gift in actual] == [gift["id"] for gift in expected], "La lista u orden no coincide con el Excel."
    for gift, imported in zip(actual, expected):
        for key_name in ("name", "description", "category", "icon", "color", "image_url", "product_url"):
            assert gift[key_name] == imported[key_name], f"Revisar {key_name} de {imported['name']}."
    report = {"date": datetime.now(ZoneInfo("America/Bogota")).date().isoformat(), "event_id": event, "connection": "ok", "gifts": len(actual),
              "categories": dict(Counter(gift["category"] for gift in actual)), "matches_import": True}
    if args.test_reservations:
        gift_id = actual[0]["id"]
        tokens = [str(uuid.uuid4()), str(uuid.uuid4())]
        results = None
        try:
            def reserve(index):
                return rpc("invitation_reserve_gift", {"p_gift_id": gift_id, "p_token": tokens[index],
                                                       "p_name": "Prueba técnica " + str(index + 1),
                                                       "p_email": f"prueba-{index + 1}@example.com"})
            with ThreadPoolExecutor(max_workers=2) as executor:
                results = list(executor.map(reserve, range(2)))
            assert sorted(results) == [False, True], "Se esperaba una sola reserva exitosa."
            winner, loser = results.index(True), results.index(False)
            assert [gift["id"] for gift in rpc("invitation_my_gifts", {"p_tokens": [tokens[winner]]})] == [gift_id]
            assert rpc("invitation_my_gifts", {"p_tokens": [tokens[loser]]}) == []
            assert gift_id not in [gift["id"] for gift in rpc("invitation_available_gifts")]
        finally:
            # Los tokens solo pueden cancelar las reservas de esta prueba.
            for token in tokens:
                rpc("invitation_cancel_gift", {"p_gift_id": gift_id, "p_token": token})
        restored = rpc("invitation_available_gifts")
        assert [gift["id"] for gift in restored] == [gift["id"] for gift in actual], "Revisar la restauración de la lista."
        report["reservation_test"] = {"simultaneous_attempts": 2, "successful": sum(results),
                                      "hidden_while_reserved": True, "own_reservations_checked": True,
                                      "cancelled_test_reservation": True, "available_after_test": len(restored)}
    report["private_tables_blocked"] = {}
    for table in ("invitation_rsvps", "invitation_gift_reservations"):
        request = urllib.request.Request(base + "/rest/v1/" + table + "?select=*&limit=0", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
        except urllib.error.HTTPError as error:
            status = error.code
        report["private_tables_blocked"][table] = status in (401, 403)
        assert status in (401, 403), "Revisar los permisos de " + table
    (ROOT / "supabase/verificacion-conexion.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""Sistema permanente de ranking em JSON."""

import json
import os
from datetime import datetime

from utils.constants import RANKING_FILE, SAVE_DIR


class RankingManager:
    """Gerencia top 10 recordes persistentes."""

    MAX_ENTRIES = 10

    def __init__(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.entries: list[dict] = []
        self.load()

    def load(self):
        """Carrega ranking do arquivo JSON."""
        if os.path.exists(RANKING_FILE):
            try:
                with open(RANKING_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = data.get("ranking", [])
            except (json.JSONDecodeError, OSError):
                self.entries = []
        else:
            self.entries = []

    def save(self):
        """Persiste ranking em disco."""
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump({"ranking": self.entries}, f, ensure_ascii=False, indent=2)

    def add_entry(self, name: str, score: int) -> bool:
        """Adiciona entrada se qualificar para o top 10."""
        name = name.strip()[:20] or "Anônimo"
        entry = {
            "name": name,
            "score": score,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[: self.MAX_ENTRIES]
        self.save()
        return any(e["name"] == name and e["score"] == score for e in self.entries)

    def get_high_score(self) -> int:
        """Retorna maior pontuação registrada."""
        if not self.entries:
            return 0
        return self.entries[0]["score"]

    def is_high_score(self, score: int) -> bool:
        """Verifica se pontuação entra no ranking."""
        if len(self.entries) < self.MAX_ENTRIES:
            return score > 0
        return score > self.entries[-1]["score"]

    def get_entries(self) -> list[dict]:
        """Retorna lista ordenada de recordes."""
        return list(self.entries)

import re
from pydantic import BaseModel
from xync_schema.models import PmRep


class PmUni(BaseModel):
    norm: str
    acronym: str = None
    country: str = None
    alias: str = None
    extra: str = None
    bank: bool = None


class PmUnifier:
    pms: dict[str, PmUni] = {}  # {origin: normalized}

    re_bank = [
        r"^bank (?!of )|bank$",
        r" banka$",
        r" bankas$",
        r" bankası$",
        r" banca$",
        r"^banco(?! de | del )| banco$",
    ]
    re_extra = [
        r"\(card\)$|\bpay$|\bmoney$|\bwallet$|\bcash$|\bmobile$",
        r"b\.s\.c\.|k\.s\.c|s\.a\.a\.?$|s\.a\.?$| sv$| gt$",
    ]
    re_glut = [
        r"\.io$|\.com\b",
        r"l'|d’|d′|d'",
    ]
    i18n_map = {
        " - ": "-",
        " & ": "&",
        "nationale": "national",
        "а": "a",
        "á": "a",
        "â": "a",
        "о": "o",
        "ó": "o",
        "ō": "o",
        "ú": "u",
        "ü": "u",
        "ų": "u",
        "с": "c",
        "č": "c",
        "ç": "c",
        "é": "e",
        "è": "e",
        "ş": "s",
        "š": "s",
        "ř": "r",
        "í": "i",
    }
    rms = ":`'’′"

    def __init__(self, countries: list[tuple[str, str]], pm_reps: list[PmRep]):
        self.pm_map = {p.src: p.trgt for p in pm_reps}
        self.cts = countries

    def countries(self, name: str):
        for ct, st in self.cts:
            # Если имя кончается на "Название_страны" в скобках
            if (
                ct
                and self.pms[name].norm.endswith((ct + ")", ct))
                and not self.pms[name].norm.endswith((" of " + ct, " of the " + ct, " and " + ct, " de " + ct))
            ):
                self.pms[name].norm = self.pms[name].norm.replace(ct, "")
                self.pms[name].country = ct
                self.clear(name)
                return
            elif st and self.pms[name].norm.endswith(f" ({st})"):
                self.pms[name].norm = self.pms[name].norm.replace(f" ({st})", "")
                self.pms[name].country = ct
                return

    def extra(self, name: str):
        for r in self.re_extra:
            if match := re.search(r, self.pms[name].norm):
                self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
                self.pms[name].extra = match.group()
                self.clear(name)
                return

    def alias(self, name: str):
        if match := re.search(r"\(.+\)$", self.pms[name].norm):
            self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
            self.pms[name].alias = match.group()[1:-1]
            self.clear(name)
            return

    def bank(self, name: str):
        for r in self.re_bank:
            if (match := re.search(r, self.pms[name].norm)) and match.group() != self.pms[name].norm:
                self.pms[name].norm = self.pms[name].norm.replace(match.group(), "")
                self.pms[name].bank = True
                self.clear(name)
                return

    def acro(self, name: str):
        acr = "".join(
            wrd[0]
            for wrd in self.pms[name].norm.split(" ")
            if not wrd.isupper()
            and not wrd.startswith(("(", "the"))
            and len(wrd) > 2
            or (len(wrd) > 1 and wrd.istitle())
        ).upper()
        if len(acr) >= 2 and (
            f"({acr})" in self.pms[name].norm
            or self.pms[name].norm.startswith((acr + " ", acr + ":"))
            or self.pms[name].norm.endswith(" " + acr)
        ):
            self.pms[name].norm = self.pms[name].norm.replace(acr, "", 1)
            self.pms[name].acronym = acr
            self.clear(name)

    def slim(self, name: str):
        for rm in self.re_glut:
            self.pms[name].norm = re.sub(rm, "", self.pms[name].norm)

    def i18n(self, name: str):
        for src, trgt in self.i18n_map.items():
            self.pms[name].norm = self.pms[name].norm.replace(src, trgt)

    def clear(self, name: str):
        self.pms[name].norm = self.pms[name].norm.replace("()", "").replace("  ", " ").strip(" -:.")

    def __call__(self, s: str) -> PmUni:
        # если в словаре замен есть текущее назвние - меняем, иначе берем строку до запятой
        self.pms[s] = PmUni(norm=self.pm_map.get(s, s.split(",")[0]))
        # вырезаем мусорные добавки
        self.slim(s)
        # заменяем локальные символы на англ:
        self.i18n(s)
        # находим и вырезаем аббревиатуру, если есть
        self.acro(s)
        # уменьшаем все буквы
        self.pms[s].norm = self.pms[s].norm.lower()
        # находим и вырезаем страны, если есть
        self.countries(s)
        self.bank(s)
        self.extra(s)
        self.alias(s)
        self.bank(s)
        self.countries(s)
        self.extra(s)
        # вырезаем каждый символ rms
        [self.pms[s].norm.replace(rm, "") for rm in self.rms]
        #
        if not self.pms[s].norm and self.pms[s].bank:
            self.pms[s].norm = "bank"

        return self.pms[s]

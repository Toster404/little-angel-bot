import re

from datetime import timedelta

time_regex = re.compile(r"([0-9]+)(секунда|секунды|секунд|сек|мин|минута|минут|минуты|час|часа|часов|дней|дня|день|нед|неделя|недели|недель|месяц|месяца|месяцев|год|года|лет|[смчднгл])")
time_dict = {"ч": 3600, "с": 1, "м": 60, "д": 86400, "секунда": 1, "секунды": 1, "секунд": 1, "сек": 1, "мин": 60, "минута": 60, "минут": 60, "минуты": 60, "час": 3600, "часа": 3600, "часов": 3600, "день": 86400, "дня": 86400, "дней": 86400, "н": 604800, "нед": 604800, "неделя": 604800, "недели": 604800, "недель": 604800, "мес": 2592000, "месяц": 2592000, "месяца": 2592000, "месяцев": 2592000, "г": 31104000, "год": 31104000, "года": 31104000, "лет": 31104000, "л": 31104000}

def verbose_timedelta(t: timedelta) -> str:
    cif_str = ""
    if t >= timedelta(days=365):
        cif = int(t.days / 365)
        t = t - timedelta(days=cif * 365)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} год "
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} года "
        else:
            cif_str += f"{cif} лет "
    if t < timedelta(days=365) and t >= timedelta(days=30):
        cif = int(t.days / 30)
        t = t - timedelta(days=cif * 30)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} месяц "
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} месяца "
        else:
            cif_str += f"{cif} месяцев "
    if t < timedelta(days=30) and t >= timedelta(days=1):
        cif = t.days
        t = t - timedelta(days=cif)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} день "
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} дня "
        else:
            cif_str += f"{cif} дней "
    if t < timedelta(days=1) and t >= timedelta(hours=1):
        cif = int(t.total_seconds() / 3600)
        t = t - timedelta(hours=cif)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} час "
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} часа "
        else:
            cif_str += f"{cif} часов "
    if t < timedelta(hours=1) and t >= timedelta(minutes=1):
        cif = int(t.total_seconds() / 60)
        t = t - timedelta(minutes=cif)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} минуту "
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} минуты "
        else:
            cif_str += f"{cif} минут "
    if t < timedelta(minutes=1) and t >= timedelta(seconds=1):
        cif = t.seconds
        t = t - timedelta(seconds=cif)
        if cif in [1, 21, 31, 41, 51]:
            cif_str += f"{cif} секунду"
        elif cif in [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54]:
            cif_str += f"{cif} секунды"
        else:
            cif_str += f"{cif} секунд"
    if cif_str and cif_str[-1] == " ":
        cif_str = cif_str[:-1]
    return cif_str
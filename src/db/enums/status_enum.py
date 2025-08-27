import enum


class StatusEnum(enum.Enum):
    PLANNED = "запланировано"
    READING = "читаю"
    FINISHED = "Прочитал"
    ABANDONED = "бросил"

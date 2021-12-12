from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT_MESSAGE: str = ('Тип тренировки: {training_type}; '
                         'Длительность: {duration:.3f} ч.; '
                         'Дистанция: {distance:.3f} км; '
                         'Ср. скорость: {speed:.3f} км/ч; '
                         'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получение сообщения о тренировке"""

        return self.TEXT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Создаем объект и сохраняем в нем значения"""
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_kmh: float = self.get_distance() / self.duration_h
        return speed_kmh

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не переопределен в дочернем классе')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULT: int = 18
    CALORIES_SUBTRACT_SPEED: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories_kcal = (
            (
                self.CALORIES_MEAN_SPEED_MULT
                * self.get_mean_speed()
                - self.CALORIES_SUBTRACT_SPEED
            )
            * self.weight_kg / self.M_IN_KM
            * self.duration_h * self.MIN_IN_H
        )
        return spent_calories_kcal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIE_WEIGHT_MULT: float = 0.035
    CALORIE_CONST_FACTOR: float = 0.029

    def __init__(self, action: int,
                 duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories_kcal: float = ((
            self.CALORIE_WEIGHT_MULT
            * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_m)
            * self.CALORIE_CONST_FACTOR
            * self.weight_kg) * self.duration_h * self.MIN_IN_H)
        return spent_calories_kcal


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIE_INCREASE_MEAN_SPEED: float = 1.1
    CALORIE_MULTIPLIER_WEIGHT: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_kmh: float = (
            self.lenght_pool_m * self.count_pool
            / self.M_IN_KM / self.duration_h)
        return speed_kmh

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories_kcal: float = (
            (
                self.get_mean_speed() + self.CALORIE_INCREASE_MEAN_SPEED
            )
            * self.CALORIE_MULTIPLIER_WEIGHT
            * self.weight_kg
        )
        return spent_calories_kcal


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    from typing import Dict
    sports: Dict[str, type[Training]] = {'RUN': Running, 'WLK': SportsWalking,
                                         'SWM': Swimming}
    if sports.get(workout_type) is None:
        raise KeyError('Неизвестный тип тренировки')
    training: Training = (sports[workout_type])(*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

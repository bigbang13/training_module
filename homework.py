class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получение сообщения о тренировке"""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_MIN = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Создаем объект и сохраняем в нем значения"""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    KOEFF_C_RUN_1 = 18
    KOEFF_C_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.KOEFF_C_RUN_1 * self.get_mean_speed() - self.KOEFF_C_RUN_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.H_IN_MIN)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KOEFF_C_WALK_1 = 0.035
    KOEFF_C_WALK_2 = 0.029
    SQARE = 2

    def __init__(self, action: int,
                 duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((
            self.KOEFF_C_WALK_1
            * self.weight
            + (self.get_mean_speed() ** self.SQARE // self.height)
            * self.KOEFF_C_WALK_2
            * self.weight) * self.duration * self.H_IN_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    KOEFF_C_SW_1 = 1.1
    KOEFF_C_SW_2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (
            self.lenght_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (self.get_mean_speed() + self.KOEFF_C_SW_1) * self.KOEFF_C_SW_2
            * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    from typing import Dict
    sports: Dict[str, type[Training]] = {'RUN': Running, 'WLK': SportsWalking,
                                         'SWM': Swimming}
    training = (sports[workout_type])(*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    print(InfoMessage.get_message(Training.show_training_info(training)))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

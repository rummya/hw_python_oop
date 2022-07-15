from dataclasses import dataclass
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration_h:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')
        return (message.format(training_type=self.training_type,
                duration_h=self.duration_h,
                distance=self.distance,
                speed=self.speed,
                calories=self.calories))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration_h: float
    weight_kg: float

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_TO_HOUR_COEFF: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight_kg / self.M_IN_KM
                * self.duration_h * self.MIN_TO_HOUR_COEFF)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration_h: float,
                 weight_kg: float,
                 height: float) -> None:
        super().__init__(action, duration_h, weight_kg)
        self.height: float = height

    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight_kg
                + (self.get_mean_speed()**2 // self.height)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight_kg)
                * self.duration_h * self.MIN_TO_HOUR_COEFF)


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration_h: float,
                 weight_kg: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration_h, weight_kg)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration_h)

    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * (self.CALORIES_MEAN_SPEED_SHIFT * self.weight_kg))


dict_types: dict[str, Type[Training]] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in dict_types.keys():
        print('Недопустимый тип тренировки. '
              'Пожалуйста выберете один из приведённых ниже:')
        for keys in dict_types.keys():
            print(keys)
        return
    return dict_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    if workout_type not in dict_types.keys():
        return
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WLKk', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

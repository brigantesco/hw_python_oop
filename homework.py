from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Метод возвращает строку сообщения."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_step = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_step * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите метод в '
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           self.duration_h,
                           distance,
                           mean_speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIE_RUN_COEF1: int = 18
    CALORIE_RUN_COEF2: int = 20

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при беге."""
        return ((self.CALORIE_RUN_COEF1 * self.get_mean_speed()
                - self.CALORIE_RUN_COEF2) * self.weight_kg
                / self.M_IN_KM * self.duration_h * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    CALORIE_WLK_COEF1: float = 0.035
    SQUAR: int = 2
    CALORIE_WLK_COEF2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm = height

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при спортивной ходьбе."""
        return ((self.CALORIE_WLK_COEF1 * self.weight_kg
                + (self.get_mean_speed() ** self.SQUAR // self.height_sm)
                * self.CALORIE_WLK_COEF2 * self.weight_kg) * self.duration_h
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 1.38
    CALORIE_SWM_COEF1: float = 1.1
    CALORIE_SWM_COEF2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_step * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Метод возвращает значение средней скорости движения во время
        тренировки по плаванию.
        """
        return (self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.CALORIE_SWM_COEF1)
                * self.CALORIE_SWM_COEF2 * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                 'WLK': SportsWalking,
                                 'RUN': Running}

    if workout_type in dict:
        return dict[workout_type](*data)
    else:
        print('Выберете тип тренировки: SWM, RUN, WLK')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

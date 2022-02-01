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
        return ('Тип тренировки: ' + self.training_type + '; '
                'Длительность: ' + str(format(self.duration, '.3f')) + ' ч.; '
                'Дистанция: ' + str(format(self.distance, '.3f')) + ' км; '
                'Ср. скорость: ' + str(format(self.speed, '.3f')) + ' км/ч; '
                'Потрачено ккал: ' + str(format(self.calories, '.3f')) + '.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # этот метод для трех видов тренировок с тремя разными значениями,
        # не понимаю для какого именно вида тренировки надо вернуть значение
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           self.duration,
                           distance,
                           mean_speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при беге."""
        return ((18 * self.get_mean_speed() - 20) * self.weight
                / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при спортивной ходьбе."""
        return ((0.035 * self.weight + (self.get_mean_speed() ** 2
                // self.height) * 0.029 * self.weight) * self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Метод возвращает значение средней скорости движения во время
        тренировки по плаванию.
        """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Метод возвращает число потраченных калорий при плавании."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)


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

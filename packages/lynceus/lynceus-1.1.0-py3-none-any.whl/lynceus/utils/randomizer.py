import random
import string








def random_int(start: int = 1, stop: int = 424242) -> int:
    return random.randint(start, stop)


def random_id(start: int = 1, stop: int = 424242) -> int:
    return random_int(start=start, stop=stop)


def random_bool() -> bool:
    return random_id() % 2 == 0


def random_string(size: int = 8, *, prefix: str = '', population=string.ascii_letters) -> str:
    return prefix + ''.join(random.choices(population=population, k=size))


def random_email():
    first_name: str = random_string()
    last_name: str = random_string()
    domain: str = f'{random_string(size=5)}.{random_string(size=3)}'
    return f'{first_name}.{last_name}@{domain}'


def random_path(*, part_size: int = 4, part_count: int = 3) -> str:
    path_parts = []
    for _ in range(part_count):
        path_parts.append(random_string(part_size))

    return '/'.join(path_parts)


def random_password(size: int = 16) -> str:
    return random_string(size, population=string.printable)



    # pylint: disable=not-an-iterable







def random_enum(enum_class):
    return random.choice([item.value for item in enum_class])









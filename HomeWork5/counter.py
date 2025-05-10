"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    cls._instance_count = 0

    def get_created_instances(self=None):
        return cls._instance_count

    def reset_instances_counter(self=None):
        count = cls._instance_count
        cls._instance_count = 0
        return count

    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        cls._instance_count += 1
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init

    return cls


if __name__ == '__main__':

    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()
    user.get_created_instances()  # 3
    user.reset_instances_counter()  # 3

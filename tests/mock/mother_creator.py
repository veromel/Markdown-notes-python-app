from faker import Faker


class MotherCreator:
    @staticmethod
    def random():
        return Faker()

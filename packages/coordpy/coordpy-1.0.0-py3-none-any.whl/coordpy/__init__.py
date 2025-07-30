from decimal import Decimal

class Coord:
    """Converts 2 numbers (not complex) into a geographic coordinate."""
    def __init__(self, latitude=0, longitude=0):
        self.south_north = 'N' if latitude >= 0 else 'S'
        self.east_west = 'E' if longitude >= 0 else 'W'

        self.latitude_deg = abs(int(latitude))
        self.longitude_deg = abs(int(longitude))

        latitude_amin_ = abs(Decimal(latitude)) % 1 * 60
        self.latitude_amin = int(latitude_amin_)
        self.latitude_asec = round(Decimal(latitude_amin_) % 1 * 60)
        if self.latitude_asec == 60:
            self.latitude_asec = 0
            self.latitude_amin += 1
        if self.latitude_amin == 60:
            self.latitude_amin = 0
            self.latitude_deg += 1

        longitude_amin_ = abs(Decimal(longitude)) % 1 * 60
        self.longitude_amin = int(longitude_amin_)
        self.longitude_asec = round(Decimal(longitude_amin_) % 1 * 60)
        if self.longitude_asec == 60:
            self.longitude_asec = 0
            self.longitude_amin += 1
        if self.longitude_amin == 60:
            self.longitude_amin = 0
            self.longitude_deg += 1

    def __str__(self): return f'{self.latitude_deg}°{self.latitude_amin}′{self.latitude_asec}″{self.south_north} ' \
                              f'{self.longitude_deg}°{self.longitude_amin}′{self.longitude_asec}″{self.east_west}'
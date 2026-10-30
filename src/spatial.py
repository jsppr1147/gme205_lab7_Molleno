import json


class Parcel:
    def __init__(self, parcel_id, land_use, geometry):
        self.parcel_id = parcel_id
        self.land_use = land_use
        self.geometry = geometry

    @classmethod
    def from_row(cls, row):
        return cls(
            parcel_id=row[0],
            land_use=row[1],
            geometry=json.loads(row[2]),
        )

    def to_feature(self):
        return {
            "type": "Feature",
            "id": self.parcel_id,
            "geometry": self.geometry,
            "properties": {
                "parcel_id": self.parcel_id,
                "land_use": self.land_use,
            },
        }
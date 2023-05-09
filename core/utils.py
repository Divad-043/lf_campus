from geopy.distance import geodesic
from .models import University


def find_nearest_university(user_lat, user_lon):
    universities = University.objects.all()
    closest_university = None
    min_distance = float('inf')
    for university in universities:
        university_lat = university.latitude
        university_lon = university.longitude
        distance = geodesic((user_lat, user_lon), (university_lat, university_lon)).km
        if distance < min_distance:
            min_distance = distance
            closest_university = university
    return closest_university


def get_feature_for_map(items):
    feature_for_map = []
    for _ in items:
        value = _.item.get_popup_information()
        feature_for_map.append(value)
    return feature_for_map

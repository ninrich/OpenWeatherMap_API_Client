import socket
import sys

slovak_translations = {
    "weather": "počasie",
    "temp": "teplota",
    "humidity": "vlhkosť vzduchu",
    "pressure": "tlak",
    "speed": "rýchlosť vetra",
    "deg": "smer vetra",
    "clouds": "oblačno",
    "mist": "hmla"
}

english_translations = {
    "weather": "weather",
    "temp": "temperature",
    "humidity": "air humidity",
    "pressure": "air pressure",
    "speed": "wind speed",
    "deg": "wind direction",
}

units = {
    "temp": "°C",
    "humidity": "%",
    "pressure": "hPa",
    "speed": "km/h",
    "deg": "°",
}


def get_translation(string, slovak=False):
    try:
        return slovak_translations[string.lower()] if slovak else english_translations[string.lower()]
    except KeyError:
        return string


def get_cardinal_direction(degrees, slovak=False):
    directions = ["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"] if slovak else \
        ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    for i in range(1, len(directions)):
        if 45 * i - 22.5 <= degrees <= 45 * i + 22.5:
            return directions[i]
    return directions[0]


def pull_data(dictionary, group_name, attributes, slovak=False):
    # Sometimes the full data isn't provided. TODO: Format output to fixed width.
    for attribute in attributes:
        try:
            print(get_translation(attribute, slovak).capitalize() + ": ", end="")
            if attribute == 'deg':
                print(get_cardinal_direction(dictionary[group_name]["deg"], slovak) + ' - ', end="")
            print(str(dictionary[group_name][attribute]) + units[attribute])
        except KeyError:
            continue


def print_weather_summary(data_dictionary, city, slovak=False):
    print(("Aktuálne počasie v meste %s: " if slovak else "The current weather in %s is ") % (
        city), end="")
    # It is possible to meet more than one weather condition for a requested location.
    # It is also possible to make more readable code.
    print(*[get_translation(data_dictionary["weather"][i]["main"], slovak) for i in
            range(len(data_dictionary["weather"]))])


def main():
    api_key, city, slovak = [None for _ in range(3)]  # TODO: Additional parameter for country.
    try:
        api_key = sys.argv[1]
        city = sys.argv[2]
        slovak = True if sys.argv[3] == "slovak" or sys.argv[3] == "sk" else False
    except IndexError:
        print("Arguments should be in the form <api_key> <city_name> <language>.\n"
              "The following arguments were passed: ", end="")
        print(*sys.argv[1:])
        exit(1)

    # define request as a bytes literal
    request = b"GET /data/2.5/weather?q=" + city.encode() + b"&units=metric&forecast?id=524901&APPID=" \
              + api_key.encode() + b" HTTP/1.1\r\nHost: www.api.openweathermap.org\r\n\r\n"
    # initialize socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    s.connect(("api.openweathermap.org", 80))
    # send the request using the pythonic socket.send
    s.sendall(request)
    # convert the received result to string
    result = s.recv(6969).decode('utf-8')

    # find start of JSON string
    start_of_data_index = result.find('{')
    # extract JSON
    data = result[start_of_data_index:]
    # convert JSON to Python Dictionary
    data_dictionary = eval(data)

    print_weather_summary(data_dictionary, city, slovak)
    pull_data(data_dictionary, "main", ["temp", "humidity", "pressure"], slovak)
    pull_data(data_dictionary, "wind", ["speed", "deg"], slovak)

    s.close()


if __name__ == '__main__':
    main()

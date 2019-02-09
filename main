import socket
import sys

slovak_translations = {
    "weather": "počasie",
    "temp": "teplota",
    "humidity": "vlhkosť vzduchu",
    "pressure": "tlak",
    "speed": "rýchlosť vetra",
    "deg": "smer vetra"
}

english_translations = {
    "weather": "weather",
    "temp": "temperature",
    "humidity": "air humidity",
    "pressure": "air pressure",
    "speed": "wind speed",
    "deg": "wind direction"
}

units = {
    "temp": "°C",
    "humidity": "%",
    "pressure": "hPa",
    "speed": "km/h",
    "deg": "°",  # TODO: Create function to convert it to cardinal direction.
}


def pull_data(dictionary, group_name, attributes, slovak=False):
    # more verbose if condition to prevent its repetition inside the for loop. TODO: Format output to fixed width.
    if slovak:
        for attribute in attributes:
            print(slovak_translations[attribute].capitalize() + ": " + str(dictionary[group_name][attribute]) + units[
                attribute])
    else:
        for attribute in attributes:
            print(english_translations[attribute].capitalize() + ": " + str(dictionary[group_name][attribute]) + units[
                attribute])


def print_weather_summary(data_dictionary, city, slovak=False):
    print(("Aktuálne počasie v meste %s: " if slovak else "The current weather in %s is ") % (
        city), end="")
    # It is possible to meet more than one weather condition for a requested location.
    # It is also possible to make more readable code. TODO: Translate the weather.
    print(*[data_dictionary["weather"][i]["main"] for i in range(len(data_dictionary["weather"]))])


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

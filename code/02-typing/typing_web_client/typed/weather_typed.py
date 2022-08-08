import api_client


def main():
    print("Untyped weather")

    forcast = api_client.get_forecast('Portland', 'OR', 'US')
    print(f"The forcast for Portland is {forcast.desc} and {forcast.temp} F")


if __name__ == '__main__':
    main()

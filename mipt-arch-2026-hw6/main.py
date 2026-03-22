from converters import UsdConverter


def main():
    try:
        amount = float(input('Введите значение в USD: '))
    except ValueError:
        print("Ошибка: введите корректное число")
        return

    converter = UsdConverter()

    if not converter.rates:
        print("Ошибка: не удалось загрузить курсы валют")
        return

    currencies = ['RUB', 'EUR', 'GBP', 'CNY']

    print(f"\n{amount} USD:")
    for currency in currencies:
        result = converter.convert(amount, currency)
        if result:
            print(f"  {currency}: {result:.2f}")


if __name__ == "__main__":
    main()
import csv


def read_csv():
    with open("victorina/database.csv", encoding="utf-8") as file:
        read_data = list(csv.reader(file, delimiter="|"))
        return read_data


def write_to_csv(row):
    with open("victorina/database.csv", mode="a", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|", lineterminator="\n")
        writer.writerow(row)


print(read_csv())
write_to_csv(row=["Где в основном проживают таты?", "Дагестан",
             "Татарстан", "Башкортостан", "Туркменистан"])

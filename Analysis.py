import HelbFour

year = HelbFour.year_prefix
week = HelbFour.week_prefix
day = HelbFour.day_prefix
all = HelbFour.total_prefix
days = HelbFour.days
products = HelbFour.products

def main():
    filename = "HELBFour_2223_project_dataset.txt"
    #filename = "test.txt"

    print("Reading file...")

    frequencies = HelbFour.read_transact(filename)

    print("Done !")
    show_max_min(frequencies)

def show_max_min(frequencies: dict):
    max_freq = max(frequencies[all], key=frequencies[all].get)
    min_freq = min(frequencies[all], key=frequencies[all].get)
    total = sum(frequencies[all].values())

    print("Maximum : " + max_freq + " - " + str(frequencies[max_freq]))
    print("Minimum : " + min_freq + " - " + str(frequencies[min_freq]))
    print("Total : " + str(total))
    print("Values : " + str(frequencies))
    print("-" * 100)

main()
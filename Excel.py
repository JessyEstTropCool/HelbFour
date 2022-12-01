import openpyxl

filename = "Results.xlsx"
wb = openpyxl.load_workbook(filename)
ws = wb.worksheets[0]
index = 1

def write_single_chart_dict(title: str, labels: list, values: dict):
    global index

    ws.cell(index, 1, title)

    for compt in range(len(labels)):
        pos = compt + 2
        ws.cell(index, pos, labels[compt])
        ws.cell(index + 1, pos, values.setdefault(labels[compt], 0))

    index += 2

def write_chart_dict(title: str, series: list, labels: list, keys: list, values: dict):
    global index

    ws.cell(index, 1, title)

    for compt in range(len(labels)):
        pos = compt + 2
        ws.cell(index, pos, labels[compt])

    index += 1

    for compt in range(len(series)):
        ws.cell(index, 1, series[compt])

        for compt2 in range(len(labels)):
            pos = compt2 + 2
            ws.cell(index, pos, values.setdefault(series[compt], {}).setdefault(keys[compt2], 0))

        index += 1

# Save the file
def save_file():
    wb.save(filename)

def close():
    wb.close()
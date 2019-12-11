import sqlite3
import matplotlib.pyplot as plt
import sys


def run_query(table):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,"+ table +" FROM dataRM")

    data = c.fetchall()

    print(data)
    processArr = []
    avgArr = []

    for row in data:
        processArr.append(row[0])
        avgArr.append(row[1])

    plt.xlabel('Process Time')
    plt.ylabel('Energy Consumption Signal')
    plt.title('Energy Database Overview')
    plt.plot(processArr,avgArr)
    plt.show()

if __name__ == "__main__":
    table_name = sys.argv[1] if len(sys.argv) > 1  else "energyAve_kW"
    run_query(table_name)



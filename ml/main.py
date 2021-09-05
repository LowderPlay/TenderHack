import os
import re
import json
import math
import pandas as pd
from tqdm import tqdm
from Ra_feature_package.DataSet.DataSet import *


def get_clean_list(value: str) -> List[str]:
    str_value = str(value).replace("[", "").replace("]", "")
    clean_value = [p.replace("{", "").replace("}", "") for p in str_value.split("},{")]
    return clean_value


def check(text):
   for char in text:
       if char not in "0123456789.":
           return False
   return True


#  Читаем первоначальный, огромный файлик
original_dataset = DataSet(dataset_project_name="original_dataset", show=True)
original_dataset.load_csv_dataset(csv_file="TenderHackDataset/Пример_датасета_для_xакатона_Tender_Hack.csv",
                                  delimiter=";")
# original_dataset.load_csv_dataset(csv_file="TenderHackDataset/DataSet_EKB_200000.csv", delimiter="~") # новый
# original_dataset.load_DataFrame(dataframe=pd.read_excel('TenderHackDataset/DataSet_EKB_200000.xlsx',
#                                                         sheet_name='200000ste'))
# original_dataset.set_delimiter(delimiter="~")
# original_dataset.export(dataset_name="DataSet_EKB_200000",
#                         dataset_folder="TenderHackDataset/",
#                         including_json=False,
#                         including_plots=False)

# print(original_dataset)
# quit()

# # Получение значения с колонки
# ids = DataSet(dataset_project_name="some", show=True)
# ids.create_empty_dataset(columns_names=["Просмотры"],
#                          delimiter=";")
# ids.delete_column(column="Просмотры")
# ids.add_column(column="Просмотры",
#                values=original_dataset.get_column(column="Просмотры"),
#                dif_len=True)
# ids.export(dataset_name="Просмотры",
#            dataset_folder="some",
#            including_plots=False,
#            including_json=False)
# some = [float(i) for i in original_dataset.get_column(column="Просмотры") if not math.isnan(i)]
# some.sort()
# print("ids", min(some), max(some), set(some))
# quit()

# Разрезаем его на файлики поменьше по 1000 записей
# tender_dataset = None
# for i in tqdm(range(len(original_dataset))):
#     if tender_dataset is None:
#         tender_dataset = DataSet(dataset_project_name="TenderDataSet", show=True)
#         tender_dataset.create_empty_dataset(columns_names=original_dataset.get_keys())
#     tender_dataset.add_row(new_row=original_dataset.get_row(index=i))
#     if i % 1000 == 0 and i != 0:
#         tender_dataset.fillna()
#         tender_dataset.set_delimiter(delimiter="~")
#         tender_dataset.export(dataset_name=f"TenderDataSet_X{i}",
#                               dataset_folder="Splitted_X1000_TenderHack",
#                               including_json=False,
#                               including_plots=False)
#         tender_dataset = DataSet(dataset_project_name="TenderDataSet", show=True)
#         tender_dataset.create_empty_dataset(columns_names=original_dataset.get_keys())
# tender_dataset.fillna()
# tender_dataset.set_delimiter(delimiter="~")
# tender_dataset.export(dataset_name=f"TenderDataSet_X200000",
#                       dataset_folder="Splitted_X1000_TenderHack",
#                       including_json=False,
#                       including_plots=False)
# quit()

# Делаем преобразование файлов(чистка и всё такое)
# folders = os.listdir("Splitted_X1000_TenderHack")
# folders = sorted(folders, key=lambda x: int(str(x).split("_")[1].replace("X", "").replace("+", "")))
# for file in tqdm(folders):
#     fly_dataset1 = DataSet(dataset_project_name=f"fly_dataset X {file}", show=True)
#     fly_dataset1.create_empty_dataset(columns_names=original_dataset.get_keys(),
#                                       delimiter="~")
#
#     fly_dataset = DataSet(dataset_project_name=f"fly_dataset X {file}", show=True)
#     fly_dataset.load_csv_dataset(csv_file=os.path.join("Splitted_X1000_TenderHack", file, f"{file}.csv"),
#                                  delimiter="~")
#     fly_dataset.fillna()
#     for fd in range(len(fly_dataset)):
#         this_row = fly_dataset.get_row(index=fd)
#         if this_row["Характеристики СТЕ"] != "-":
#             this_row["Характеристики СТЕ"] = "|".join([str(gcl)
#                                                        .replace('\"Name\":', "")
#                                                        .replace('\"Id\":', "")
#                                                        .replace('\"Value\":', "")
#                                                        .replace('\"Unit\":', "")
#                                                        for gcl in get_clean_list(this_row["Характеристики СТЕ"])])
#         if this_row["Регионы поставки"] != "-":
#             this_row["Регионы поставки"] = "|".join([str(i).replace('\"Name\":', '')
#                                                      for i in get_clean_list(this_row["Регионы поставки"])])
#         if this_row["Поставщики"] != "-":
#             this_row["Поставщики"] = "|".join([str(gcl)
#                                                .replace('\"SupplierId\":', "")
#                                                .replace('\"Name\":', "")
#                                                .replace('\"Inn\":', "")
#                                                for gcl in get_clean_list(this_row["Поставщики"])])
#         if this_row["Другая продукция в контрактах"] != "-":
#             this_row["Другая продукция в контрактах"] = "|".join([str(gcl)
#                                               .replace('\"OtherSkuId\":', "")
#                                               .replace('\"OtherSkuName\":', "")
#                                               .replace('\"Quantity\":', "")
#                                               for gcl in get_clean_list(this_row["Другая продукция в контрактах"])])
#         if this_row["Цена"] != "-":
#             this_row["Цена"] = "|".join([str(i).replace('\"Cost\":', '') for i in get_clean_list(this_row["Цена"])])
#         contracts = float(this_row["Кол-во заключенных контрактов"]) if this_row["Кол-во заключенных контрактов"] not in ["-", ""] else 0
#         views = float(this_row["Просмотры"]) if this_row["Просмотры"] not in ["-", ""] else 0
#         if not contracts > views:
#             fly_dataset1.add_row(new_row=this_row)
#     fly_dataset1.set_delimiter(delimiter="~")
#     fly_dataset1.export(dataset_name=file,
#                         dataset_folder="New_TenderHack",
#                         including_json=False,
#                         including_plots=False)
#     # print(fly_dataset1)
# quit()

# Делаем преобразование файлов(чистка и всё такое)
folders = os.listdir("New_TenderHack")
folders = sorted(folders, key=lambda x: int(str(x).split("_")[1].replace("X", "").replace("+", "")))
contracts = []
# simbols = ["0", "1", " 2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
for file in tqdm(folders):
    fly_dataset = DataSet(dataset_project_name=f"fly_dataset X {file}", show=True)
    fly_dataset.load_csv_dataset(csv_file=os.path.join("New_TenderHack", file, f"{file}.csv"),
                                 delimiter="~")
    # print(fly_dataset)
    fly_dataset.fillna()
    for fd in range(len(fly_dataset)):
        this_row = fly_dataset.get_row(index=fd)
        item_list = str(this_row['Другая продукция в контрактах']).split("|")
        item_list = [[str(i).split(",")[0], str(i).split(",")[-1]] for i in item_list]

        for i in range(len(item_list)):
            try:
                product = int(this_row['Идентификатор СТЕ'])
                related_product = str(item_list[i][0]) if item_list[i][0] not in ["-", ""] else 0
                correlation = str(item_list[i][1]) if item_list[i][1] not in ["-", ""] else "0"
                if related_product != "0" and correlation != "0" and check(correlation) and \
                    check(related_product) and check(str(product)):
                    contracts.append([float(product), float(related_product), float(correlation)])
                    # print(contracts[-1])
            except:
                pass
    fly_dataset.set_delimiter(delimiter="~")
    fly_dataset.export(dataset_name=file,
                       dataset_folder="New_TenderHack",
                       including_json=False,
                       including_plots=False)
dataset = pd.DataFrame(contracts, columns=["product", "related_product", "correlation"])
dataset.to_csv("dataset.csv", index=False, sep=";", encoding="utf-8")
print(len(contracts))

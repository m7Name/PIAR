import glob
import  os



path=""
folders = [f for f in glob.glob(path + "**/migrations/*.py", recursive=True)
            if not os.path.basename(f).startswith('__init__')]

print("Удалил: ")
for f in folders:
    os.remove(f)
    print(f)


try:
    os.remove(""+"db.sqlite3")
    print("Файл базы был удалён")
except:
    print("Файл базы не найден")
print("RESET DONE")

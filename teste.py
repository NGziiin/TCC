import time
contagem = 1
while contagem < 50:
    time.sleep(1)
    contagem += 1
    print(contagem)
    if contagem == 50:
        contagem = 1

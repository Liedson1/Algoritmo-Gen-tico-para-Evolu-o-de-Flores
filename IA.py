import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np

# Definição das características possíveis
cores = ["red", "blue", "yellow", "purple"]
numeros_petalas = [3, 5, 7]
tamanhos_petalas = [0.1, 0.15, 0.2]
formas_folhas = ["oval", "lanceolada", "cordiforme"]

# Função para criar uma flor aleatória
def criar_flor():
    return {
        "cor": random.choice(cores),
        "numero_petalas": random.choice(numeros_petalas),
        "tamanho_petalas": random.choice(tamanhos_petalas),
        "forma_folhas": random.choice(formas_folhas)
    }

# Função para calcular a aptidão de uma flor
def calcular_aptidao(flor):
    aptidao = 0
    if flor["cor"] == "red":
        aptidao += 2
    if flor["numero_petalas"] == 7:
        aptidao += 2
    if flor["tamanho_petalas"] == 0.2:
        aptidao += 1
    if flor["forma_folhas"] == "oval":
        aptidao += 1
    return aptidao

# Função para realizar o cruzamento entre duas flores
def cruzar_flores(flor1, flor2):
    nova_flor = {
        "cor": random.choice([flor1["cor"], flor2["cor"]]),
        "numero_petalas": random.choice([flor1["numero_petalas"], flor2["numero_petalas"]]),
        "tamanho_petalas": random.choice([flor1["tamanho_petalas"], flor2["tamanho_petalas"]]),
        "forma_folhas": random.choice([flor1["forma_folhas"], flor2["forma_folhas"]])
    }
    return nova_flor

# Função para realizar mutação em uma flor e registrar as mutações
def mutar_flor(flor):
    mutacoes = []
    if random.random() < 0.1:  # 10% de chance de mutação em cada característica
        flor["cor"] = random.choice(cores)
        mutacoes.append(f"Cor: {flor['cor']}")
    if random.random() < 0.1:
        flor["numero_petalas"] = random.choice(numeros_petalas)
        mutacoes.append(f"Nº Pétalas: {flor['numero_petalas']}")
    if random.random() < 0.1:
        flor["tamanho_petalas"] = random.choice(tamanhos_petalas)
        mutacoes.append(f"Tamanho: {flor['tamanho_petalas']}")
    if random.random() < 0.1:
        flor["forma_folhas"] = random.choice(formas_folhas)
        mutacoes.append(f"Forma: {flor['forma_folhas']}")
    
    return mutacoes

# Função para desenhar uma flor com múltiplas pétalas
def desenhar_flor(ax, flor, pos_x, pos_y, mutacoes=None):
    angulo_inicial = 0
    for i in range(flor["numero_petalas"]):
        angulo = angulo_inicial + i * (360 / flor["numero_petalas"])
        petala = patches.Ellipse((pos_x, pos_y), width=flor["tamanho_petalas"] * 1.5,
                                 height=flor["tamanho_petalas"] * 0.8,
                                 angle=angulo, color=flor["cor"], alpha=0.7)
        ax.add_patch(petala)
    
    # Adicionar anotações para mutações
    if mutacoes:
        y_texto = pos_y - 0.3
        ax.text(pos_x, y_texto, "Mutado", fontsize=8, ha='center', color='red')
        y_texto -= 0.1
        
        for mutacao in mutacoes:
            ax.text(pos_x, y_texto, mutacao, fontsize=8, ha='center', color='blue')
            y_texto -= 0.1

    ax.text(pos_x, pos_y - 0.2, f'{flor["forma_folhas"]}', fontsize=8, ha='center', color='black')

# Função para gerar os quadros da animação
def gerar_quadros(populacao_inicial, geracoes):
    populacao = populacao_inicial
    quadros = []
    
    for geracao in range(geracoes):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(0, len(populacao) + 1)
        ax.set_ylim(0, 2)
        ax.axis('off')
        
        # Desenhar as flores da geração atual
        for i, flor in enumerate(populacao):
            mutacoes = mutar_flor(flor)  # Checa se a flor foi mutada e aplica a mutação
            desenhar_flor(ax, flor, pos_x=i+1, pos_y=1, mutacoes=mutacoes)
        
        plt.title(f"Geração {geracao}")
        
        # Converter a figura para um quadro
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        quadros.append(img)
        plt.close(fig)
        
        # Calcular aptidão e selecionar as melhores flores
        aptidoes = [calcular_aptidao(flor) for flor in populacao]
        melhores_flores = sorted(populacao, key=calcular_aptidao, reverse=True)[:len(populacao)//2]

        # Cruzar as melhores flores para criar nova geração
        nova_populacao = melhores_flores[:]
        while len(nova_populacao) < len(populacao):
            pai1, pai2 = random.sample(melhores_flores, 2)
            filho = cruzar_flores(pai1, pai2)
            mutar_flor(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao

    return quadros

# Inicializar a população inicial
populacao_inicial = [criar_flor() for i in range(6)]

# Gerar os quadros para a animação
quadros = gerar_quadros(populacao_inicial, 4)

# Configurar e salvar o vídeo
import cv2

video_name = 'evolucao_flores.mp4'
frame_size = (quadros[0].shape[1], quadros[0].shape[0])
fps = 1

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_name, fourcc, fps, frame_size)

for quadro in quadros:
    video_writer.write(cv2.cvtColor(quadro, cv2.COLOR_RGB2BGR))

video_writer.release()
cv2.destroyAllWindows()

print("Vídeo criado com sucesso!")

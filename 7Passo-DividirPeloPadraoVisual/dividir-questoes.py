"""
Propósito: Dividir as questões por padrão visual vertical.
Autor: Alexandre Nassar de Peder
Atualização: 03/06/2026
"""

from PIL import Image
import os

def conferir_cor(pixel, cor_alvo, tolerancia=15):
    """
    Verifica se a cor do pixel está dentro da tolerância em relação à cor alvo.
    """
    r, g, b = pixel[:3]
    return (abs(r - cor_alvo[0]) <= tolerancia and 
            abs(g - cor_alvo[1]) <= tolerancia and 
            abs(b - cor_alvo[2]) <= tolerancia)

def encontrar_faixa_padrao(imagem, tolerancia=15):
    """
    Procura no último pixel da direita (largura - 1) pelo padrão vertical:
    - 9 px (7 a 11 px) RGB (35, 31, 32)
    - 4 px (2 a 6 px)  RGB (255, 255, 255)
    - 5 px (3 a 7 px)  RGB (35, 31, 32)
    - 4 px (2 a 6 px)  RGB (255, 255, 255)
    - 9 px (7 a 11 px) RGB (35, 31, 32)
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)
    
    posicoes_corte = []
    
    # Define os blocos do padrão visual com margem de ±2 px
    # (cor, min_px, max_px)
    padrao = [
        (cor_escura, 7, 11),  # Alvo: 9 px
        (cor_branca, 2, 6),   # Alvo: 4 px
        (cor_escura, 3, 7),   # Alvo: 5 px
        (cor_branca, 2, 6),   # Alvo: 4 px
        (cor_escura, 7, 11)   # Alvo: 9 px
    ]
    
    y = 0
    while y < altura - 30:
        # Percorre o último pixel da direita
        x = largura - 1
        
        y_atual = y
        padrao_valido = True
        
        for cor_alvo, min_h, max_h in padrao:
            contagem_px = 0
            
            # Conta quantos pixels consecutivos correspondem à cor atual do bloco
            while y_atual < altura and conferir_cor(pixels[x, y_atual], cor_alvo, tolerancia):
                contagem_px += 1
                y_atual += 1
                if contagem_px > max_h:
                    break
            
            # Verifica se o número de pixels encontrados está dentro da margem de erro
            if not (min_h <= contagem_px <= max_h):
                padrao_valido = False
                break
        
        if padrao_valido:
            # Posição de início do padrão visual
            inicio_padrao = y
            # Corta 10 px antes do padrão (os 10 px ficam no início do novo bloco)
            posicao_corte = max(0, inicio_padrao - 10)
            
            posicoes_corte.append(posicao_corte)
            print(f"Padrão encontrado em y={inicio_padrao}, cortando em y={posicao_corte}")
            
            # Avança o ponteiro y para além do padrão detectado
            y = y_atual
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando com base no padrão encontrado.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_padrao(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem!")
        return
    
    print(f"Encontrados {len(posicoes_corte)} padrões para corte.")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Corta a seção final (após a última marcação)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "./inteiras/.png"  # Substitua pela sua imagem
    pasta_saida = "Colunas"          # Substitua pela pasta de saída
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    print("Divisão concluída!")
import pygame
import random
import sys

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurações de Tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Coleta - Projeto Acadêmico")
FPS = 60
RELOGIO = pygame.time.Clock()

# Cores
BRANCO, PRETO, AMARELO = (255, 255, 255), (0, 0, 0), (255, 215, 0)
AZUL, VERMELHO = (0, 0, 255), (200, 0, 0)

# Estados
MENU, JOGANDO, VITORIA, DERROTA = 0, 1, 2, 3
estado = MENU

# Variáveis Globais
pontos = 0
tempo_inicio = 0
moedas = []


def criar_moeda():
    """Gera um retângulo de moeda em posição aleatória."""
    return pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 20)


def desenhar_texto(texto, tamanho, cor, x, y):
    """Renderiza texto na tela."""
    fonte = pygame.font.SysFont('Arial', tamanho, bold=True)
    superficie = fonte.render(texto, True, cor)
    TELA.blit(superficie, (x, y))


def resetar_jogo():
    """Reinicia variáveis para uma nova partida."""
    global pontos, tempo_inicio, jogador, fantasma, moedas
    pontos = 0
    tempo_inicio = pygame.time.get_ticks()
    jogador = pygame.Rect(400, 300, 40, 40)
    fantasma = pygame.Rect(100, 100, 40, 40)
    moedas = [criar_moeda() for _ in range(10)]


resetar_jogo()

# Loop Principal
while True:
    TELA.fill(PRETO)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and estado != JOGANDO:
                resetar_jogo()
                estado = JOGANDO

    if estado == MENU:
        desenhar_texto("JOGO COLETA", 60, BRANCO, 250, 150)
        desenhar_texto("Controles: W, A, S, D para mover", 30, BRANCO, 200, 250)
        desenhar_texto("Pressione ENTER para começar", 30, AMARELO, 220, 400)

    elif estado == JOGANDO:
        # Movimentação Jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and jogador.y > 0: jogador.y -= 5
        if teclas[pygame.K_s] and jogador.y < ALTURA - 40: jogador.y += 5
        if teclas[pygame.K_a] and jogador.x > 0: jogador.x -= 5
        if teclas[pygame.K_d] and jogador.x < LARGURA - 40: jogador.x += 5

        # IA Simples (Perseguição)
        if fantasma.x < jogador.x: fantasma.x += 2
        if fantasma.x > jogador.x: fantasma.x -= 2
        if fantasma.y < jogador.y: fantasma.y += 2
        if fantasma.y > jogador.y: fantasma.y -= 2

        # Colisões
        if jogador.colliderect(fantasma): estado = DERROTA
        for m in moedas[:]:
            if jogador.colliderect(m):
                moedas.remove(m)
                pontos += 10

        if len(moedas) == 0: estado = VITORIA

        # Cronômetro
        tempo_decorrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
        tempo_restante = max(0, 60 - tempo_decorrido)
        if tempo_restante == 0: estado = DERROTA

        # Desenho
        pygame.draw.rect(TELA, AZUL, jogador)  # Substituir por .blit(img_jogador, jogador)
        pygame.draw.rect(TELA, VERMELHO, fantasma)
        for m in moedas: pygame.draw.rect(TELA, AMARELO, m)
        desenhar_texto(f"Pontos: {pontos}  Tempo: {tempo_restante}s", 30, BRANCO, 10, 10)

    elif estado == VITORIA:
        desenhar_texto("PARABÉNS! VOCÊ VENCEU!", 50, BRANCO, 120, 250)
        desenhar_texto("ENTER para jogar novamente", 30, AMARELO, 230, 350)

    elif estado == DERROTA:
        desenhar_texto("FIM DE JOGO!", 50, VERMELHO, 250, 250)
        desenhar_texto("ENTER para tentar novamente", 30, BRANCO, 230, 350)

    pygame.display.flip()
    RELOGIO.tick(FPS)
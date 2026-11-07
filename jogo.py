import pygame
import random

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Python Brick Breaker")
relogio = pygame.time.Clock()

# Cores
PRETO = (0,0,0)
BRANCO = (255,255,255)
AZUL = (0,150,255)
VERMELHO = (255,70,70)
VERDE = (70,255,70)
AMARELO = (255,255,70)
CORES_TIJOLOS = [AZUL, VERMELHO, VERDE, AMARELO]

# Varáveis jogo
score = 0
combo = 0
ultimo_tempo_tijolo = 0

# Raquete
raquete = pygame.Rect(LARGURA//2 - 60, ALTURA - 40, 120,15)
vel_raquete = 8

# Bolas
bolas = [{"x": LARGURA//2, "y": ALTURA‑60, "dx":4, "dy":‑4}]
tamanho_bola = 8

# Tijolos
tijolos = []
for linha in range(5):
    for coluna in range(10):
        cor = CORES_TIJOLOS[random.randint(0,3)]
        tijolos.append({"rect":pygame.Rect(coluna*75 +25, linha*30 +40,70,25), "cor":cor})

# Power‑up
powerup = None
vel_powerup = 3

fonte = pygame.font.SysFont(None,36)

def spawn_bola_extra(x,y):
    return {"x":x, "y":y, "dx":random.choice([‑4,4]), "dy":‑4}

# Loop principal
rodando = True
while rodando:
    tela.fill(PRETO)
    tempo_atual = pygame.time.get_ticks()

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento raquete
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and raquete.left >0:
        raquete.x -= vel_raquete
    if teclas[pygame.K_RIGHT] and raquete.right < LARGURA:
        raquete.x += vel_raquete

    # Atualiza bolas
    for b in bolas:
        b["x"] += b["dx"]
        b["y"] += b["dy"]
        # Parede esq/dir
        if b["x"]‑tamanho_bola <0 or b["x"]+tamanho_bola>LARGURA:
            b["dx"] *=‑1
        # Teto
        if b["y"]‑tamanho_bola <0:
            b["dy"] *=‑1
        # Colisão raquete
        bola_rect = pygame.Rect(b["x"]‑tamanho_bola, b["y"]‑tamanho_bola, tamanho_bola*2, tamanho_bola*2)
        if bola_rect.colliderect(raquete):
            b["dy"] *=‑1
        # Bola cai fora
        if b["y"] > ALTURA:
            bolas.remove(b)

    # Colisão tijolos
    for tijolo in tijolos[:]:
        tr = tijolo["rect"]
        for b in bolas:
            br = pygame.Rect(b["x"]‑tamanho_bola, b["y"]‑tamanho_bola, tamanho_bola*2, tamanho_bola*2)
            if br.colliderect(tr):
                tijolos.remove(tijolo)
                b["dy"] *=‑1
                score +=100
                if tempo_atual - ultimo_tempo_tijolo < 400:
                    combo +=1
                else:
                    combo =1
                ultimo_tempo_tijolo = tempo_atual
                # Chance de cair powerup (multi‑bola)
                if random.random() <0.15 and powerup is None:
                    powerup = pygame.Rect(tr.center.x‑10, tr.y,20,20)
                break

    # Power‑up
    if powerup is not None:
        powerup.y += vel_powerup
        pygame.draw.rect(tela, (255,0,255), powerup)
        if powerup.colliderect(raquete):
            bolas.append(spawn_bola_extra(powerup.center.x, powerup.y))
            powerup = None
        elif powerup.y>ALTURA:
            powerup = None

    # Desenhar
    pygame.draw.rect(tela, BRANCO, raquete)
    for b in bolas:
        pygame.draw.circle(tela, (255,0,200), (int(b["x"]), int(b["y"])), tamanho_bola)
    for t in tijolos:
        pygame.draw.rect(tela, t["cor"], t["rect"])

    # Texto
    txt_score = fonte.render(f"SCORE: {score}", True, BRANCO)
    txt_combo = fonte.render(f"COMBO: {combo}", True, (255,255,0))
    tela.blit(txt_score, (10,10))
    tela.blit(txt_combo, (LARGURA‑140,10))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()

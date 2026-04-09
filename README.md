# Knightfall

Projeto de RPG em Python focado na construção de sistemas e arquitetura de código, com ênfase em lógica, organização e escalabilidade — não em interface gráfica.

## Sobre o projeto

O Knightfall foi desenvolvido como um laboratório prático para simular sistemas comuns em jogos e aplicações reais, como gerenciamento de estado, regras de negócio e modularização.

O objetivo principal não é apenas criar um jogo, mas estruturar componentes reutilizáveis e evolutivos.

---

## Funcionalidades atuais

-  Sistema de combate por turnos
-  Inventário com empilhamento inteligente de itens
-  Sistema de drop baseado em classe (Knight, Archer, Thief, Mage)
-  Progressão de personagem (level, atributos e recursos)
-  Persistência de dados utilizando JSON
-  Estrutura de habilidades com possibilidade de expansão

---

##  Arquitetura

O projeto foi organizado buscando separação de responsabilidades:

- `player/` → lógica do jogador e atributos
- `monsters/` → definição e comportamento de inimigos
- `itens/` → estrutura de itens e regras de uso
- `battle.py` → sistema de combate
- `rules.py` → regras de progressão e lógica auxiliar
- `main.py` → fluxo principal do jogo

A estrutura foi pensada para permitir crescimento sem necessidade de refatorações complexas.

---

##  Destaques técnicos

### Inventário inteligente
Implementação de lógica para diferenciar itens empilháveis e únicos, evitando duplicação desnecessária e mantendo consistência dos dados.

### Sistema de combate desacoplado
O combate é tratado como um módulo separado, permitindo evolução independente da lógica do jogador ou dos inimigos.

### Persistência simples e funcional
Uso de JSON para salvar o estado do jogador, facilitando testes e continuidade do jogo.

---

##  Como executar

```bash
git clone https://github.com/EtielOguh/Knightfall.git
cd Knightfall
python main.py

# 🕹️ Jogo em PgZero

Este é um projeto de jogo desenvolvido utilizando **PgZero**, com base nas restrições e requisitos definidos para a disciplina. O jogo segue os gêneros **Platformer**, **Rogue** ou **Roguelike**, utilizando apenas bibliotecas específicas e animações personalizadas.

---


![image](https://github.com/user-attachments/assets/7c920b4c-72c7-407e-a7bf-c8c784620a56)


![image](https://github.com/user-attachments/assets/76b4363d-e43e-4a14-929a-75def983c2c1)

## ✅ Requisitos do Projeto

### Bibliotecas Permitidas

Somente os seguintes módulos e bibliotecas podem ser usados no projeto:

- `pgzrun` (PgZero)  
- `math`  
- `random`  

> ❗ **Outras bibliotecas NÃO podem ser usadas!**  
> ❗ A biblioteca **Pygame NÃO DEVE ser usada!**  
> ✅ **Exceção:** é permitido importar a classe `Rect` da biblioteca `pygame`.

---

### Gêneros Permitidos

O jogo deve pertencer a um dos seguintes gêneros:

- **Roguelike**  
- **Rogue**  
- **Platformer**

---

## 🧩 Funcionalidades Obrigatórias

- Menu principal com botões clicáveis:
  - **Começar o jogo**
  - **Música e sons ligados/desligados**
  - **Sair do jogo**

- Música de fundo e efeitos sonoros  
- Inimigos que representam perigo ao herói  
- Inimigos se movem em seu território  
- Animação de sprites para o herói e inimigos:
  - Tanto em movimento quanto parados (ex: nadadeiras, cauda, respiração, olhar)

- Uso de **classes próprias** para:
  - Movimento dos personagens  
  - Animações

- O código deve estar:
  - Nomeado com **identificadores claros em inglês**
  - Em conformidade com o padrão **PEP8**
  - **Livre de bugs**
  - **Completamente único e autoral**

---

## ▶️ Como Executar

1. Instale e execute o  **PgZero** (se ainda não tiver) Python versão 3.7.7:

```bash
pip install pgzero
pgzrun main.py


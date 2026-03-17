# 💰 Sistema de Triagem Financeira | José Felipe

Bem-vindo ao repositório do meu Sistema de Triagem Financeira! Este projeto foi desenvolvido inteiramente em **Python** utilizando o framework **Streamlit** para criar uma aplicação web interativa que analisa o perfil de investidores e recomenda estratégias financeiras automatizadas.

## 🎯 Sobre o Projeto

Criei este sistema para aplicar conceitos sólidos de lógica de programação, manipulação de arquivos e controle de sessão em um cenário real. O objetivo da aplicação é cruzar dados financeiros do usuário (renda, despesas, capital e idade) para calcular a meta de reserva de emergência e classificar o investidor com base no seu perfil de risco, utilizando as estruturas modernas do Python (como o `match-case`).

## 🚀 Funcionalidades Principais

O sistema é dividido em áreas de acesso com controle de permissões:
* **Autenticação e Cadastro:** Sistema de login para usuários com armazenamento de credenciais em um "banco de dados" local (arquivo `.json`).
* **Painel Administrativo:** Uma aba exclusiva liberada apenas para o usuário `admin`, permitindo a visualização e exclusão de contas cadastradas.
* **Triagem Interativa:** Formulário dinâmico que gera uma análise detalhada na tela e cria um recibo em `.txt` com a data e hora exatas para download.

## 🛠️ Tecnologias Utilizadas

* Python 3.10+
* Streamlit
* Bibliotecas nativas: `json`, `datetime` e `os`

## 💻 Como executar localmente

Clone este repositório:
```bash
git clone [https://github.com/Jose-Felipe-N/sistema-triagem-financeira.git](https://github.com/Jose-Felipe-N/sistema-triagem-financeira.git)
pip install streamlit
streamlit run app.py

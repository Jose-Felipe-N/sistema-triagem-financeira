import streamlit as st
from datetime import datetime
import json
import os

# 1. A configuração da página DEVE ser o primeiro comando Streamlit do arquivo
st.set_page_config(page_title="Triagem Financeira", page_icon="💰")

arquivos_usuarios = "usuarios.json"

def carregar_usuarios():
    caminho_arquivo = 'usuarios.json'
    
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'w') as f:
            json.dump({}, f)
        return {}

    try:
        with open(caminho_arquivo, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}
    
def salvar_usuario(nome, senha):
    """Salva um novo usuairo no arquivo JSON"""
    usuarios = carregar_usuarios()
    if nome in usuarios: # Correção: alterado para verificar se já existe
        return False
    usuarios[nome] = senha
    with open(arquivos_usuarios, "w") as f:
        json.dump(usuarios, f, indent=4)
    return True

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

usuarios_cadastrados = carregar_usuarios()

def sistema_triagem_financeira(nome_investidor, idade, renda_mensal, despesas_mensais, capital_disp, perfil_investidor, tempo_de_investimento):
    """Lógica principal do Sistema de Triagem Financeira"""
    meta_reserva = despesas_mensais * 6
    faltante = meta_reserva - capital_disp
    porcentagem_para_conclusao = (capital_disp / meta_reserva) * 100 if meta_reserva > 0 else 0

    resultado = ""
    status = ""
    
    if 0 < capital_disp < meta_reserva * 0.5:
        status = f"Faltam R${faltante:.2f} para atingir a meta de reserva de emergência. ({porcentagem_para_conclusao:.2f}% concluído)"
    elif capital_disp >= meta_reserva * 0.5:
        status = "Meta de reserva de emergência atingida! Parabéns!"
    else:
        status = "Nenhum capital disponível para investimento. Priorize a construção de uma reserva de emergência."

    match (idade, renda_mensal, despesas_mensais, capital_disp, perfil_investidor, tempo_de_investimento):
        case _ if idade < 18:
            resultado = "INVESTIDOR JOVEM (Perfil Conservador) - Recomendação: Fundos de renda fixa e poupança."
        case _ if renda_mensal < despesas_mensais:
            resultado = "DÉFICIT FINANCEIRO - Ação: Cortar gastos antes de investir."
        case _ if capital_disp < 2000:
            resultado = "INVESTIDOR INICIANTE - Ação: Focar em liquidez e aprendizado."
        case _ if 2000 <= capital_disp < 8000:
            if perfil_investidor == "agressivo":
                resultado = "INTERMEDIÁRIO ARRISCADO - Recomendação: Fundos de ações e ETFs."
            else:
                resultado = "INTERMEDIÁRIO EQUILIBRADO - Recomendação: Fundos multimercados e ações de empresas sólidas."
        case _ if capital_disp >= 8000:
            if perfil_investidor == "agressivo" and tempo_de_investimento >= 5:
                resultado = "ESTRATEGISTA DE LONGO PRAZO - Recomendação: Fundos de ações, ETFs e investimentos alternativos."
            else:
                resultado = "PATRIMÔNIO CONSOLIDADO - Recomendação: Fundos multimercados, ações de empresas sólidas e renda fixa."
        case _:
            resultado = "PERFIL GERAL / CONSERVADOR - Recomendação: Focar em segurança e renda fixa."

    return resultado, status

def gerar_texto_recibo(nome_investidor, idade, renda_mensal, despesas_mensais, perfil, recomendacao_final, status):
    """Gera o texto do recibo em formato string para download"""
    agora = datetime.now()
    formato_data = agora.strftime("%Y-%m-%d %H:%M:%S")
    
    recibo = (
        f"{'=' * 40}\n"
        f"Recibo de Triagem Financeira\n"
        f"Data e hora: {formato_data}\n"
        f"{'-' * 40}\n\n"
        f"Status: {status}\n\n"
        f"{'-' * 40}\n\n"
        f"Cliente: {nome_investidor}\n"
        f"Idade: {idade} anos\n"
        f"Renda Mensal: R${renda_mensal:.2f}\n"
        f"Despesas Mensais: R${despesas_mensais:.2f}\n"
        f"Perfil de Investimento: {perfil.capitalize()}\n"
        f"Recomendação: {recomendacao_final}\n"
        f"{'=' * 40}\n"
    )
    return recibo

# ==========================================
# TELAS DO SISTEMA
# ==========================================
def tela_login():
    st.title("🔐 Login")
    aba_login, aba_cadastro = st.tabs(["Login", "Cadastrar"])
    
    with aba_login:
        usuario_login = st.text_input("Usuario:", key="input_usuario_login")
        senha_login = st.text_input("Senha:", type="password", key="input_senha_login")

        if st.button("Entrar"):
            if usuario_login in usuarios_cadastrados and usuarios_cadastrados[usuario_login] == senha_login:
                st.session_state['logado'] = True
                st.session_state['usuario_atual'] = usuario_login
                st.rerun()
            else:
                st.error("Usuario ou senha incorretos!")
                
    with aba_cadastro:
        st.write("Crie uma nova conta")
        novo_usuario = st.text_input("Escolha um nome de usuário:", key="input_novo_usuario")
        nova_senha = st.text_input("Escolha uma senha:", type="password", key="input_nova_senha")
        confirmar_senha = st.text_input("Confirme a senha:", type="password", key="input_confirmar_senha")

        if st.button("Cadastrar"):
            if not novo_usuario or not nova_senha:
                st.warning("Por favor, preencha todos os campos!")
            elif nova_senha != confirmar_senha:
                st.warning("As senhas não coincidem!")
            else:
                sucesso = salvar_usuario(novo_usuario, nova_senha)
                if sucesso:
                    st.success("Conta criada com sucesso! Faça login para continuar.")
                    usuarios_cadastrados.update(carregar_usuarios()) # Atualiza a memória
                else: 
                    st.error("O nome de usuário já existe. Por favor, escolha outro.")

def tela_principal():
    # Cabeçalho com botão de sair
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title(f"Bem-vindo, {st.session_state['usuario_atual']}! 👋")
    with col2:
        st.write("") # Espaço para alinhar o botão
        if st.button("Sair", use_container_width=True):
            st.session_state['logado'] = False
            st.session_state['usuario_atual'] = None
            st.rerun()
            
    st.divider()
    
    # Lógica da Triagem realocada para dentro da função!
    st.title("💰 Sistema de Triagem Financeira para Investidores")
    st.write("Insira suas informações abaixo para receber uma análise do seu perfil financeiro.")

    with st.form("form_investidor"):
        nome_investidor = st.text_input("Nome do investidor:")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            idade = st.number_input("Idade (em anos):", min_value=0, max_value=130, step=1, value=None, placeholder="Ex: 25")
            renda_mensal = st.number_input("Renda mensal (R$):", min_value=0.0, step=100.0, format="%.2f", value=None, placeholder="Ex: 3500.00")
            despesas_mensais = st.number_input("Despesas mensais (R$):", min_value=0.0, step=100.0, format="%.2f", value=None, placeholder="Ex: 2000.00")
        
        with col_form2:
            capital_disp = st.number_input("Capital disponível (R$):", min_value=0.0, step=100.0, format="%.2f", value=None, placeholder="Ex: 5000.00")
            tempo_de_investimento = st.number_input("Tempo de investimento (anos):", min_value=0, max_value=100, step=1, value=None, placeholder="Ex: 5")
            perfil_investidor = st.pills(
                "Perfil de investimento:", 
                options=["Conservador", "Moderado", "Agressivo"],
                default="Conservador" 
            ).lower()
        
        submit = st.form_submit_button("Analisar Perfil")

    # Executa quando o botão é clicado
    if submit:
        # Adicionei a validação do None para evitar erro se o usuário mandar o form vazio
        if not nome_investidor:
            st.warning("Por favor, preencha o nome do investidor.")
        elif None in [idade, renda_mensal, despesas_mensais, capital_disp, tempo_de_investimento]:
            st.warning("Por favor, preencha todos os campos numéricos corretamente.")
        else:
            recomendacao_final, status_final = sistema_triagem_financeira(
                nome_investidor, idade, renda_mensal, despesas_mensais, 
                capital_disp, perfil_investidor, tempo_de_investimento
            )
            
            st.subheader(f"Resultados para {nome_investidor}")
            
            if "Parabéns" in status_final:
                st.success(status_final)
            else:
                st.warning(status_final)
                
            st.info(recomendacao_final)

            texto_recibo = gerar_texto_recibo(
                nome_investidor, idade, renda_mensal, despesas_mensais, 
                perfil_investidor, recomendacao_final, status_final
            )
            
            agora_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"recibo_{nome_investidor.replace(' ', '_')}_{agora_str}.txt"
            
            st.download_button(
                label="📄 Baixar Recibo (TXT)",
                data=texto_recibo,
                file_name=nome_arquivo,
                mime="text/plain"
            )

# ==========================================
# CONTROLE DE ROTAS (O que mostra na tela)
# ==========================================
if not st.session_state['logado']:
    tela_login()
else:
    tela_principal()

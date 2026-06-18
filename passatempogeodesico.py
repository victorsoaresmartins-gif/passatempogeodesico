import streamlit as st
import random
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Passatempo Geodésico - Edição Acadêmica", page_icon="🌎", layout="wide")

# 2. BANCO DE DADOS INTEGRADO (FONTES RASTREÁVEIS E REAIS)
if "banco_perguntas" not in st.session_state:
    st.session_state.banco_perguntas = [
        # TOPOGRAFIA (Casas 1-10) - Dificuldade Fácil (10 XP)
        {"cat": "Topografia", "dif": "Fácil", "xp": 10, "p": "Qual o ângulo horizontal medido a partir do Norte verdadeiro ou magnético, variando de 0° a 360° no sentido horário?", "r": "Azimute", "opcoes": ["Azimute", "Rumo", "Deflexão"], "expl": "O azimute é contado de 0° a 360° a partir do Norte. O rumo varia de 0° a 90° em quadrantes.", "f": "Gemael ( introduction à Geodésia Geométrica)"},
        {"cat": "Topografia", "dif": "Fácil", "xp": 10, "p": "O erro que se repete regularmente sob as mesmas condições de medição e segue uma lei matemática determinística é o:", "r": "Erro Sistemático", "opcoes": ["Erro Aleatório", "Erro Sistemático", "Engano Blunder"], "expl": "Erros sistemáticos podem ser eliminados por calibração ou fórmulas matemáticas.", "f": "Ajustamento por MMQ - Conceitos Básicos"},
        {"cat": "Topografia", "dif": "Fácil", "xp": 10, "p": "Qual o método de nivelamento geométrico que utiliza visadas horizontais com nível óptico e mira graduada?", "r": "Nivelamento Geométrico", "opcoes": ["Nivelamento Trigonométrico", "Nivelamento Geométrico", "Nivelamento Barométrico"], "expl": "O nivelamento geométrico é o método mais preciso para determinação de diferenças de altitudes.", "f": "Manual Técnico de Topografia Geral"},

        # GNSS (Casas 11-20) - Dificuldade Média (20 XP)
        {"cat": "GNSS", "dif": "Média", "xp": 20, "p": "Qual método de posicionamento GNSS exige uma estação de referência (base) enviando correções em tempo real para um receptor móvel (rover)?", "r": "RTK", "opcoes": ["PPP", "RTK", "Estático Pós-Processado"], "expl": "O RTK (Real Time Kinematic) transmite correções instantâneas via rádio UHF ou internet (NTRIP).", "f": "Monico (2008) - Posicionamento pelo GNSS"},
        {"cat": "GNSS", "dif": "Média", "xp": 20, "p": "O efeito da refração que causa o maior atraso ionosférico no sinal GNSS pode ser eliminado principalmente através de:", "r": "Uso de receptores de dupla frequência (L1/L2)", "opcoes": ["Uso de receptores de dupla frequência (L1/L2)", "Aumento do tempo de rastreio", "Calibração da antena"], "expl": "A combinação linear livre da ionosfera elimina o erro de primeira ordem usando duas frequências distintas.", "f": "Seeber - Satellite Geodesy"},
        {"cat": "GNSS", "dif": "Média", "xp": 20, "p": "Qual termo descreve a degradação da precisão das coordenadas devido à má geometria espacial dos satélites rastreados?", "r": "DOP", "opcoes": ["DOP", "PPP", "NTRIP"], "expl": "O Dilution of Precision (DOP) indica quão espalhados os satélites estão no céu; valores baixos são melhores.", "f": "Monico (2008) - Posicionamento pelo GNSS"},

        # GEODÉSIA FÍSICA (Casas 21-30) - Dificuldade Avançada (30 XP)
        {"cat": "Geodésia Física", "dif": "Avançada", "xp": 30, "p": "A superfície equipotencial do campo de gravidade da Terra que coincide com o nível médio dos mares em repouso prolongado é o:", "r": "Geoide", "opcoes": ["Elipsoide", "Geoide", "Superfície Topográfica"], "expl": "O geoide é a superfície de referência física para altitudes ortométricas.", "f": "Torge & Müller - Geodesy"},
        {"cat": "Geodésia Física", "dif": "Avançada", "xp": 30, "p": "A diferença medida sobre a normal entre a altitude elipsoidal (h) obtida pelo GNSS e a altitude ortométrica (H) é a:", "r": "Ondulação Geoidal (N)", "opcoes": ["Ondulação Geoidal (N)", "Anomalia da Gravidade", "Desvio da Vertical"], "expl": "A relação fundamental é dada por h = H + N.", "f": "IBGE - hgeoHNOR2020"},
        {"cat": "Geodésia Física", "dif": "Avançada", "xp": 30, "p": "Qual modelo oficial o IBGE disponibiliza para a conversão de altitudes elipsoidais em ortométricas no território brasileiro?", "r": "hgeoHNOR2020", "opcoes": ["MAPGEO2015", "hgeoHNOR2020", "EGM96"], "expl": "O hgeoHNOR2020 é o modelo de fator de conversão de altitude vigente no Brasil.", "f": "IBGE - Diretoria de Geociências"},

        # CARTOGRAFIA (Casas 31-40) - Dificuldade Profissional (40 XP)
        {"cat": "Cartografia", "dif": "Profissional", "xp": 40, "p": "O ângulo entre o Norte Verdadeiro (Geográfico) e o Norte de Quadrícula (Projeção) em um determinado ponto de um fuso UTM chama-se:", "r": "Convergência Meridiana", "opcoes": ["Declinação Magnética", "Convergência Meridiana", "Fator de Escala"], "expl": "A convergência meridiana é nula sobre o Meridiano Central do fuso e aumenta em direção às bordas.", "f": "IBGE - Noções de Cartografia"},
        {"cat": "Cartografia", "dif": "Profissional", "xp": 40, "p": "No sistema de projeção UTM, qual é o valor numérico exato do fator de escala (k0) aplicado sobre o Meridiano Central de qualquer fuso?", "r": "0,9996", "opcoes": ["1,0000", "0,9996", "1,0004"], "expl": "O fator de escala de 0,9996 reduz as distorções nas áreas intermediárias do fuso UTM.", "f": "Manual Técnico para Georreferenciamento de Imóveis Rurais"},

        # SGB (Casas 41-50) - Dificuldade Especialista (50 XP)
        {"cat": "SGB", "dif": "Especialista", "xp": 50, "p": "O sistema SIRGAS 2000, referencial geodésico oficial do Brasil, possui uma concepção de qual tipo?", "r": "Geocêntrica", "opcoes": ["Topocêntrica", "Geocêntrica", "Planimétrica Pura"], "expl": "O SIRGAS 2000 tem sua origem vinculada ao centro de massa da Terra.", "f": "IBGE - Resolução PR Nº 1/2005"}
    ]

# 3. GLOSSÁRIO ACADÊMICO EXPANDIDO (55 Termos)
GLOSSARIO = {
    "Acurácia": "Grau de conformidade de um valor medido com o seu valor verdadeiro (padrão absoluto).",
    "Ajustamento": "Processo matemático (ex: MMQ) para estimar valores de grandezas e consistência de redundâncias eliminando erros aleatórios.",
    "Anomalia da Gravidade": "Diferença entre a gravidade real observada e a gravidade teórica normal calculada sobre o elipsoide.",
    "Azimute": "Ângulo horizontal medido a partir do meridiano de referência (Norte), variando de 0° a 360° no sentido horário.",
    "BeiDou": "Sistema de Navegação por Satélite global desenvolvido e operado pela República Popular da China.",
    "Cartografia": "Ciência e arte de representar graficamente a superfície terrestre por meio de mapas e cartas.",
    "Córrego Alegre": "Datum topocêntrico antigo utilizado no Brasil, tendo como vértice o ponto Córrego Alegre (MG).",
    "Convergência Meridiana": "Ângulo formado entre o norte geográfico (meridiano) e o norte da projeção (paralela ao meridiano central).",
    "Datum": "Ponto, linha ou superfície de referência a partir do qual as coordenadas tridimensionais são calculadas.",
    "Datum Topocêntrico": "Referencial cujo centro do elipsoide associado está deslocado do centro de massa planetário (ex: SAD-69).",
    "Datum Geocêntrico": "Referencial cujo elipsoide possui o centro coincidente com o centro de massa da Terra (ex: SIRGAS 2000).",
    "DOP (Diluição da Precisão)": "Indicador adimensional baseado na geometria espacial dos satélites GNSS que multiplica os erros de medição.",
    "Efemérides": "Conjunto de dados transmitidos pelos satélites que descrevem suas órbitas e posições exatas no espaço em função do tempo.",
    "Elipsoide de Referência": "Superfície matemática gerada pela rotação de uma elipse que simula a forma geométrica macro da Terra.",
    "Erro Aleatório": "Erro residual inevitável nas medições que obedece a leis de probabilidade e distribuições normais.",
    "Erro Sistemático": "Erro que segue uma lei física ou matemática constante e pode ser modelado ou eliminado por calibração.",
    "Estação Total": "Equipamento eletrônico que combina teodolito digital, distanciômetro eletrônico e microprocessador.",
    "Fator de Escala (k)": "Razão entre a distância linear em uma projeção cartográfica e a distância real sobre o elipsoide.",
    "Fuso UTM": "Cada uma das 60 zonas de projeção cilíndrica transversal da Terra, possuindo amplitude exata de 6° de longitude.",
    "Galileo": "Sistema de posicionamento e navegação global por satélite civil operado pela União Europeia.",
    "Gemael": "Professor e autor de livros fundamentais de Geodésia Geométrica e Ajustamento no Brasil.",
    "Geodésia": "Ciência geométrica e física que estuda a forma, dimensões e o campo gravimétrico da Terra ao longo do tempo.",
    "Geodésia Física": "Ramo que estuda a Terra por meio de medições gravimétricas para modelagem precisa do Geoide.",
    "Geoide": "Superfície equipotencial do campo gravítico terrestre que coincide com o nível médio dos mares não perturbados.",
    "GLONASS": "Sistema de Navegação Global por Satélite desenvolvido e administrado pela Federação Russa.",
    "GPS": "Global Positioning System. Sistema de navegação global por satélite desenvolvido pelo Departamento de Defesa dos EUA.",
    "Gravimetria": "Medição e determinação da magnitude do vetor gravidade nas adjacências da superfície planetária.",
    "GRS80": "Geodetic Reference System 1980. Elipsoide geocêntrico adotado oficialmente como base geométrica do SIRGAS 2000.",
    "hgeoHNOR2020": "Modelo oficial de conversão de altitudes do IBGE baseado em nivelamento geométrico associado a gravimetria.",
    "IBGE": "Instituto Brasileiro de Geografia e Estatística, órgão gestor do Sistema Geodésico Brasileiro.",
    "Irradiação": "Método topográfico de determinação de coordenadas de pontos a partir de uma estação conhecida por ângulo e distância.",
    "Máscara de Elevação": "Ângulo de corte configurado no receptor GNSS (ex: 10° ou 15°) para ignorar satélites baixos poluídos por refração.",
    "Meridiano Central": "Meridiano localizado no centro exato de um fuso UTM, adotado como origem do eixo das abcissas.",
    "MMQ (Mínimos Quadrados)": "Método matemático de ajustamento que minimiza a soma dos quadrados dos resíduos das medições.",
    "Monico": "Pesquisador brasileiro referência nacional na literatura de posicionamento e navegação por satélite GNSS.",
    "Nivelamento Geométrico": "Método de determinação de diferenças de nível usando nível de precisão óptico e miras verticais graduadas.",
    "Nivelamento Trigonométrico": "Determinação de desníveis por meio da leitura de ângulos zenitais e distâncias inclinadas obtidas com estação total.",
    "Norte Verdadeiro": "Direção que aponta para o polo geográfico de rotação da Terra.",
    "Norte de Quadrícula": "Direção das linhas verticais paralelas ao meridiano central de um sistema de projeção plana como o UTM.",
    "NTRIP": "Protocolo para transmissão de correções diferenciais GNSS (RTK) via fluxos de dados de internet móvel.",
    "Ondulação Geoidal": "Distância vertical, contada ao longo da normal, entre a superfície do elipsoide de referência e o geoide.",
    "Pós-processamento": "Cálculo vetorial preciso de coordenadas executado em escritório após o término da sessão de coleta de dados de campo.",
    "Poligonal Topográfica": "Método de estabelecimento de pontos de apoio de campo ligando uma série de linhas consecutivas medidas.",
    "Potencial Gravítico": "Função escalar que descreve a energia potencial por unidade de massa no campo de gravidade da Terra.",
    "PPP (Posicionamento por Ponto Preciso)": "Método GNSS absoluto que faz uso de efemérides precisas e correções de relógio geradas globalmente.",
    "Precisão": "Grau de dispersão ou repetibilidade mútua entre uma série de medições independentes de uma mesma grandeza.",
    "RBMC": "Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS. Infraestrutura oficial de estações ativas do IBGE.",
    "RTK": "Real Time Kinematic. Posicionamento cinemático em tempo real baseado em correções de fase de onda portadora.",
    "Rumo": "Menor ângulo horizontal formado pelo meridiano de referência e a linha de visada, variando de 0° a 90° por quadrante (NE, SE, SW, NW).",
    "SAD-69": "South American Datum 1969. Antigo sistema de referência topocêntrico unificado para a América do Sul.",
    "SGB": "Sistema Geodésico Brasileiro. Conjunto de pontos, redes e padrões homologados e gerenciados pelo IBGE.",
    "SIRGAS 2000": "Sistema de Referência Geocêntrico para as Américas. Referencial legal e obrigatório do Brasil desde 2015.",
    "UTM": "Universal Transversa de Mercator. Sistema de projeção conforme, cilíndrico e transverso dividido em fusos.",
    "Variância": "Medida estatística de dispersão matemática de dados que representa o quadrado do desvio-padrão.",
    "WGS84": "World Geodetic System 1984. Sistema geodésico global de referência utilizado nativamente pelo GPS americano."
}

# 4. INICIALIZAÇÃO DE VARIÁVEIS DE ESTADO DO JOGO
if "posicao" not in st.session_state: st.session_state.posicao = 0
if "xp" not in st.session_state: st.session_state.xp = 0
if "acertos" not in st.session_state: st.session_state.acertos = 0
if "erros" not in st.session_state: st.session_state.erros = 0
if "status_jogo" not in st.session_state: st.session_state.status_jogo = "jogar"
if "historico" not in st.session_state: st.session_state.historico = "🛰️ Sistema Geodésico Calibrado. Inicie seu levantamento de campo!"
if "conquistas" not in st.session_state: st.session_state.conquistas = []
if "pergunta_atual" not in st.session_state: st.session_state.pergunta_atual = None

TAMANHO_TABULEIRO = 50

# DETERMINAÇÃO DINÂMICA DE SETORES E TÍTULOS DE NÍVEIS
def obter_nivel(xp):
    if xp < 100: return "🎓 Estagiário de Agrimensura"
    if xp < 250: return "📐 Auxiliar de Campo Técnico"
    if xp < 500: return "📡 Analista GNSS Sênior"
    if xp < 850: return "🌍 Engenheiro Cartógrafo Adjunto"
    return "🏆 Especialista em Geodésia de Alta Precisão"

def obter_setor_atual(pos):
    if pos < 10: return "📐 SETOR 1: Topografia de Base", "🟩", "Casas 0 a 9. Foco em medições clássicas, azimutes, rumos e erros sistemáticos."
    elif pos < 20: return "📡 SETOR 2: Posicionamento GNSS", "🟦", "Casas 10 a 19. Rastreamento por satélite, métodos RTK/PPP e efeitos atmosféricos."
    elif pos < 30: return "🌍 SETOR 3: Geodésia Física", "🟪", "Casas 20 a 29. Altitudes ortométricas, gravimetria e modelagem matemática do Geoide."
    elif pos < 40: return "🗺️ SETOR 4: Cartografia e Projeções", "🟧", "Casas 30 a 39. Deformações lineares, fusos UTM e convergências meridianas."
    else: return "🏛️ SETOR 5: Sistema Geodésico Brasileiro", "🔴", "Casas 40 a 49. Legislações do IBGE, SIRGAS 2000 e marcos geodésicos estruturais."

# GERENCIADOR DE AVANÇO
def mover_jogador(passos):
    st.session_state.posicao += passos
    st.toast(f"🚶 Movendo {passos} marcos na rede...", icon="🏃‍♂️")

    # Valida fim de jogo
    if st.session_state.posicao >= TAMANHO_TABULEIRO - 1:
        st.session_state.posicao = TAMANHO_TABULEIRO - 1
        st.session_state.status_jogo = "fim"
        return

    # Determinação lógica exata das casas de eventos especiais fixos
    pos = st.session_state.posicao
    if pos in [5, 14, 25, 34, 44]:
        st.session_state.status_jogo = "biblioteca"
    elif pos == 8:
        st.session_state.status_jogo = "minigame_timeline"
    elif pos == 12:
        st.session_state.status_jogo = "minigame_radar"
    elif pos == 18:
        st.session_state.status_jogo = "minigame_associacao"
    elif pos in [22, 42]:
        st.session_state.status_jogo = "minigame_auditoria"
    elif pos == 32:
        st.session_state.status_jogo = "minigame_pistas"
    elif pos == 38:
        st.session_state.status_jogo = "minigame_criptograma"
    else:
        # Puxa pergunta do banco correspondente ao tema
        filtradas = [q for q in st.session_state.banco_perguntas if q["cat"] == tema_filtro]
        if filtradas:
            st.session_state.pergunta_atual = random.choice(filtradas)
            st.session_state.status_jogo = "pergunta"
        else:
            st.session_state.status_jogo = "jogar"

# DIÁLOGO INTEGRADO PARA FEEDBACK ACADÊMICO
@st.dialog("📋 Avaliação Técnica do Relatório")
def exibir_modal_feedback(sucesso, explicacao, fonte, xp_ganho):
    if sucesso:
        st.success(f"🎯 AJUSTE HOMOLOGADO COM SUCESSO! (+{xp_ganho} XP)")
    else:
        st.error("💥 REPROVADO FORA DA TOLERÂNCIA GEODÉSICA! (-1 Casa)")
    st.markdown(f"**Justificativa Científica:** {explicacao}")
    st.info(f"📚 Referência Rastreável: {fonte}")
    if st.button("Atualizar Banco de Dados e Fechar"):
        st.rerun()

# --- INTERFACE PRINCIPAL ---
aba_jogo, aba_glossario = st.tabs(["🎮 Painel de Controle de Campanha", "📖 Enciclopédia de Apoio Técnico"])

with aba_glossario:
    st.header("📖 Glossário de Engenharia Cartográfica e Agrimensura")
    st.caption("Apoio didático para revisões rápidas com definições completas baseadas em normas nacionais.")
    termo_selecionado = st.selectbox("Selecione um conceito geodésico para consulta:", sorted(list(GLOSSARIO.keys())))
    st.info(f"**{termo_selecionado}:** {GLOSSARIO[termo_selecionado]}")

with aba_jogo:
    # 1. SIDEBAR DE STATUS E CONQUISTAS
    with st.sidebar:
        st.header("📊 Dados do Operador")
        st.metric(label="Título Profissional", value=obter_nivel(st.session_state.xp))
        st.metric(label="Pontuação de Experiência (XP)", value=f"{st.session_state.xp} XP")

        # Monitoramento de Desempenho Estatístico
        total_resp = st.session_state.acertos + st.session_state.erros
        taxa = int((st.session_state.acertos / total_resp) * 100) if total_resp > 0 else 0

        st.markdown("---")
        st.markdown(f"**🎯 Acertos Homologados:** {st.session_state.acertos}")
        st.markdown(f"**❌ Erros de Fechamento:** {st.session_state.erros}")
        st.markdown(f"**📈 Taxa de Precisão:** {taxa}%")

        # Painel de Conquistas Reais
        st.markdown("---")
        st.subheader("🏅 Medalhas de Campo")
        if st.session_state.acertos >= 3 and "GNSS" not in st.session_state.conquistas:
            st.session_state.conquistas.append("GNSS")
            st.toast("Medalha Atribuída: Guardião da RBMC!", icon="🏅")
        if st.session_state.xp >= 400 and "Geo" not in st.session_state.conquistas:
            st.session_state.conquistas.append("Geo")
            st.toast("Medalha Atribuída: Fiscal Avançado do IBGE!", icon="🏅")

        if not st.session_state.conquistas:
            st.caption("Execute medições corretas para desbloquear medalhas.")
        for medalha in st.session_state.conquistas:
            if medalha == "GNSS": st.success("🏅 Guardião da RBMC (3+ Acertos)")
            if medalha == "Geo": st.warning("🏅 Fiscal Técnico do IBGE (400+ XP)")

    # 2. SEÇÃO SUPERIOR: PROGRESSÃO E TABULEIRO VISUAL
    setor_nome, setor_cor, setor_desc = obter_setor_atual(st.session_state.posicao)
    st.markdown(f"### {setor_nome}")
    st.caption(setor_desc)

    # Barra de Progresso Real
    porcentagem_concluida = int((st.session_state.posicao / (TAMANHO_TABULEIRO - 1)) * 100)
    st.progress(porcentagem_concluida / 100, text=f"Vértices Consolidados: {st.session_state.posicao} de 49 ({porcentagem_concluida}%)")

    # Renderização da Malha do Tabuleiro em Sublinhas Coerentes
    linha1, linha2 = "", ""
    for idx in range(TAMANHO_TABULEIRO):
        if idx == st.session_state.posicao: char = "🏃‍♂️ "
        elif idx in [5, 14, 25, 34, 44]: char = "📚 "
        elif idx in [8, 12, 18, 22, 32, 38, 42]: char = "🧩 "
        elif idx == TAMANHO_TABULEIRO - 1: char = "🏁 "
        else:
            if idx < 10: char = "🟩 "
            elif idx < 20: char = "🟦 "
            elif idx < 30: char = "🟪 "
            elif idx < 40: char = "🟧 "
            else: char = "🔴 "
        if idx < 25: linha1 += char
        else: linha2 += char

    st.markdown(f"**Rede Setorial Norte (01 a 25):** {linha1}")
    st.markdown(f"**Rede Setorial Sul (26 a 50):** {linha2}")
    st.caption("🏃‍♂️ Sua Posição | 🟩 Topografia | 🟦 GNSS | 🟪 Físicа | 🟧 Cartografia | 🔴 SGB | 📚 Biblioteca | 🧩 Desafio Técnico")
    st.markdown("---")
    st.info(st.session_state.historico)

    # 3. INTERAÇÕES E MECÂNICAS DOS MINIGAMES
    if st.session_state.status_jogo == "jogar":
        st.subheader("🎲 Avanço de Malha de Transporte")
        if st.button("Disparar Pulso do Dado Finito (1 a 3)"):
            passos = random.randint(1, 3)
            st.session_state.historico = f"Última ação: Dado de precisão gerou avanço de **{passos}** unidades."
            mover_jogador(passos)
            st.rerun()

    elif st.session_state.status_jogo == "biblioteca":
        st.subheader("📚 Casa de Estudo Especial: Biblioteca Geodésica")
        # Fornece conhecimento em vez de teste pura e simplesmente
        if st.session_state.posicao == 5:
            st.markdown("### Definição Prática de Azimutes e Rumos")
            st.write("Um dos maiores erros em levantamentos de topografia clássica decorre da confusão de quadrantes. Lembre-se: O Rumo varia apenas de 0-90° e obrigatoriamente carrega a sigla do quadrante de amarração (ex: 45° SE).")
        elif st.session_state.posicao == 14:
            st.markdown("### Funcionamento Estrutural da RBMC")
            st.write("A Rede Brasileira de Monitoramento Contínuo elimina a necessidade de instalar receptores de referência próprios em campo para levantamentos pós-processados, contanto que o operador baixe os arquivos RINEX oficiais no portal do IBGE dentro do mesmo intervalo de rastreamento.")
        else:
            st.markdown("### O Elipsoide Geocêntrico")
            st.write("Ao contrário de sistemas obsoletos como o SAD-69, sistemas geocêntricos modernos alinham seu centro tridimensional com o baricentro terrestre, minimizando discrepâncias globais nos cálculos de navegação orbital de frotas de satélites.")

        st.caption("Fonte: IBGE - Diretoria de Geociências (Coleta de Dados de Alta Precisão)")
        if st.button("Concluir Leitura e Coletar Bônus (+20 XP)"):
            st.session_state.xp += 20
            st.session_state.status_jogo = "jogar"
            st.session_state.historico = "Leitura técnica registrada em seu diário de campo."
            st.rerun()

    elif st.session_state.status_jogo == "pergunta":
        q = st.session_state.pergunta_atual
        st.subheader(f"❓ Avaliação Teórica - Categoria: {q['cat']} ({q['dif']})")
        st.markdown(f"### **{q['p']}**")
        resp = st.radio("Escolha o parecer técnico correto baseado nas normas de engenharia:", q['opcoes'], key="radio_pergunta_central")

        if st.button("Homologar Resposta Técnica"):
            if resp == q['r']:
                st.session_state.acertos += 1
                st.session_state.xp += q['xp']
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "✅ Último relatório homologado com sucesso no sistema!"
                exibir_modal_feedback(True, q['expl'], q['f'], q['xp'])
            else:
                st.session_state.erros += 1
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "❌ Relatório contendo inconsistências conceituais. Retrocesso de 1 marco imposto."
                exibir_modal_feedback(False, q['expl'], q['f'], 0)

    # --- MINIGAMES EXCLUSIVOS (LÓGICOS E ACADÊMICOS) ---
    elif st.session_state.status_jogo == "minigame_timeline":
        st.subheader("🧩 Minigame: Reconstituição de Linha do Tempo Histórica")
        st.write("Ordene cronologicamente a evolução dos referenciais geodésicos e marcos regulatórios adotados na história cartográfica do Brasil:")

        evento_1 = st.selectbox("Evento 1 (Mais Antigo):", ["SIRGAS 2000", "SAD-69", "Córrego Alegre"])
        evento_2 = st.selectbox("Evento 2 (Intermediário):", ["SIRGAS 2000", "SAD-69", "Córrego Alegre"])
        evento_3 = st.selectbox("Evento 3 (Mais Recente):", ["SIRGAS 2000", "SAD-69", "Córrego Alegre"])

        if st.button("Autenticar Sequência Temporal"):
            if evento_1 == "Córrego Alegre" and evento_2 == "SAD-69" and evento_3 == "SIRGAS 2000":
                st.session_state.xp += 40
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "🎯 Perfeito! Sequência histórica exata (Córrego Alegre -> SAD-69 -> SIRGAS 2000). Avança 2 casas!"
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Anacronismo técnico! A evolução cronológica está incorreta. Volte 1 casa."
                st.rerun()

    elif st.session_state.status_jogo == "minigame_radar":
        st.subheader("📡 Minigame: Processamento de Dados de Elevação GNSS")
        st.write("Analise a tabela de dados brutos coletados pela antena receptora. De acordo com as boas práticas, aplica-se uma **Máscara de Elevação de 15°** para cortar efeitos de refração troposférica severa nas baixas altitudes do horizonte.")

        dados_tabela = pd.DataFrame({
            "Satélite Identificado": ["G01 (GPS)", "G05 (GPS)", "R12 (GLONASS)", "E24 (Galileo)", "C02 (BeiDou)"],
            "Ângulo de Elevação Real": ["72°", "11°", "45°", "08°", "31°"]
        })
        st.table(dados_tabela)

        resposta_filtro = st.number_input("Quantos satélites estão válidos para o cálculo do posicionamento (acima de 15°)?", min_value=0, max_value=5, value=0)

        if st.button("Submeter Filtragem"):
            if resposta_filtro == 3:  # G01, R12, C02 estão acima de 15
                st.session_state.xp += 40
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "✅ Excelente interpretação de dados de órbita! Os satélites de 11° e 08° foram devidamente descartados. Avança 2 casas!"
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Erro de processamento! Você incluiu satélites degradados abaixo da máscara de corte. Recua 1 casa."
                st.rerun()

    elif st.session_state.status_jogo == "minigame_associacao":
        st.subheader("🧩 Minigame: Associação de Infraestruturas de Constelações Globais")
        st.write("Realize a correta associação internacional das matrizes operacionais de controle aeroespacial:")

        a1 = st.selectbox("Quem gerencia a constelação Galileo?", ["EUA", "União Europeia", "Federação Russa", "República Popular da China"])
        a2 = st.selectbox("Quem gerencia a constelação GLONASS?", ["EUA", "União Europeia", "Federação Russa", "República Popular da China"])

        if st.button("Validar Vínculos"):
            if a1 == "União Europeia" and a2 == "Federação Russa":
                st.session_state.xp += 40
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "✅ Associação internacional validada! Avança 2 casas."
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Inconsistência de inteligência geopolítica espacial. Recua 1 casa."
                st.rerun()

    elif st.session_state.status_jogo == "minigame_auditoria":
        st.subheader("⚠️ Minigame: Auditoria Estrutural de Metadados")
        st.write("Um topógrafo submeteu o seguinte cabeçalho de dados para homologação de planta no IBGE:")
        st.code("""
        -- METADADOS DO LEVANTAMENTO --
        Projeção Cartográfica: Projeção Universal Transversa de Mercator (UTM)
        Fuso de Trabalho: 22S (Meridiano Central: -51° W)
        Coordenada de Teste Registrada: E = -150.000 m
        Referencial Geodésico Adotado: SIRGAS 2000
        """)

        auditoria_escolha = st.radio("Como auditor sênior, aponte a falha fatal contida neste diário:", [
            "Não há erro, os dados são perfeitamente consistentes.",
            "O erro está na coordenada E. O sistema UTM não admite valores de coordenadas planas Este negativos.",
            "O erro está no meridiano central atribuído ao fuso 22."
        ])

        if st.button("Executar Parecer Final"):
            if "não admite valores de coordenadas planas Este negativos" in auditoria_escolha:
                st.session_state.xp += 50
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "⚠️ Perfeito! Na projeção UTM, soma-se uma constante de 500.000m ao Meridiano Central exatamente para proibir a existência de coordenadas 'E' negativas dentro de qualquer fuso. Avança 2 casas!"
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Fraude/Erro não detectado na auditoria de coordenadas! Volte 1 casa para revisão."
                st.rerun()

    elif st.session_state.status_jogo == "minigame_pistas":
        st.subheader("🧩 Minigame: Jogo das Três Pistas Técnicas")
        st.write("Adivinhe o conceito fundamental com base nas dicas graduais apresentadas:")

        st.markdown("* **Pista 1:** Sou um modelo puramente geométrico e matemático matemático perfeito.")
        st.markdown("* **Pista 2:** Sou gerado por meio da rotação de uma elipse plana ao redor do seu eixo menor.")
        st.markdown("* **Pista 3:** Sirvo de base computacional para o cálculo de latitude e longitude em softwares de SIG.")

        resposta_pista = st.text_input("Qual é a estrutura matemática geodésica? (Dica: uma única palavra)").strip().lower()

        if st.button("Verificar Palavra"):
            if resposta_pista in ["elipsoide", "elipsóide"]:
                st.session_state.xp += 40
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "✅ Excelente! O elipsoide cumpre esse papel estrutural geométrico. Avança 2 casas!"
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Resposta errada! O modelo descrito não coincide com seu palpite. Recua 1 casa."
                st.rerun()

    elif st.session_state.status_jogo == "minigame_criptograma":
        st.subheader("🧩 Minigame: Criptograma de Transmissão de Satélites")
        st.write("Um receptor decodificou um acrônimo importante criptografado por uma cifra de deslocamento simples (Cifra de César de +1 letra).")
        st.info("Mensagem Encriptada Recebida: **S B N D**")
        st.caption("Dica: Se a letra fosse 'B', subtraindo 1 no alfabeto ela voltaria a ser 'A'.")

        resposta_cripto = st.text_input("Qual é a sigla real da infraestrutura de monitoramento contínuo do IBGE?").strip().upper()

        if st.button("Descriptografar"):
            if resposta_cripto == "RBMC":
                st.session_state.xp += 40
                st.session_state.posicao += 2
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "🎯 Código quebrado! S(-1)=R, B(-1)=B, N(-1)=M, D(-1)=C -> RBMC! Avança 2 casas."
                st.rerun()
            else:
                st.session_state.posicao = max(0, st.session_state.posicao - 1)
                st.session_state.status_jogo = "jogar"
                st.session_state.historico = "💥 Falha de descriptografia. Ruído de sinal gerou dados incorretos. Recua 1 casa."
                st.rerun()

    elif st.session_state.status_jogo == "fim":
        st.balloons()
        st.success(f"🏆 GRANDE CAMPANHA CONCLUÍDA COM SUCESSO! Você finalizou o tabuleiro com {st.session_state.xp} XP acumulados!")
        st.markdown("### Relatório Verde de Desempenho do Aluno")
        st.write(f"* **Total de acertos teóricos:** {st.session_state.acertos}")
        st.write(f"* **Total de desvios/erros:** {st.session_state.erros}")
        st.write(f"* **Nível de Registro Técnico Conquistado:** {obter_nivel(st.session_state.xp)}")

        if st.button("🔄 Iniciar Nova Campanha do Zero"):
            del st.session_state.posicao
            del st.session_state.banco_perguntas
            del st.session_state.status_jogo
            del st.session_state.xp
            del st.session_state.acertos
            del st.session_state.erros
            del st.session_state.conquistas
            st.rerun()
